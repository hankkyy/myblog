#!/usr/bin/env python3
"""构建脚本 — 1:1 匹配 sinyalee.com/blog"""

import re, shutil
from datetime import datetime
from pathlib import Path
import frontmatter
from markdown import markdown

SRC = Path(__file__).parent
ROOT = SRC.parent
CONTENT = SRC / "content"
THEME = SRC / "themes" / "cenote-style"
CSS_DIR = ROOT / "css"

SITE = {"title":"Welcome To My Blog","url":"https://hankzhang.us/","desc":"「保持好奇心，继续探索世界」"}
AUTHOR = "Zihao Zhang"
YEAR = str(datetime.now().year)
MENU = [("首页","/"),("文章列表","/posts/"),("分类","/categories/"),("关于","/about/")]
SAFE = {".git","src","vercel.json",".gitignore","README.md","pagefind","images","api","package.json","package-lock.json","node_modules"}

# i18n strings
T = {
    "en": {
        "html_lang": "en",
        "skip_link": "Skip to content",
        "site_desc": '"Wonder more, wander further"',
        "nav": [("Home","/"),("Archives","/posts/"),("Categories","/categories/"),("About","/about/")],
        "read_more": "Read More",
        "prev_post": "Previous",
        "next_post": "Next",
        "post_nav_aria": "Posts",
        "post_nav_sr": "Post Navigation",
        "about_author": "About {author}",
        "author_bio": "Data Platform Engineer. Distributed systems, OLAP databases, AI Agent development.",
        "comments": "Comments",
        "comments_closed": "Comments are closed.",
        "recent_posts": "Recent Posts",
        "categories_widget": "Categories",
        "category_prefix": "Category: ",
        "category": "Category",
        "category_count": "（{n} articles）",
        "post_list": "Archives",
        "page_title": "Page {n}",
        "page_aria": "Post Pagination",
        "jump_placeholder": "Go",
        "articles_count": "articles",
        "categories_count": "categories",
        "date_fmt": lambda d: f"{d.year}-{d.month:02d}-{d.day:02d}",
        "year_suffix": "",
        "month_suffix": "",
        "home_title": "Home",
        "about_title": "About",
        "about_greeting": "Hi, I'm",
        "about_name": "Zihao Zhang",
        "about_name_sub": "",
        "about_bio": "Data Platform Engineer — Data Infrastructure & AI Agent Development.",
        "about_skills": "Tech Stack",
        "about_focus": "Focus Areas",
        "about_projects": "Projects",
        "about_hobby": "Interests",
        "about_blog": "About This Blog",
        "about_contact": "Get In Touch",
        "about_hero_img_alt": "Zihao Zhang",
        "skill_lang": "Languages",
        "skill_fw": "Frameworks",
        "skill_db": "Databases",
        "skill_mq": "Middleware",
        "skill_infra": "Infrastructure",
        "skill_ai": "AI / Agent",
        "skill_tools": "Tools",
        "skill_lang_val": "Java · Python · SQL",
        "skill_fw_val": "Spring Boot · Spring MVC · MyBatis · LangChain",
        "skill_db_val": "MySQL · Redis · Apache Doris",
        "skill_mq_val": "Kafka · Flink",
        "skill_infra_val": "Docker · Kubernetes · Nginx",
        "skill_ai_val": "RAG · Chroma · Prompt Engineering · MCP",
        "skill_tools_val": "Git · Linux · PySpark",
        "focus_items": [
            ("Distributed Systems & Microservices", "High concurrency, high availability, service governance"),
            ("OLAP Databases & Real-time Data Warehousing", "Apache Doris, ClickHouse, data lakes"),
            ("AI Agent Development & Applications", "RAG, MCP, LLM application architecture"),
            ("Backend Performance Optimization", "JVM tuning, SQL optimization, caching strategies"),
        ],
        "project_eastwood_desc": "Antique auction platform. Full-stack Next.js + TypeScript + Supabase app. Browser-side visual search engine (multi-dimensional feature signatures, weighted similarity, confidence gating), bilingual CN/EN, dark luxury theme design system.",
        "project_trek_desc": "Self-hosted travel planner with real-time collaboration, interactive maps, and itinerary management.",
        "project_rag_desc": "RAG-based customer support system for robot vacuum products, supporting knowledge base retrieval and intelligent Q&A.",
        "project_hermes_desc": "Desktop companion app for Hermes Agent, providing localized AI Agent interaction experience.",
        "hobby_text": 'Passionate about travel and aviation. Half of my geography knowledge comes from books, the other half from airplane windows at 30,000 feet.<br>Seeing the world shapes your vision — visit more places, meet more people, understand more.',
        "blog_about_text": 'A static site built with Python, deployed on Vercel. Theme inspired by WordPress Cenote.<br>Technical notes, project retrospectives, industry observations. Quality over frequency.',
        "flight_hours": "Total Flight Hours",
        "flight_km": "Total Flight Distance",
        "cities_count_label": "Cities Visited",
        "mainland_china": "🇨🇳 Mainland China",
        "international": "🌍 International",
        "lang_switch_en": "EN",
        "lang_switch_zh": "中",
        "copyright": 'Copyright © {year} <a href="{url}" title="{title}"><span>{title}</span></a>. All rights reserved.',
        "chat_title": "Ask Me Anything",
        "chat_placeholder": "Ask about my skills, projects, or travel...",
        "chat_welcome": "Hi! I'm Hank's AI assistant. Ask me anything about his skills, projects, or travel experiences!",
        "chat_send": "Send",
        "chat_typing": "Thinking...",
        "admin_password": "Enter password",
        "admin_unlock": "Unlock",
        "admin_title": "Chat Logs",
        "admin_loading": "Loading...",
        "admin_empty": "No conversations yet.",
        "admin_logout": "Lock",
        "admin_close": "Close",
    },
    "zh": {
        "html_lang": "zh-Hans",
        "skip_link": "跳到内容",
        "site_desc": "「保持好奇心，继续探索世界」",
        "nav": [("首页","/zh/"),("文章列表","/zh/posts/"),("分类","/zh/categories/"),("关于","/zh/about/")],
        "read_more": "阅读更多",
        "prev_post": "上一篇文章",
        "next_post": "下一篇文章",
        "post_nav_aria": "文章",
        "post_nav_sr": "文章导航",
        "about_author": "关于 {author}",
        "author_bio": "数据平台工程师。关注分布式系统，OLAP 数据库，AI Agent 开发与应用。",
        "comments": "评论",
        "comments_closed": "评论已关闭。",
        "recent_posts": "近期文章",
        "categories_widget": "分类",
        "category_prefix": "分类： ",
        "category": "分类",
        "category_count": "（{n} 篇）",
        "post_list": "文章列表",
        "page_title": "第{n}页",
        "page_aria": "文章分页",
        "jump_placeholder": "跳转",
        "articles_count": "篇文章",
        "categories_count": "个分类",
        "date_fmt": lambda d: f"{d.year}年{d.month}月{d.day}日",
        "year_suffix": "年",
        "month_suffix": "月",
        "home_title": "首页",
        "about_title": "关于",
        "about_greeting": "Hi, I'm",
        "about_name": "张子豪",
        "about_name_sub": " · Hank Zhang",
        "about_bio": "数据平台工程师，专注于数据基础设施与 AI Agent 开发。",
        "about_hero_img_alt": "张子豪",
        "about_skills": "技术栈",
        "about_focus": "关注方向",
        "about_projects": "项目",
        "about_hobby": "兴趣爱好",
        "about_blog": "关于这个博客",
        "about_contact": "欢迎交流",
        "skill_lang": "语言",
        "skill_fw": "框架",
        "skill_db": "数据库",
        "skill_mq": "中间件",
        "skill_infra": "基础设施",
        "skill_ai": "AI / Agent",
        "skill_tools": "工具",
        "skill_lang_val": "Java · Python · SQL",
        "skill_fw_val": "Spring Boot · Spring MVC · MyBatis · LangChain",
        "skill_db_val": "MySQL · Redis · Apache Doris",
        "skill_mq_val": "Kafka · Flink",
        "skill_infra_val": "Docker · Kubernetes · Nginx",
        "skill_ai_val": "RAG · Chroma · Prompt Engineering · MCP",
        "skill_tools_val": "Git · Linux · PySpark",
        "focus_items": [
            ("分布式系统与微服务架构", "高并发、高可用、服务治理"),
            ("OLAP 数据库与实时数仓", "Apache Doris、ClickHouse、数据湖"),
            ("AI Agent 开发与应用", "RAG、MCP、LLM 应用架构"),
            ("后端性能优化", "JVM 调优、SQL 优化、缓存策略"),
        ],
        "project_eastwood_desc": "古董拍卖平台。Next.js + TypeScript + Supabase 全栈应用。浏览器端视觉搜索引擎（多维特征签名、加权相似度、置信度门控），中英双语，暗色奢华主题设计系统。",
        "project_trek_desc": "自托管旅行规划器，支持实时协作、交互式地图和行程管理。",
        "project_rag_desc": "基于 RAG 的扫地机器人产品客服系统，支持知识库检索和智能问答。",
        "project_hermes_desc": "Hermes Agent 桌面伴侣应用，提供本地化 AI Agent 交互体验。",
        "hobby_text": "热爱旅行和航空。地理知识，一半来自书本，另一半来自三万英尺高空的舷窗。<br>相信眼界决定世界——去更多地方，见更多人，理解更多事。",
        "blog_about_text": "用 Python 构建的静态站点，部署在 Vercel。外观参考 WordPress Cenote 主题。<br>写技术笔记、项目复盘、行业观察。不追求日更，追求每篇都值得读。",
        "flight_hours": "累计飞行时长",
        "flight_km": "累计飞行里程",
        "cities_count_label": "个城市",
        "mainland_china": "🇨🇳 中国大陆",
        "international": "🌍 国际 · 港澳台",
        "lang_switch_en": "EN",
        "lang_switch_zh": "中",
        "copyright": 'Copyright © {year} <a href="{url}" title="{title}"><span>{title}</span></a>. All rights reserved.',
        "chat_title": "随便问问",
        "chat_placeholder": "问我技能、项目、旅行经历...",
        "chat_welcome": "你好！我是 Hank 的 AI 助手，可以问我关于他的技能、项目或旅行经历！",
        "chat_send": "发送",
        "chat_typing": "思考中...",
        "admin_password": "输入密码",
        "admin_unlock": "解锁",
        "admin_title": "对话记录",
        "admin_loading": "加载中...",
        "admin_empty": "暂无对话记录。",
        "admin_logout": "锁定",
        "admin_close": "关闭",
    },
}

# 旅行城市数据 — 来源：航旅纵横行程导出（含广州、东莞）
# 两栏：中国大陆 / 国际（含港澳台）
TRAVEL_CITIES = [
    ("🇨🇳 中国大陆", "mainland", [
        "北京", "上海", "广州", "深圳", "武汉", "杭州",
        "厦门", "福州", "三亚", "太原", "琼海", "东莞",
        "珠海", "苏州", "无锡", "南京",
        "桂林", "柳州", "阳朔", "海口", "博鳌", "陵水", "甘孜",
        "南昌", "长沙", "九江", "成都", "康定",
    ]),
    ("🌍 国际 · 港澳台", "international", [
        "东京", "大阪", "京都", "神户", "奈良", "镰仓", "首尔",
        "台北", "香港", "澳门",
        "河内", "宁平", "下龙", "海阳",
        "哥伦布", "洛杉矶", "旧金山", "西雅图", "达拉斯", "波特兰",
        "丹佛", "亚特兰大", "休斯敦", "凤凰城", "拉斯维加斯",
        "劳德代尔堡", "圣安东尼奥", "圣安娜", "坦帕",
        "奥克兰", "安大略", "底特律", "长滩", "雷诺",
        "圣何塞", "奥兰多", "迈阿密", "尔湾", "芝加哥",
        "太浩湖", "伯克利", "圣克鲁兹",
    ]),
]


def menu_html(lang, current="/"):
    parts = []
    for label, url in T[lang]["nav"]:
        a = ' class="active"' if current == url else ""
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        parts.append(f'<li class="menu-item menu-item-type-custom menu-item-object-custom"><a href="{url}"{a}{ext}>{label}</a></li>')
    return "".join(parts)


def page_html(title_tag, body, *, lang="en", base_path="", current="/", desc="", is_home=False, body_class="layout--no-sidebar", extra_body_class="", sticky_title=""):
    t = T[lang]
    main_nav = menu_html(lang, current)
    st = SITE["title"]
    site_title_tag = "h1" if is_home else "p"
    desc_meta = f'<meta name="description" content="{desc}">' if desc else ""
    bc = f"{body_class} {extra_body_class}".strip()
    site_url = SITE["url"]
    site_url_clean = site_url.rstrip('/')
    page_full_url = f"{site_url_clean}{base_path}/" if current == f"{base_path}/" else f"{site_url_clean}{current}"
    other_lang = "zh" if lang == "en" else "en"
    other_base = "/zh/" if lang == "en" else "/"
    other_current = current.replace(base_path + "/", other_base) if base_path else other_base + current.lstrip("/")
    lang_switch_html = f'<a href="{other_current}" class="lang-link">{t["lang_switch_" + other_lang]}</a>'

    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_tag}</title>
{desc_meta}
<meta property="og:title" content="{title_tag}">
<meta property="og:description" content="{desc or t['site_desc']}">
<meta property="og:type" content="{'website' if is_home else 'article'}">
<meta property="og:url" content="{page_full_url}">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="{page_full_url}">
<link rel="alternate" hreflang="{"zh-Hans" if other_lang == "zh" else "en"}" href="{site_url}{other_current}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{'Article' if not is_home and current != base_path + '/about/' else 'WebSite'}",
  "headline": "{title_tag}",
  "description": "{desc or t['site_desc']}",
  "url": "{page_full_url}",
  "datePublished": "2026-06-17",
  "author": {{ "@type": "Person", "name": "{AUTHOR}" }}
}}
</script>
<link rel="stylesheet" href="/css/style.css">
<link rel="icon" type="image/png" href="/favicon.png">
</head>
<body class="{bc}">
<div id="page" class="site">
<a class="skip-link screen-reader-text" href="#content">{t['skip_link']}</a>
<header id="masthead" class="site-header tg-site-header tg-site-header--default">
  <div class="tg-header-top">
    <div class="container" style="display:flex;justify-content:flex-end;align-items:center;padding:8px 0">
      <div class="lang-switch">{lang_switch_html}</div>
    </div>
  </div>
  <div class="tg-header-bottom">
    <div class="header-bottom-top">
      <div class="container tg-flex-container tg-flex-space-between tg-flex-item-centered">
        <div class="site-branding">
          <{site_title_tag} class="site-title"><a href="{site_url}{base_path}/" rel="home">{st}</a></{site_title_tag}>
          <p class="site-description">{t['site_desc']}</p>
        </div>
      </div>
    </div>
    <div class="header-bottom-bottom">
      <div class="container" style="display:flex;justify-content:center;align-items:center;gap:15px">
        <nav id="site-navigation" class="main-navigation tg-site-menu--default" style="display:inline-flex;align-items:center;gap:10px">
          <div class="menu-menu-container"><ul id="primary-menu" class="nav-menu" style="justify-content:center">{main_nav}</ul></div>
        </nav>
      </div>
    </div>
  </div>
</header>
<nav id="cenote-sticky-header" class="cenote-header-sticky">
  <div class="sticky-header-slide">
    <div class="cenote-sticky-main">
      <div class="container tg-flex-container tg-flex-space-between tg-flex-item-centered">
        {f'<span class="sticky-title">{sticky_title}</span>' if sticky_title else f'<nav class="main-navigation cenote-sticky-navigation tg-site-menu--default"><div class="menu-menu-container"><ul class="menu" style="justify-content:center">{main_nav}</ul></div></nav>'}
      </div>
    </div>
  </div>
</nav>
<div id="content" class="site-content">
  <div class="container">
{body}
  </div>
</div>
<footer id="colophon" class="site-footer tg-site-footer tg-site-footer--default">
  <div class="tg-footer-bottom">
    <div class="container">
      <div class="site-info" style="display:flex;justify-content:space-between;align-items:center">
        <span id="footer-copyright">{t['copyright'].format(year=YEAR, url=site_url, title=st)}</span>
        <nav style="display:flex;gap:15px">
          {"".join(f'<a href=\"{url}\"{(" target=\"_blank\" rel=\"noopener\"" if url.startswith("http") else "")}>{label}</a>' for label, url in t["nav"])}
        </nav>
      </div>
    </div>
  </div>
</footer>
<button id="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" style="position:fixed;bottom:30px;right:30px;width:44px;height:44px;border-radius:50%;background:#16181a;color:#fff;border:none;cursor:pointer;font-size:20px;display:none;z-index:999;box-shadow:0 2px 8px rgba(0,0,0,.2)">↑</button>
<script>
window.addEventListener('scroll',function(){{document.getElementById('back-to-top').style.display=window.scrollY>300?'block':'none';var s=document.getElementById('cenote-sticky-header');if(s)s.classList.toggle('visible',window.scrollY>200);}});
</script>
<!-- AI Chat Widget -->
<div id="chat-widget">
  <button id="chat-toggle" onclick="toggleChat()" title="{t['chat_title']}">
    <svg id="chat-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"></path></svg>
    <svg id="chat-close-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
  </button>
  <div id="chat-panel">
    <div id="chat-header">
      <span>{t['chat_title']}</span>
      <button onclick="toggleChat()" style="background:none;border:none;color:#fff;cursor:pointer;font-size:18px;line-height:1">&times;</button>
    </div>
    <div id="chat-messages">
      <div class="chat-msg assistant"><div class="chat-bubble">{t['chat_welcome']}</div></div>
    </div>
    <div id="chat-input-area">
      <input type="text" id="chat-input" placeholder="{t['chat_placeholder']}" onkeydown="if(event.key==='Enter')sendMessage()">
      <button id="chat-send-btn" onclick="sendMessage()">{t['chat_send']}</button>
    </div>
  </div>
</div>
<style>
#chat-widget{{position:fixed;bottom:30px;right:30px;z-index:1000;font-family:"Roboto",helvetica,arial,sans-serif}}
#chat-toggle{{width:50px;height:50px;border-radius:50%;background:#16181a;color:#fff;border:none;cursor:pointer;font-size:22px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 16px rgba(0,0,0,.15);transition:transform .2s,box-shadow .2s}}
#chat-toggle:hover{{transform:scale(1.08);box-shadow:0 6px 24px rgba(0,0,0,.25)}}
#chat-panel{{display:none;position:absolute;bottom:60px;right:0;width:360px;max-width:calc(100vw - 32px);height:500px;max-height:calc(100vh - 120px);background:#fff;border-radius:12px;box-shadow:0 8px 40px rgba(0,0,0,.12);flex-direction:column;overflow:hidden}}
#chat-panel.open{{display:flex}}
#chat-header{{background:#16181a;color:#fff;padding:14px 18px;font-weight:700;font-size:15px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
#chat-messages{{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;background:#fafbfc}}
.chat-msg{{display:flex;max-width:85%}}
.chat-msg.user{{align-self:flex-end}}
.chat-msg.assistant{{align-self:flex-start}}
.chat-bubble{{padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.55;word-break:break-word}}
.chat-msg.user .chat-bubble{{background:#146bb7;color:#fff;border-bottom-right-radius:4px}}
.chat-msg.assistant .chat-bubble{{background:#fff;color:#363b40;border:1px solid #e9ecef;border-bottom-left-radius:4px}}
.chat-msg.typing .chat-bubble{{color:#adb5bd;font-style:italic}}
#chat-input-area{{display:flex;gap:8px;padding:12px 16px;border-top:1px solid #f1f3f5;flex-shrink:0;background:#fff}}
#chat-input{{flex:1;border:1px solid #e9ecef;border-radius:20px;padding:10px 16px;font-size:14px;outline:none;color:#363b40;transition:border-color .2s}}
#chat-input:focus{{border-color:#146bb7}}
#chat-send-btn{{background:#146bb7;color:#fff;border:none;border-radius:20px;padding:10px 20px;font-size:13px;font-weight:600;cursor:pointer;transition:background .2s;white-space:nowrap}}
#chat-send-btn:hover{{background:#0e5a9e}}
#chat-send-btn:disabled{{opacity:.5;cursor:default}}
/* Language switcher */
.lang-switch{{display:flex;align-items:center}}
.lang-link{{display:inline-flex;align-items:center;justify-content:center;min-width:36px;height:30px;padding:0 10px;border:1px solid rgba(255,255,255,.35);border-radius:15px;color:#fff;font-size:13px;font-weight:600;text-decoration:none;letter-spacing:.5px;transition:all .25s;background:rgba(255,255,255,.08)}}
.lang-link:hover{{background:rgba(255,255,255,.2);border-color:rgba(255,255,255,.6);transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.15);text-decoration:none;color:#fff}}
@media(max-width:768px){{#chat-panel{{width:calc(100vw - 32px);right:-8px;height:450px}}#chat-widget{{bottom:76px;right:16px}}}}
</style>
<script>
(function(){{
var panel=document.getElementById('chat-panel');
var input=document.getElementById('chat-input');
var messages=document.getElementById('chat-messages');
var sendBtn=document.getElementById('chat-send-btn');
var chatIcon=document.getElementById('chat-icon');
var closeIcon=document.getElementById('chat-close-icon');
var isOpen=false;
var isStreaming=false;
var sessionId='s'+Date.now()+'_'+Math.random().toString(36).slice(2,8);

window.toggleChat=function(){{
  isOpen=!isOpen;
  panel.classList.toggle('open',isOpen);
  chatIcon.style.display=isOpen?'none':'block';
  closeIcon.style.display=isOpen?'block':'none';
  if(isOpen){{input.focus();messages.scrollTop=messages.scrollHeight;}}
}};

function addMessage(role,text){{
  var div=document.createElement('div');
  div.className='chat-msg '+role;
  div.innerHTML='<div class="chat-bubble">'+text+'</div>';
  messages.appendChild(div);
  messages.scrollTop=messages.scrollHeight;
  return div;
}}

function addTyping(){{return addMessage('assistant typing','{t['chat_typing']}');}}

window.sendMessage=async function(){{
  if(isStreaming)return;
  var text=input.value.trim();
  if(!text)return;
  input.value='';
  addMessage('user',text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'));
  var typing=addTyping();
  isStreaming=true;
  sendBtn.disabled=true;
  input.disabled=true;

  // Build conversation history
  var history=[];
  var msgs=messages.querySelectorAll('.chat-msg:not(.typing)');
  msgs.forEach(function(m){{
    var role=m.classList.contains('user')?'user':'assistant';
    var content=m.querySelector('.chat-bubble').textContent;
    history.push({{role:role,content:content}});
  }});

  try{{
    var resp=await fetch('/api/chat',{{
      method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{messages:history,sessionId:sessionId}})
    }});
    if(!resp.ok)throw new Error('API error');
    typing.remove();

    var assistantDiv=addMessage('assistant','');
    var bubble=assistantDiv.querySelector('.chat-bubble');
    var fullText='';
    var reader=resp.body.getReader();
    var decoder=new TextDecoder();
    var buffer='';

    while(true){{
      var r=await reader.read();
      if(r.done)break;
      buffer+=decoder.decode(r.value,{{stream:true}});
      var lines=buffer.split('\\n');
      buffer=lines.pop()||'';
      for(var i=0;i<lines.length;i++){{
        var line=lines[i].trim();
        if(!line.startsWith('data: '))continue;
        var data=line.slice(6);
        if(data==='[DONE]')break;
        try{{
          var json=JSON.parse(data);
          var delta=json.choices&&json.choices[0]&&json.choices[0].delta;
          if(delta&&delta.content){{
            fullText+=delta.content;
            bubble.textContent=fullText;
            messages.scrollTop=messages.scrollHeight;
          }}
        }}catch(e){{}}
      }}
    }}
    if(!fullText)bubble.textContent='Sorry, something went wrong. Please try again.';
  }}catch(e){{
    typing.remove();
    addMessage('assistant','Sorry, the service is temporarily unavailable. Please try again later.');
  }}
  isStreaming=false;
  sendBtn.disabled=false;
  input.disabled=false;
  input.focus();
}};
}})();
</script>
<!-- Hidden Admin Panel (triple-click footer copyright to open) -->
<div id="admin-overlay">
  <div id="admin-panel">
    <div id="admin-header">
      <span>{t['admin_title']}</span>
      <div style="display:flex;gap:8px">
        <button id="admin-logout-btn" onclick="lockAdmin()" style="display:none;background:rgba(255,255,255,.15);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer">{t['admin_logout']}</button>
        <button onclick="closeAdmin()" style="background:none;border:none;color:#fff;cursor:pointer;font-size:18px;line-height:1">{t['admin_close']}</button>
      </div>
    </div>
    <div id="admin-body">
      <div id="admin-login">
        <input type="password" id="admin-password" placeholder="{t['admin_password']}" onkeydown="if(event.key==='Enter')unlockAdmin()">
        <button onclick="unlockAdmin()">{t['admin_unlock']}</button>
      </div>
      <div id="admin-logs" style="display:none">
        <div id="admin-logs-list"></div>
        <div id="admin-pagination" style="display:flex;justify-content:center;gap:8px;padding:16px"></div>
      </div>
    </div>
  </div>
</div>
<style>
#admin-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:10000;align-items:center;justify-content:center}}
#admin-overlay.open{{display:flex}}
#admin-panel{{background:#fff;border-radius:14px;width:700px;max-width:94vw;max-height:80vh;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.25)}}
#admin-header{{background:#16181a;color:#fff;padding:14px 20px;font-weight:700;font-size:15px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
#admin-body{{flex:1;overflow-y:auto;padding:24px}}
#admin-login{{display:flex;flex-direction:column;align-items:center;gap:14px;padding:40px 0}}
#admin-password{{width:260px;padding:12px 18px;border:2px solid #e9ecef;border-radius:10px;font-size:15px;text-align:center;outline:none;transition:border-color .2s;letter-spacing:4px}}
#admin-password:focus{{border-color:#16181a}}
#admin-login button{{padding:10px 40px;background:#16181a;color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;transition:background .2s}}
#admin-login button:hover{{background:#333}}
.log-entry{{border:1px solid #e9ecef;border-radius:10px;margin-bottom:14px;overflow:hidden}}
.log-entry-header{{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:#f8f9fa;cursor:pointer;user-select:none;font-size:13px;color:#495057}}
.log-entry-header:hover{{background:#e8f4fd}}
.log-entry-header .session-id{{font-family:monospace;font-size:12px;color:#868e96}}
.log-entry-header .time{{color:#adb5bd;font-size:12px}}
.log-entry-body{{display:none;padding:16px;border-top:1px solid #e9ecef}}
.log-entry.open .log-entry-body{{display:block}}
.log-entry.open .log-entry-header{{background:#e8f4fd;font-weight:600}}
.log-msg{{margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #f1f3f5}}
.log-msg:last-child{{margin-bottom:0;padding-bottom:0;border-bottom:none}}
.log-msg .role{{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;padding:2px 8px;border-radius:4px;margin-bottom:4px}}
.log-msg .role.user{{background:#146bb7;color:#fff}}
.log-msg .role.assistant{{background:#e8f4fd;color:#146bb7}}
.log-msg .content{{font-size:13px;color:#363b40;line-height:1.6;white-space:pre-wrap;word-break:break-word}}
.copyright-hint{{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:#16181a;color:#fff;padding:8px 20px;border-radius:20px;font-size:13px;opacity:0;transition:opacity .3s;pointer-events:none;z-index:10001}}
.copyright-hint.show{{opacity:.9}}
.page-btn{{min-width:34px;height:34px;border:1px solid #dee2e6;border-radius:6px;background:#fff;color:#495057;font-size:13px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;padding:0 10px;transition:all .2s}}
.page-btn:hover{{background:#16181a;color:#fff;border-color:#16181a}}
.page-btn.active{{background:#16181a;color:#fff;border-color:#16181a}}
.log-chevron{{transition:transform .2s;font-size:12px;color:#adb5bd}}
.log-entry.open .log-chevron{{transform:rotate(180deg)}}
</style>
<script>
(function(){{
var overlay=document.getElementById('admin-overlay');
var pwdInput=document.getElementById('admin-password');
var loginSection=document.getElementById('admin-login');
var logsSection=document.getElementById('admin-logs');
var logoutBtn=document.getElementById('admin-logout-btn');
var logsList=document.getElementById('admin-logs-list');
var pagination=document.getElementById('admin-pagination');
var adminPassword='';
var currentPage=1;
var clickCount=0;
var clickTimer=null;

// Triple click on footer copyright
document.getElementById('footer-copyright').addEventListener('click',function(){{
  clickCount++;
  if(clickCount===1){{
    clickTimer=setTimeout(function(){{clickCount=0;}},600);
  }}
  if(clickCount===3){{
    clearTimeout(clickTimer);
    clickCount=0;
    openAdmin();
  }}
}});

window.openAdmin=function(){{
  overlay.classList.add('open');
  pwdInput.value='';
  pwdInput.focus();
  loginSection.style.display='flex';
  logsSection.style.display='none';
  logoutBtn.style.display='none';
  logsList.innerHTML='';
  pagination.innerHTML='';
}};

window.closeAdmin=function(){{
  overlay.classList.remove('open');
}};

overlay.addEventListener('click',function(e){{
  if(e.target===overlay)closeAdmin();
}});

window.unlockAdmin=function(){{
  adminPassword=pwdInput.value;
  if(!adminPassword)return;
  loadLogs(1);
}};

window.lockAdmin=function(){{
  adminPassword='';
  loginSection.style.display='flex';
  logsSection.style.display='none';
  logoutBtn.style.display='none';
  logsList.innerHTML='';
  pwdInput.value='';
  pwdInput.focus();
}};

window.loadLogs=async function(page){{
  currentPage=page;
  logsList.innerHTML='<p style="text-align:center;color:#adb5bd;padding:40px">{t['admin_loading']}</p>';
  pagination.innerHTML='';

  try{{
    var resp=await fetch('/api/admin/chat-logs',{{
      method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{password:adminPassword,page:page}})
    }});
    if(resp.status===401){{
      logsList.innerHTML='<p style="text-align:center;color:#dc3545;padding:40px">Wrong password</p>';
      return;
    }}
    if(!resp.ok)throw new Error('Failed');
    var data=await resp.json();

    if(data.logs.length===0){{
      logsList.innerHTML='<p style="text-align:center;color:#adb5bd;padding:40px">{t['admin_empty']}</p>';
    }}else{{
      loginSection.style.display='none';
      logsSection.style.display='block';
      logoutBtn.style.display='block';
      logsList.innerHTML='';
      data.logs.forEach(function(log){{
        var entry=document.createElement('div');
        entry.className='log-entry';
        var date=new Date(log.timestamp);
        var timeStr=date.toLocaleString();
        var preview=(log.messages&&log.messages[0])?log.messages[0].content.slice(0,80):'';
        entry.innerHTML='<div class="log-entry-header" onclick="this.parentElement.classList.toggle(\'open\')"><div><span style="color:#16181a;font-weight:600">'+preview.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span></div><div style="display:flex;align-items:center;gap:12px"><span class="session-id">'+log.sessionId.slice(0,12)+'</span><span class="time">'+timeStr+'</span><span class="log-chevron">▼</span></div></div>';
        var body=document.createElement('div');
        body.className='log-entry-body';
        if(log.messages){{
          log.messages.forEach(function(m){{
            var msgDiv=document.createElement('div');
            msgDiv.className='log-msg';
            msgDiv.innerHTML='<span class="role '+m.role+'">'+m.role+'</span><div class="content">'+(m.content||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</div>';
            body.appendChild(msgDiv);
          }});
        }}
        entry.appendChild(body);
        logsList.appendChild(entry);
      }});

      // Pagination
      var pg='';
      var tp=data.totalPages;
      if(tp>1){{
        var pages=[];
        for(var i=Math.max(1,page-2);i<=Math.min(tp,page+2);i++)pages.push(i);
        if(pages[0]>1){{pg+='<button class="page-btn" onclick="loadLogs(1)">1</button>';if(pages[0]>2)pg+='<span style="padding:0 4px;color:#adb5bd">…</span>';}}
        pages.forEach(function(p){{pg+='<button class="page-btn'+(p===page?' active':'')+'" onclick="loadLogs('+p+')">'+p+'</button>';}});
        if(pages[pages.length-1]<tp){{if(pages[pages.length-1]<tp-1)pg+='<span style="padding:0 4px;color:#adb5bd">…</span>';pg+='<button class="page-btn" onclick="loadLogs('+tp+')">'+tp+'</button>';}}
      }}
      pagination.innerHTML=pg;
    }}
  }}catch(e){{
    logsList.innerHTML='<p style="text-align:center;color:#dc3545;padding:40px">Failed to load. Please try again.</p>';
  }}
}};

// Keyboard shortcut: Escape to close
document.addEventListener('keydown',function(e){{
  if(e.key==='Escape'&&overlay.classList.contains('open'))closeAdmin();
}});

}})();
</script>
</div>
</body>
</html>"""


def parse_page(md_path):
    post = frontmatter.load(md_path)
    content_html = markdown(post.content, extensions=["extra", "codehilite"])
    # Clean: remove code blocks (```...```) and inline code from original markdown
    raw_md = re.sub(r'```[\s\S]*?```', '', post.content)
    raw_md = re.sub(r'`[^`]+`', '', raw_md)
    # Remove ASCII box-drawing lines and other non-prose content
    raw_md = re.sub(r'[┌└┐┘│─├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬]+', '', raw_md)
    # Remove separator lines and markdown artifacts
    raw_md = re.sub(r'^[-*=]{3,}\s*$', '', raw_md, flags=re.MULTILINE)
    raw_md = re.sub(r'^#{1,6}\s', '', raw_md, flags=re.MULTILINE)
    raw_md = re.sub(r'^\|.*\|$', '', raw_md, flags=re.MULTILINE)  # table rows
    # Convert remaining markdown to plain text
    plain = re.sub(r'[\*\|\>\<\[]+', '', raw_md)
    plain = re.sub(r'\s+', ' ', plain).strip()
    summary = plain[:55]
    # Use description for featured card when available (cleaner)
    desc = post.get("description", "")
    long_summary = plain[:180]
    truncated = len(plain) > 55
    long_truncated = len(plain) > 180
    date = post.get("date", datetime.now())
    if isinstance(date, str):
        try: date = datetime.fromisoformat(date)
        except ValueError: date = datetime.now()
    from datetime import date as date_type
    if isinstance(date, date_type) and not isinstance(date, datetime):
        date = datetime.combine(date, datetime.min.time())
    if hasattr(date, 'tzinfo') and date.tzinfo is not None:
        date = date.replace(tzinfo=None)
    return {
        "title": post.get("title", "Untitled"),
        "date": date,
        "date_fmt": lambda lang: T[lang]["date_fmt"](date),
        "date_iso": date.strftime("%Y-%m-%d"),
        "categories": post.get("categories", []),
        "description": post.get("description", ""),
        "content": content_html,
        "summary": summary,
        "long_summary": long_summary,
        "truncated": truncated,
        "long_truncated": long_truncated,
        "slug": md_path.stem,
        "lang": post.get("lang", "en"),
    }


def cat_links_meta(cats, base_path=""):
    if not cats: return ""
    parts = []
    for i, c in enumerate(cats):
        slug = c.lower().replace(" ", "-")
        sep = '<span class="cat-seperator">, </span>' if i > 0 else ""
        parts.append(f'{sep}<a href="{base_path}/categories/{slug}/" rel="category">{c}</a>')
    return "".join(parts)


def cat_links_footer(cats, lang, base_path=""):
    if not cats: return ""
    t = T[lang]
    links = "".join(f'<a href="{base_path}/categories/{c.lower().replace(" ", "-")}/" rel="category">{c}</a>' for c in cats)
    return f'<span class="cat-links">{t["category_prefix"]}{links}</span>'


def posted_on(p, lang, base_path=""):
    return f'<span class="posted-on"><a href="{base_path}/posts/{p["slug"]}/" rel="bookmark"><time class="entry-date published" datetime="{p["date_iso"]}">{p["date_fmt"](lang)}</time></a></span>'


def article_card(p, lang, base_path=""):
    t = T[lang]
    cats_html = cat_links_meta(p["categories"], base_path)
    return f"""<article id="post-{p['slug']}" class="post type-post status-publish format-standard hentry">
            <div class="entry-meta">
              <span class="cat-links">{cats_html}</span>{posted_on(p, lang, base_path)}
            </div>
            <header class="entry-header">
              <h2 class="entry-title"><a href="{base_path}/posts/{p['slug']}/" rel="bookmark">{p['title']}</a></h2>
            </header>
            <div class="entry-content">
              <p>{p['summary']}{' [&hellip;]' if p['truncated'] else ''}</p>
            </div>
            <footer class="entry-footer">
              <a href="{base_path}/posts/{p['slug']}/" class="tg-readmore-link">{t['read_more']}</a>
            </footer>
          </article>"""

def featured_card(p, lang, base_path=""):
    t = T[lang]
    cats_html = cat_links_meta(p["categories"], base_path)
    return f"""<article id="post-{p['slug']}" class="post type-post status-publish format-standard hentry">
            <div class="entry-meta">
              <span class="cat-links">{cats_html}</span>{posted_on(p, lang, base_path)}
            </div>
            <header class="entry-header">
              <h2 class="entry-title"><a href="{base_path}/posts/{p['slug']}/" rel="bookmark">{p['title']}</a></h2>
            </header>
            <div class="entry-content">
              <p>{p['long_summary']}{' [&hellip;]' if p['long_truncated'] else ''}</p>
            </div>
            <footer class="entry-footer">
              <a href="{base_path}/posts/{p['slug']}/" class="tg-readmore-link">{t['read_more']}</a>
            </footer>
          </article>"""


def article_single(p, all_posts, lang, base_path=""):
    t = T[lang]
    idx = next((i for i, pp in enumerate(all_posts) if pp["slug"] == p["slug"]), None)
    prev_html = next_html = ""
    if idx is not None:
        if idx < len(all_posts) - 1:
            prev = all_posts[idx + 1]
            prev_html = f'<div class="nav-previous"><a href="{base_path}/posts/{prev["slug"]}/" rel="prev"><span class="nav-links__label">{t["prev_post"]}</span> {prev["title"]}</a></div>'
        if idx > 0:
            nxt = all_posts[idx - 1]
            next_html = f'<div class="nav-next"><a href="{base_path}/posts/{nxt["slug"]}/" rel="next"><span class="nav-links__label">{t["next_post"]}</span> {nxt["title"]}</a></div>'
    nav = ""
    if prev_html or next_html:
        nav = f"""<nav class="navigation post-navigation" aria-label="{t['post_nav_aria']}">
            <h2 class="screen-reader-text">{t['post_nav_sr']}</h2>
            <div class="nav-links">{prev_html}{next_html}</div>
          </nav>"""

    return f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="post type-post status-publish format-standard hentry">
              <div class="entry-meta">
                <span class="cat-links">{cat_links_meta(p["categories"], base_path)}</span>{posted_on(p, lang, base_path)}
              </div>
              <header class="entry-header">
                <h1 class="entry-title">{p['title']}</h1>
              </header>
              <div class="entry-content">{p['content']}</div>
              <footer class="entry-footer">{cat_links_footer(p['categories'], lang, base_path)}</footer>
            </article>
            {nav}
            <a href="{base_path}/about/" class="author-bio-link">
            <div class="author-bio">
              <div class="author-bio-content">
                <h3>{t['about_author'].format(author=AUTHOR)}</h3>
                <p>{t['author_bio']}</p>
              </div>
            </div>
            </a>
            <div class="comments-area">
              <h3>{t['comments']}</h3>
              <p class="no-comments">{t['comments_closed']}</p>
            </div>
          </main>
        </div>"""


def sidebar_html(posts, lang, base_path=""):
    t = T[lang]
    recent = "".join(f'<li><a href="{base_path}/posts/{p["slug"]}/">{p["title"]}</a></li>' for p in posts[:5])
    cats_set = sorted({c for p in posts for c in p.get("categories", [])})
    tags = "".join(f'<a href="{base_path}/categories/{c.lower().replace(" ", "-")}/">{c}</a>' for c in cats_set)
    return f"""<aside id="secondary" class="widget-area">
          <section class="widget widget_recent_entries">
            <h2 class="widget-title">{t['recent_posts']}</h2>
            <ul>{recent}</ul>
          </section>
          <section class="widget widget_tag_cloud">
            <h2 class="widget-title">{t['categories_widget']}</h2>
            <div class="tagcloud">{tags}</div>
          </section>
        </aside>"""


def build_site(lang, posts):
    """Build the static site for a given language at the appropriate base path."""
    t = T[lang]
    base_path = "" if lang == "en" else "/zh"
    out_root = ROOT / base_path.lstrip("/")

    # ===== HOMEPAGE with pagination =====
    PER_PAGE = 10
    total_pages = max(1, (len(posts) + PER_PAGE - 1) // PER_PAGE)
    home_title = f"{SITE['title']} – {t['site_desc']}"

    def pagination_html(current_page):
        if total_pages <= 1:
            return ""
        show = {1, total_pages}
        for d in range(-2, 3):
            pg = current_page + d
            if 1 < pg < total_pages:
                show.add(pg)
        sorted_pg = sorted(show)
        blocks = []
        prev = 0
        for pg in sorted_pg:
            if pg > prev + 1:
                blocks.append(f'<span class="page-numbers dots">&hellip;</span>')
            if pg == current_page:
                blocks.append(f'<span class="page-numbers current">{pg}</span>')
            else:
                href = f"{base_path}/" if pg == 1 else f"{base_path}/page/{pg}/"
                blocks.append(f'<a class="page-numbers" href="{href}">{pg}</a>')
            prev = pg
        jump_input = f'<span class="page-jump">'
        jump_input += f'<input type="number" min="1" max="{total_pages}" placeholder="{t["jump_placeholder"]}" id="jump-input-{current_page}" style="width:56px;text-align:center;border:1px solid #dee2e6;border-right:none;border-radius:4px 0 0 4px;padding:5px 2px;font-size:.85rem;line-height:1.4;outline:none;color:#363b40;transition:border-color .2s" onfocus="this.style.borderColor=&#39;#146bb7&#39;" onblur="this.style.borderColor=&#39;#dee2e6&#39;">'
        jump_input += f'<button onclick="var v=parseInt(document.getElementById(&quot;jump-input-{current_page}&quot;).value);if(v>=1&&v<={total_pages})location.href=v===1?&quot;{base_path}/&quot;:&quot;{base_path}/page/&quot;+v+&quot;/&quot;" style="border:1px solid #dee2e6;border-left:none;border-radius:0 4px 4px 0;padding:6px 10px;cursor:pointer;background:#f8f9fa;color:#495057;font-size:.85rem;transition:all .2s" onmouseover="this.style.background=&#39;#146bb7&#39;;this.style.color=&#39;#fff&#39;;this.style.borderColor=&#39;#146bb7&#39;" onmouseout="this.style.background=&#39;#f8f9fa&#39;;this.style.color=&#39;#495057&#39;;this.style.borderColor=&#39;#dee2e6&#39;">→</button>'
        jump_input += '</span>'
        return f'<nav class="navigation pagination" aria-label="{t["page_aria"]}"><div class="nav-links">{"".join(blocks)}{jump_input}</div></nav>'

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * PER_PAGE
        end = start + PER_PAGE
        page_posts = posts[start:end]

        if posts:
            first_card = featured_card(page_posts[0], lang, base_path) if page_posts else ""
            rest_cards = "\n".join(article_card(p, lang, base_path) for p in page_posts[1:]) if len(page_posts) > 1 else ""
        else:
            first_card = f'<article class="post type-post status-publish format-standard hentry"><div class="entry-content"><p>{t.get("empty_posts", "No posts yet.")}</p></div></article>'
            rest_cards = ""
        pgn = pagination_html(page_num)

        page_body = f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <div class="tg-archive-featured">{first_card}</div>
            <div class="tg-archive-grid tg-archive-col--3">{rest_cards}</div>
            {pgn}
          </main>
        </div>"""

        if page_num == 1:
            page_title = home_title
            out_dir = out_root
        else:
            page_title = f"{t['page_title'].format(n=page_num)} – {SITE['title']}"
            out_dir = out_root / "page" / str(page_num)

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page_html(
            page_title,
            page_body,
            lang=lang,
            base_path=base_path,
            is_home=(page_num == 1),
            body_class="layout--no-sidebar",
            extra_body_class="tg-archive-style--big-block",
            current=f"{base_path}/" if page_num == 1 else f"{base_path}/page/{page_num}/"
        ))

    # ===== /posts/ archive =====
    (out_root / "posts").mkdir(parents=True, exist_ok=True)
    from itertools import groupby
    all_cards_groups = []
    for year, year_group in groupby(posts, key=lambda p: p["date"].year):
        year_posts = list(year_group)
        year_suffix = f'<span class="timeline-sep">{t["year_suffix"]}</span>' if t["year_suffix"] else ""
        year_label = f'{year}{year_suffix}'
        month_sections = []
        for month, month_group in groupby(year_posts, key=lambda p: p["date"].month):
            month_posts = list(month_group)
            month_suffix = f'<span class="timeline-sep">{t["month_suffix"]}</span>' if t["month_suffix"] else ""
            import calendar
            if lang == "en":
                month_display = f'{calendar.month_name[month]}{month_suffix}'
            else:
                month_display = f'{month}{month_suffix}'
            cards_html = "\n".join(article_card(p, lang, base_path) for p in month_posts)
            month_sections.append('<div class="timeline-month-group collapsed"><h3 class="timeline-month-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + month_display + '<span class="toggle-icon">▼</span></h3>' + cards_html + '</div>')
        all_cards_groups.append('<div class="timeline-group collapsed"><h2 class="timeline-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + year_label + '<span class="toggle-icon">▼</span></h2>' + "".join(month_sections) + '</div>')
    all_cards = "\n".join(all_cards_groups) if posts else f'<p>{t.get("empty_posts", "No posts yet.")}</p>'
    archive = page_html(f"{t['post_list']} – {SITE['title']}",
        f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <header class="page-header"><h1 class="page-title">{t['post_list']}</h1></header>
            {all_cards}
          </main>
        </div>""",
        lang=lang, base_path=base_path,
        current=f"{base_path}/posts/",
        body_class="layout--no-sidebar")
    (out_root / "posts" / "index.html").write_text(archive)

    # ===== SINGLE POSTS =====
    for p in posts:
        body = article_single(p, posts, lang, base_path)
        side = sidebar_html(posts, lang, base_path)
        html = page_html(f"{p['title']} – {SITE['title']}",
            f'<div class="tg-flex-container tg-flex-space-between">{body}{side}</div>',
            desc=p["description"],
            lang=lang, base_path=base_path,
            body_class="layout--right-sidebar",
            sticky_title=p["title"])
        d = out_root / "posts" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)

    # ===== CATEGORIES =====
    cats = {}
    for p in posts:
        for c in p.get("categories", []):
            cats.setdefault(c, []).append(p)
    for cat_name, cat_posts in cats.items():
        slug = cat_name.lower().replace(" ", "-")
        d = out_root / "categories" / slug
        d.mkdir(parents=True, exist_ok=True)
        cat_cards = "\n".join(article_card(p, lang, base_path) for p in cat_posts)
        ph = f'<header class="page-header"><h1 class="page-title">{t["category"]}： <span>{cat_name}</span></h1></header>'
        (d / "index.html").write_text(page_html(
            f"{cat_name} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            {ph}
            {cat_cards}
          </main>
        </div>""",
            lang=lang, base_path=base_path,
            current=f"{base_path}/categories/{slug}/",
            body_class="layout--no-sidebar"))

    # ===== CATEGORIES INDEX =====
    cat_groups = []
    for cat_name, cat_posts in sorted(cats.items(), key=lambda x: -len(x[1])):
        cards = "\n".join(article_card(p, lang, base_path) for p in cat_posts)
        cat_groups.append('<div class="cat-index-group collapsed"><h2 class="cat-index-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + cat_name + ' <span class="cat-count">' + t["category_count"].format(n=len(cat_posts)) + '</span><span class="toggle-icon">▼</span></h2><div class="cat-index-articles">' + cards + '</div></div>')
    cats_index = page_html(f"{t['categories_widget']} – {SITE['title']}",
        f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <header class="page-header"><h1 class="page-title">{t['categories_widget']}</h1></header>
            {"".join(cat_groups) if cat_groups else '<p>' + t.get("empty_posts", "No posts yet.") + '</p>'}
          </main>
        </div>""",
        lang=lang, base_path=base_path,
        current=f"{base_path}/categories/",
        body_class="layout--no-sidebar")
    (out_root / "categories").mkdir(parents=True, exist_ok=True)
    (out_root / "categories" / "index.html").write_text(cats_index)

    # ===== ABOUT =====
    about = None
    try:
        about = parse_page(CONTENT / "about.md")
    except:
        pass
    if True:  # always build about page
        (out_root / "about").mkdir(parents=True, exist_ok=True)

        mainland_cities = TRAVEL_CITIES[0][2]
        international_cities = TRAVEL_CITIES[1][2]
        total_cities = len(mainland_cities) + len(international_cities)
        mainland_tags = "".join(f'<span class="travel-tag">{c}</span>' for c in mainland_cities)
        international_tags = "".join(f'<span class="travel-tag">{c}</span>' for c in international_cities)
        travel_cards = f"""<div class="travel-col">
              <div class="travel-col-title">{t['mainland_china']} <span class="travel-col-num">{len(mainland_cities)}</span></div>
              <div class="travel-tags">{mainland_tags}</div>
            </div>
            <div class="travel-col">
              <div class="travel-col-title">{t['international']} <span class="travel-col-num">{len(international_cities)}</span></div>
              <div class="travel-tags">{international_tags}</div>
            </div>"""

        focus_html = "".join(
            f'<div class="focus-item"><div class="focus-marker"><span class="focus-num">{i+1:02d}</span></div><div class="focus-body"><strong class="focus-text">{title}</strong><p class="focus-desc">{desc}</p></div></div>'
            for i, (title, desc) in enumerate(t["focus_items"])
        )

        skills = [
            ("skill_lang", "skill_lang_val", "☕"), ("skill_fw", "skill_fw_val", "⚙️"),
            ("skill_db", "skill_db_val", "🗄️"), ("skill_mq", "skill_mq_val", "📨"),
            ("skill_infra", "skill_infra_val", "🐳"), ("skill_ai", "skill_ai_val", "🤖"),
            ("skill_tools", "skill_tools_val", "🔧"),
        ]
        skill_cards = "".join(
            f'<div class="skill-card skill-card-feat"><span class="skill-icon">{icon}</span><span class="skill-label">{t[sk]}</span><span class="skill-value">{t[sv]}</span></div>'
            for sk, sv, icon in skills
        )

        about_name_html = t['about_name'] + (f'<span class="about-name-en">{t["about_name_sub"]}</span>' if t["about_name_sub"] else "")

        about_html = f"""
          <section class="about-intro">
            <div class="about-hero-decor">
              <span class="hero-blob hero-blob-1"></span>
              <span class="hero-blob hero-blob-2"></span>
              <span class="hero-blob hero-blob-3"></span>
            </div>
            <div class="about-intro-left">
              <img src="/avatar.jpg" alt="{t['about_hero_img_alt']}" class="about-avatar" width="80" height="80">
              <p class="about-greeting"><span class="greeting-dot"></span>{t['about_greeting']}</p>
              <h1 class="about-name">{about_name_html}</h1>
              <p class="about-bio">{t['about_bio']}</p>
              <div class="about-stats">
                <div class="about-stat"><strong>{len(posts)}</strong><span>{t['articles_count']}</span></div>
                <div class="about-stat"><strong>{len(cats)}</strong><span>{t['categories_count']}</span></div>
              </div>
            </div>
          </section>

          <section class="about-block">
            <h2 class="about-label">{t['about_skills']}</h2>
            <div class="skill-grid">
              {skill_cards}
            </div>
          </section>

          <section class="about-block">
            <h2 class="about-label">{t['about_focus']}</h2>
            <div class="focus-list">
              {focus_html}
            </div>
          </section>

          <section class="about-block">
            <h2 class="about-label">{t['about_projects']}</h2>
            <div class="project-card">
              <div class="project-header">
                <span class="project-emoji">🏛️</span>
                <div>
                  <strong class="project-name">Eastwood Auction</strong>
                  <span class="project-link"><a href="https://github.com/hankkyy/EastWood-Auction" target="_blank">GitHub ↗</a> · <a href="https://hankzhang.us/posts/client-side-visual-search/" target="_blank">{'Tech Article ↗' if lang == 'en' else '技术文章 ↗'}</a></span>
                </div>
              </div>
              <p class="project-desc">{t['project_eastwood_desc']}</p>
              <div class="project-tags"><span>TypeScript</span><span>Next.js</span><span>Supabase</span><span>CV</span><span>Canvas API</span></div>
            </div>

            <div class="project-card">
              <div class="project-header">
                <span class="project-emoji">✈️</span>
                <div>
                  <strong class="project-name">TREK — Trip Planner</strong>
                  <span class="project-link"><a href="https://github.com/hankkyy/TREK" target="_blank">GitHub ↗</a></span>
                </div>
              </div>
              <p class="project-desc">{t['project_trek_desc']}</p>
              <div class="project-tags"><span>TypeScript</span><span>Next.js</span><span>Supabase</span></div>
            </div>

            <div class="project-card">
              <div class="project-header">
                <span class="project-emoji">🤖</span>
                <div>
                  <strong class="project-name">RAG Customer Support Agent</strong>
                  <span class="project-link"><a href="https://github.com/hankkyy/RAG-Based-Customer-Support-Agent-for-Robot-Vacuum-Products" target="_blank">GitHub ↗</a></span>
                </div>
              </div>
              <p class="project-desc">{t['project_rag_desc']}</p>
              <div class="project-tags"><span>Python</span><span>LangChain</span><span>RAG</span><span>Chroma</span></div>
            </div>

            <div class="project-card">
              <div class="project-header">
                <span class="project-emoji">🖥️</span>
                <div>
                  <strong class="project-name">Hermes Desktop</strong>
                  <span class="project-link"><a href="https://github.com/hankkyy/hermes-desktop" target="_blank">GitHub ↗</a></span>
                </div>
              </div>
              <p class="project-desc">{t['project_hermes_desc']}</p>
              <div class="project-tags"><span>TypeScript</span><span>Electron</span><span>AI Agent</span></div>
            </div>
          </section>

          <section class="about-block">
            <h2 class="about-label">{t['about_hobby']}</h2>
            <div class="hobby-card">
              <p class="about-text">
                {t['hobby_text']}
              </p>
              <div class="travel-stats">
                <div class="travel-stat"><strong>319<span class="stat-unit">h</span>&thinsp;40<span class="stat-unit">min</span></strong><span>{t['flight_hours']}</span></div>
                <div class="travel-stat"><strong>238,719<span class="stat-unit">km</span></strong><span>{t['flight_km']}</span></div>
                <div class="travel-stat travel-stat-toggle" onclick="this.closest('.hobby-card').classList.toggle('expanded')"><strong>{total_cities}</strong><span>{t['cities_count_label']}<span class="toggle-arrow">▼</span></span></div>
              </div>
            <div class="travel-regions">
              {travel_cards}
            </div>
            </div>
          </section>

          <section class="about-block">
            <h2 class="about-label">{t['about_blog']}</h2>
            <div class="blog-about-card">
              <p class="about-text">
                {t['blog_about_text']}
              </p>
            </div>
          </section>

          <section class="about-block contact-block">
            <h2 class="about-label">{t['about_contact']}</h2>
            <div class="contact-links">
              <a href="https://github.com/hankkyy" target="_blank" class="contact-link"><img src="/github-logo.svg" alt="" class="contact-icon" width="20" height="20"> GitHub @hankkyy</a>
              <a href="https://www.linkedin.com/in/hankzhang-ky" target="_blank" class="contact-link"><svg class="contact-icon" width="18" height="18" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="3" fill="#0A66C2"/><text x="12" y="17" text-anchor="middle" fill="#fff" font-size="14" font-weight="700" font-family="sans-serif">in</text></svg> LinkedIn</a>
              <a href="mailto:hank.zihao@gmail.com" class="contact-link"><svg class="contact-icon" width="18" height="18" viewBox="0 0 24 24" fill="none"><rect width="24" height="24" rx="4" fill="#EA4335"/><path d="M4 6l8 6 8-6" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M20 6v12H4V6" stroke="#fff" stroke-width="2.2" fill="none"/></svg> hank.zihao@gmail.com</a>
            </div>
          </section>
        """
        about_title = about["title"] if about else t.get("about_title", "About")
        (out_root / "about" / "index.html").write_text(page_html(
            f"{about_title} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            {about_html}
          </main>
        </div>""",
            lang=lang, base_path=base_path,
            current=f"{base_path}/about/",
            body_class="layout--no-sidebar"))

    return len(cats)


def build():
    for item in ROOT.iterdir():
        if item.name in SAFE: continue
        if item.is_dir(): shutil.rmtree(item)
        else: item.unlink()

    CSS_DIR.mkdir(exist_ok=True)
    css_src = THEME / "static" / "css" / "style.css"
    if css_src.exists(): shutil.copy(css_src, CSS_DIR / "style.css")
    favicon_src = THEME / "static" / "favicon.png"
    if favicon_src.exists(): shutil.copy(favicon_src, ROOT / "favicon.png")
    gh_logo = THEME / "static" / "github-logo.svg"
    if gh_logo.exists(): shutil.copy(gh_logo, ROOT / "github-logo.svg")
    avatar_src = THEME / "static" / "avatar.jpg"
    if avatar_src.exists(): shutil.copy(avatar_src, ROOT / "avatar.jpg")

    images_dir = CONTENT / "images"
    if images_dir.exists():
        out_images = ROOT / "images"
        out_images.mkdir(exist_ok=True)
        for img in images_dir.iterdir():
            if img.is_file():
                shutil.copy(img, out_images / img.name)

    posts = []
    posts_dir = CONTENT / "posts"
    if posts_dir.exists():
        for f in posts_dir.glob("*.md"):
            posts.append(parse_page(f))
    posts.sort(key=lambda p: p["date"], reverse=True)

    # All posts appear on both language versions — only UI differs
    en_posts = posts
    zh_posts = posts

    en_cats = build_site("en", en_posts)
    zh_cats = build_site("zh", zh_posts)

    # ===== SITEMAP =====
    urls = [(SITE["url"], "daily")]
    for lang, base in [("en", ""), ("zh", "/zh")]:
        lp = en_posts if lang == "en" else zh_posts
        for p in lp:
            urls.append((f'{SITE["url"]}{base}/posts/{p["slug"]}/', "weekly"))
        lcats = {}
        for p in lp:
            for c in p.get("categories", []):
                lcats.setdefault(c, []).append(p)
        for cat_name in lcats:
            urls.append((f'{SITE["url"]}{base}/categories/{cat_name.lower().replace(" ", "-")}/', "weekly"))
        for page in ["posts/", "about/"]:
            urls.append((f'{SITE["url"]}{base}/{page}', "monthly"))
        urls.append((f'{SITE["url"]}{base}/', "daily"))

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, freq in urls:
        sitemap += f'  <url><loc>{url}</loc><changefreq>{freq}</changefreq></url>\n'
    sitemap += '</urlset>'
    (ROOT / "sitemap.xml").write_text(sitemap)

    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}sitemap.xml\n")

    print(f"✅ EN: {len(en_posts)} posts / ZH: {len(zh_posts)} posts")


if __name__ == "__main__":
    build()
