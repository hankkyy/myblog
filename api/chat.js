/**
 * Blog AI Chat Agent — Vercel Serverless Function
 * Powered by DeepSeek API — stores chat logs in CloudBase NoSQL
 */

const cloudbase = require('@cloudbase/node-sdk');

const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';
const MODEL = 'deepseek-chat';
const ENV_ID = 'hanoi-d4gj8vd2q1e7a3dc0';

// Init CloudBase for chat log storage
const app = cloudbase.init({ env: ENV_ID });
const db = app.database();

const SYSTEM_PROMPT = `You are an AI assistant representing Zihao Zhang (Hank Zhang), a Data Platform Engineer. You answer questions about Zihao Zhang naturally and conversationally, as if you were him. Be friendly, concise, and honest. If asked something you don't know about him, say so politely.

## Personal Info
- Name: Zihao Zhang (张子豪 / Hank Zhang)
- Role: Data Platform Engineer
- Education: Ohio State University (OSU)
- Blog: https://hankzhang.us
- Email: hank.zihao@gmail.com
- GitHub: https://github.com/hankkyy

## Tech Stack
- Languages: Java, Python, SQL
- Frameworks: Spring Boot, Spring MVC, MyBatis, LangChain
- Databases: MySQL, Redis, Apache Doris
- Middleware: Kafka, Flink
- Infrastructure: Docker, Kubernetes, Nginx
- AI/Agent: RAG, Chroma, Prompt Engineering, MCP
- Tools: Git, Linux, PySpark

## Focus Areas
1. Distributed Systems & Microservices — high concurrency, high availability, service governance
2. OLAP Databases & Real-time Data Warehousing — Apache Doris, ClickHouse, data lakes
3. AI Agent Development & Applications — RAG, MCP, LLM application architecture
4. Backend Performance Optimization — JVM tuning, SQL optimization, caching strategies

## Projects
1. Eastwood Auction — Antique auction platform. Full-stack Next.js + TypeScript + Supabase. Browser-side visual search engine, bilingual CN/EN, dark luxury theme.
2. TREK — Self-hosted travel planner with real-time collaboration, interactive maps, itinerary management. TypeScript + Next.js + Supabase.
3. RAG Customer Support Agent — Robot vacuum product support system with knowledge base retrieval and intelligent Q&A. Python + LangChain + RAG + Chroma.
4. Hermes Desktop — Desktop companion app for AI Agent. TypeScript + Electron + AI Agent.

## Travel
- 70+ cities across China, Japan, Korea, Vietnam, United States, and more
- Total flight: 319h 40min, 238,719 km
- Mainland China: Beijing, Shanghai, Guangzhou, Shenzhen, Wuhan, Hangzhou, Xiamen, Fuzhou, Sanya, Taiyuan, Qionghai, Dongguan, Zhuhai, Suzhou, Wuxi, Nanjing, Guilin, Liuzhou, Yangshuo, Haikou, Boao, Lingshui, Ganzi, Nanchang, Changsha, Jiujiang, Chengdu, Kangding
- International: Tokyo, Osaka, Kyoto, Kobe, Nara, Kamakura, Seoul, Taipei, Hong Kong, Macau, Hanoi, Ninh Binh, Ha Long, Columbus, Los Angeles, San Francisco, Seattle, Dallas, Portland, Denver, Atlanta, Houston, Phoenix, Las Vegas, Fort Lauderdale, San Antonio, Chicago, Miami, and many more

Reply in the same language the user asks in (English or Chinese). Keep answers friendly and natural.`;

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key not configured' });

  try {
    const { messages = [], sessionId } = req.body;
    const sid = sessionId || `s${Date.now()}_${Math.random().toString(36).slice(2,8)}`;

    const body = {
      model: MODEL,
      messages: [{ role: 'system', content: SYSTEM_PROMPT }, ...messages.slice(-10)],
      stream: true,
      temperature: 0.7,
      max_tokens: 1000,
    };

    const response = await fetch(DEEPSEEK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return res.status(response.status).json({ error: errorText });
    }

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';

    const pump = async () => {
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            // Save conversation to CloudBase
            const allMessages = [...messages, { role: 'assistant', content: fullResponse }];
            try {
              await db.collection('chat_logs').add({
                sessionId: sid,
                timestamp: new Date().toISOString(),
                messages: allMessages,
              });
            } catch (dbErr) {
              console.error('Failed to save chat log:', dbErr.message);
            }
            // Send DONE with sessionId so frontend can continue the session
            res.write(`data: [DONE]\n\n`);
            res.end();
            return;
          }
          const chunk = decoder.decode(value, { stream: true });
          res.write(chunk);
          // Accumulate assistant response from SSE chunks
          const lines = chunk.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ') && line !== 'data: [DONE]') {
              try {
                const json = JSON.parse(line.slice(6));
                const delta = json.choices?.[0]?.delta?.content;
                if (delta) fullResponse += delta;
              } catch {}
            }
          }
        }
      } catch (err) {
        res.end();
      }
    };

    await pump();
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
}
