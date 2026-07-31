/**
 * Admin API — Read chat logs from CloudBase NoSQL
 * Password-protected: only Zihao can access
 */

const cloudbase = require('@cloudbase/node-sdk');

const ENV_ID = 'hanoi-d4gj8vd2q1e7a3dc0';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'hankyky';

const app = cloudbase.init({ env: ENV_ID });
const db = app.database();

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { password, page = 1, pageSize = 20 } = req.body;

    if (password !== ADMIN_PASSWORD) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Count total
    const countResult = await db.collection('chat_logs').count();
    const total = countResult.total;

    // Fetch logs, newest first, paginated
    const result = await db.collection('chat_logs')
      .orderBy('timestamp', 'desc')
      .skip((page - 1) * pageSize)
      .limit(pageSize)
      .get();

    const logs = result.data.map(item => ({
      id: item._id,
      sessionId: item.sessionId,
      timestamp: item.timestamp,
      messages: item.messages,
    }));

    return res.json({
      logs,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
    });
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
}
