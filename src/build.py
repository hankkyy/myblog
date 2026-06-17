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

SITE = {"title":"纵横四海","url":"https://hankzhang.us/","desc":"「保持好奇心，继续探索世界」"}
AUTHOR = "Zihao Zhang"
YEAR = str(datetime.now().year)
MENU = [("首页","/"),("文章列表","/posts/"),("分类","/categories/"),("关于","/about/")]
SAFE = {".git","src","vercel.json",".gitignore","README.md","pagefind"}


def menu_html(current="/"):
    parts = []
    for label, url in MENU:
        a = ' class="active"' if current == url else ""
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        parts.append(f'<li class="menu-item menu-item-type-custom menu-item-object-custom"><a href="{url}"{a}{ext}>{label}</a></li>')
    return "".join(parts)


def page_html(title_tag, body, *, current="/", desc="", is_home=False, body_class="layout--no-sidebar", extra_body_class="", sticky_title=""):
    main_nav = menu_html(current)
    st = SITE["title"]
    site_title_tag = "h1" if is_home else "p"
    desc_meta = f'<meta name="description" content="{desc}">' if desc else ""
    bc = f"{body_class} {extra_body_class}".strip()

    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_tag}</title>
<meta name="description" content="{desc or SITE['desc']}">
<meta property="og:title" content="{title_tag}">
<meta property="og:description" content="{desc or SITE['desc']}">
<meta property="og:type" content="{'website' if is_home else 'article'}">
<meta property="og:url" content="{SITE['url']}{'' if current == '/' else current}">
<meta name="twitter:card" content="summary">
<link rel="canonical" href="{SITE['url']}{'' if current == '/' else current}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{'Article' if not is_home and current != '/about/' else 'WebSite'}",
  "headline": "{title_tag}",
  "description": "{desc or SITE['desc']}",
  "url": "{SITE['url']}{'' if current == '/' else current}",
  "datePublished": "2026-06-17",
  "author": {{ "@type": "Person", "name": "{AUTHOR}" }}
}}
</script>
<link rel="stylesheet" href="/css/style.css">
<link rel="icon" type="image/png" href="/favicon.png">
</head>
<body class="{bc}">
<div id="page" class="site">
<a class="skip-link screen-reader-text" href="#content">跳到内容</a>
<header id="masthead" class="site-header tg-site-header tg-site-header--default">
  <div class="tg-header-top"></div>
  <div class="tg-header-bottom">
    <div class="header-bottom-top">
      <div class="container tg-flex-container tg-flex-space-between tg-flex-item-centered">
        <div class="site-branding">
          <{site_title_tag} class="site-title"><a href="{SITE['url']}" rel="home">{st}</a></{site_title_tag}>
          <p class="site-description">{SITE['desc']}</p>
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
        <span>Copyright &copy; {YEAR} <a href="{SITE['url']}" title="{st}"><span>{st}</span></a>. All rights reserved.</span>
        <nav style="display:flex;gap:15px">
          {"".join(f'<a href=\"{url}\"{(" target=\"_blank\" rel=\"noopener\"" if url.startswith("http") else "")}>{label}</a>' for label, url in MENU)}
        </nav>
      </div>
    </div>
  </div>
</footer>
<button id="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" style="position:fixed;bottom:30px;right:30px;width:44px;height:44px;border-radius:50%;background:#16181a;color:#fff;border:none;cursor:pointer;font-size:20px;display:none;z-index:999;box-shadow:0 2px 8px rgba(0,0,0,.2)">↑</button>
<script>
window.addEventListener('scroll',function(){{document.getElementById('back-to-top').style.display=window.scrollY>300?'block':'none';var s=document.getElementById('cenote-sticky-header');if(s)s.classList.toggle('visible',window.scrollY>200);}});
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
    return {
        "title": post.get("title", "Untitled"),
        "date": date,
        "date_fmt": f"{date.year}年{date.month}月{date.day}日",
        "date_iso": date.strftime("%Y-%m-%d"),
        "categories": post.get("categories", []),
        "description": post.get("description", ""),
        "content": content_html,
        "summary": summary,
        "long_summary": long_summary,
        "truncated": truncated,
        "long_truncated": long_truncated,
        "slug": md_path.stem,
    }


def cat_links_meta(cats):
    if not cats: return ""
    parts = []
    for i, c in enumerate(cats):
        slug = c.lower().replace(" ", "-")
        sep = '<span class="cat-seperator">, </span>' if i > 0 else ""
        parts.append(f'{sep}<a href="/categories/{slug}/" rel="category">{c}</a>')
    return "".join(parts)


def cat_links_footer(cats):
    if not cats: return ""
    links = "".join(f'<a href="/categories/{c.lower().replace(" ", "-")}/" rel="category">{c}</a>' for c in cats)
    return f'<span class="cat-links">分类： {links}</span>'


def posted_on(p):
    return f'<span class="posted-on"><a href="/posts/{p["slug"]}/" rel="bookmark"><time class="entry-date published" datetime="{p["date_iso"]}">{p["date_fmt"]}</time></a></span>'


def article_card(p):
    cats_html = cat_links_meta(p["categories"])
    return f"""<article id="post-{p['slug']}" class="post type-post status-publish format-standard hentry">
            <div class="entry-meta">
              <span class="cat-links">{cats_html}</span>{posted_on(p)}
            </div>
            <header class="entry-header">
              <h2 class="entry-title"><a href="/posts/{p['slug']}/" rel="bookmark">{p['title']}</a></h2>
            </header>
            <div class="entry-content">
              <p>{p['summary']}{' [&hellip;]' if p['truncated'] else ''}</p>
            </div>
            <footer class="entry-footer">
              <a href="/posts/{p['slug']}/" class="tg-readmore-link">阅读更多</a>
            </footer>
          </article>"""

def featured_card(p):
    cats_html = cat_links_meta(p["categories"])
    return f"""<article id="post-{p['slug']}" class="post type-post status-publish format-standard hentry">
            <div class="entry-meta">
              <span class="cat-links">{cats_html}</span>{posted_on(p)}
            </div>
            <header class="entry-header">
              <h2 class="entry-title"><a href="/posts/{p['slug']}/" rel="bookmark">{p['title']}</a></h2>
            </header>
            <div class="entry-content">
              <p>{p['long_summary']}{' [&hellip;]' if p['long_truncated'] else ''}</p>
            </div>
            <footer class="entry-footer">
              <a href="/posts/{p['slug']}/" class="tg-readmore-link">阅读更多</a>
            </footer>
          </article>"""


def article_single(p, all_posts):
    idx = next((i for i, pp in enumerate(all_posts) if pp["slug"] == p["slug"]), None)
    prev_html = next_html = ""
    if idx is not None:
        if idx < len(all_posts) - 1:
            prev = all_posts[idx + 1]
            prev_html = f'<div class="nav-previous"><a href="/posts/{prev["slug"]}/" rel="prev"><span class="nav-links__label">上一篇文章</span> {prev["title"]}</a></div>'
        if idx > 0:
            nxt = all_posts[idx - 1]
            next_html = f'<div class="nav-next"><a href="/posts/{nxt["slug"]}/" rel="next"><span class="nav-links__label">下一篇文章</span> {nxt["title"]}</a></div>'
    nav = ""
    if prev_html or next_html:
        nav = f"""<nav class="navigation post-navigation" aria-label="文章">
            <h2 class="screen-reader-text">文章导航</h2>
            <div class="nav-links">{prev_html}{next_html}</div>
          </nav>"""

    return f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="post type-post status-publish format-standard hentry">
              <div class="entry-meta">
                <span class="byline"><span class="author vcard"><a class="url fn n" href="/about/">{AUTHOR}</a></span></span>{posted_on(p)}
              </div>
              <header class="entry-header">
                <h1 class="entry-title">{p['title']}</h1>
              </header>
              <div class="entry-content">{p['content']}</div>
              <footer class="entry-footer">{cat_links_footer(p['categories'])}</footer>
            </article>
            {nav}
            <div class="author-bio">
              <div class="author-bio-content">
                <h3>关于 {AUTHOR}</h3>
                <p>后端开发工程师。关注 Java/Spring Boot/Redis/MySQL 技术栈，分布式系统，OLAP 数据库，AI Agent 开发与应用。</p>
              </div>
            </div>
            <div class="comments-area">
              <h3>评论</h3>
              <p class="no-comments">评论已关闭。</p>
            </div>
          </main>
        </div>"""


def sidebar_html(posts):
    recent = "".join(f'<li><a href="/posts/{p["slug"]}/">{p["title"]}</a></li>' for p in posts[:5])
    cats_set = sorted({c for p in posts for c in p.get("categories", [])})
    tags = "".join(f'<a href="/categories/{c.lower().replace(" ", "-")}/">{c}</a>' for c in cats_set)
    return f"""<aside id="secondary" class="widget-area">
          <section class="widget widget_recent_entries">
            <h2 class="widget-title">近期文章</h2>
            <ul>{recent}</ul>
          </section>
          <section class="widget widget_tag_cloud">
            <h2 class="widget-title">分类</h2>
            <div class="tagcloud">{tags}</div>
          </section>
        </aside>"""


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

    posts = []
    posts_dir = CONTENT / "posts"
    if posts_dir.exists():
        for f in posts_dir.glob("*.md"):
            posts.append(parse_page(f))
    # 按日期降序排列（最新的在前）
    posts.sort(key=lambda p: p["date"], reverse=True)

    home_title = f"{SITE['title']} – {SITE['desc']}"

    # ===== HOMEPAGE with pagination: 10 per page, first full-width, rest 3-col grid =====
    PER_PAGE = 10
    total_pages = (len(posts) + PER_PAGE - 1) // PER_PAGE

    def pagination_html(current_page):
        if total_pages <= 1:
            return ""
        # Show up to 6 page numbers: always first, last, and pages around current
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
                href = "/" if pg == 1 else f"/page/{pg}/"
                blocks.append(f'<a class="page-numbers" href="{href}">{pg}</a>')
            prev = pg
        jump_input = f'<span class="page-jump">'
        jump_input += f'<input type="number" min="1" max="{total_pages}" placeholder="跳转" id="jump-input-{current_page}" style="width:56px;text-align:center;border:1px solid #dee2e6;border-right:none;border-radius:4px 0 0 4px;padding:5px 2px;font-size:.85rem;line-height:1.4;outline:none;color:#363b40;transition:border-color .2s" onfocus="this.style.borderColor=&#39;#146bb7&#39;" onblur="this.style.borderColor=&#39;#dee2e6&#39;">'
        jump_input += f'<button onclick="var v=parseInt(document.getElementById(&quot;jump-input-{current_page}&quot;).value);if(v>=1&&v<={total_pages})location.href=v===1?&quot;/&quot;:&quot;/page/&quot;+v+&quot;/&quot;" style="border:1px solid #dee2e6;border-left:none;border-radius:0 4px 4px 0;padding:6px 10px;cursor:pointer;background:#f8f9fa;color:#495057;font-size:.85rem;transition:all .2s" onmouseover="this.style.background=&#39;#146bb7&#39;;this.style.color=&#39;#fff&#39;;this.style.borderColor=&#39;#146bb7&#39;" onmouseout="this.style.background=&#39;#f8f9fa&#39;;this.style.color=&#39;#495057&#39;;this.style.borderColor=&#39;#dee2e6&#39;">→</button>'
        jump_input += '</span>'
        return f'<nav class="navigation pagination" aria-label="文章分页"><div class="nav-links">{"".join(blocks)}{jump_input}</div></nav>'

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * PER_PAGE
        end = start + PER_PAGE
        page_posts = posts[start:end]

        first_card = featured_card(page_posts[0]) if page_posts else ""
        rest_cards = "\n".join(article_card(p) for p in page_posts[1:]) if len(page_posts) > 1 else ""
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
            out_dir = ROOT
        else:
            page_title = f"第{page_num}页 – {SITE['title']}"
            out_dir = ROOT / "page" / str(page_num)

        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page_html(
            page_title,
            page_body,
            is_home=(page_num == 1),
            body_class="layout--no-sidebar",
            extra_body_class="tg-archive-style--big-block",
            current="/" if page_num == 1 else f"/page/{page_num}/"
        ))

    # ===== /posts/ = 文章列表 with timeline =====
    (ROOT / "posts").mkdir(parents=True, exist_ok=True)
    all_cards_groups = []
    from itertools import groupby
    # Group by year, then by month within each year
    for year, year_group in groupby(posts, key=lambda p: p["date"].year):
        year_posts = list(year_group)
        year_label = f'{year}<span class="timeline-sep">年</span>'
        month_sections = []
        for month, month_group in groupby(year_posts, key=lambda p: p["date"].month):
            month_posts = list(month_group)
            month_label = f'{month}<span class="timeline-sep">月</span>'
            cards_html = "\n".join(article_card(p) for p in month_posts)
            month_sections.append('<div class="timeline-month-group collapsed"><h3 class="timeline-month-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + month_label + '<span class="toggle-icon">▼</span></h3>' + cards_html + '</div>')
        all_cards_groups.append('<div class="timeline-group collapsed"><h2 class="timeline-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + year_label + '<span class="toggle-icon">▼</span></h2>' + "".join(month_sections) + '</div>')
    all_cards = "\n".join(all_cards_groups)
    archive = page_html(f"文章列表 – {SITE['title']}",
        f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <header class="page-header"><h1 class="page-title">文章列表</h1></header>
            {all_cards}
          </main>
        </div>""",
        current="/posts/",
        body_class="layout--no-sidebar")
    (ROOT / "posts" / "index.html").write_text(archive)

    # ===== SINGLE POSTS =====
    for p in posts:
        body = article_single(p, posts)
        side = sidebar_html(posts)
        html = page_html(f"{p['title']} – {SITE['title']}",
            f'<div class="tg-flex-container tg-flex-space-between">{body}{side}</div>',
            desc=p["description"],
            body_class="layout--right-sidebar",
            sticky_title=p["title"])
        d = ROOT / "posts" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)

    # ===== CATEGORIES =====
    cats = {}
    for p in posts:
        for c in p.get("categories", []):
            cats.setdefault(c, []).append(p)
    for cat_name, cat_posts in cats.items():
        slug = cat_name.lower().replace(" ", "-")
        d = ROOT / "categories" / slug
        d.mkdir(parents=True, exist_ok=True)
        cat_cards = "\n".join(article_card(p) for p in cat_posts)
        ph = f'<header class="page-header"><h1 class="page-title">分类： <span>{cat_name}</span></h1></header>'
        (d / "index.html").write_text(page_html(
            f"{cat_name} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            {ph}
            {cat_cards}
          </main>
        </div>""",
            current=f"/categories/{slug}/",
            body_class="layout--no-sidebar"))

    # ===== CATEGORIES INDEX =====
    cat_groups = []
    for cat_name, cat_posts in sorted(cats.items(), key=lambda x: -len(x[1])):
        slug = cat_name.lower().replace(" ", "-")
        cards = "\n".join(article_card(p) for p in cat_posts)
        cat_groups.append('<div class="cat-index-group collapsed"><h2 class="cat-index-heading collapsed" onclick="this.parentElement.classList.toggle(\'collapsed\');this.classList.toggle(\'collapsed\')">' + cat_name + ' <span class="cat-count">（' + str(len(cat_posts)) + ' 篇）</span><span class="toggle-icon">▼</span></h2><div class="cat-index-articles">' + cards + '</div></div>')
    cats_index = page_html(f"分类 – {SITE['title']}",
        f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <header class="page-header"><h1 class="page-title">分类</h1></header>
            {"".join(cat_groups)}
          </main>
        </div>""",
        current="/categories/",
        body_class="layout--no-sidebar")
    (ROOT / "categories" / "index.html").write_text(cats_index)

    # ===== ABOUT =====
    about_md = CONTENT / "about.md"
    if about_md.exists():
        about = parse_page(about_md)
        (ROOT / "about").mkdir(parents=True, exist_ok=True)
        about_html = f"""
          <div class="about-hero" style="text-align:center;padding:40px 0 20px">
            <h1 class="about-name">张子豪 · Hank Zhang</h1>
            <p class="about-tagline" style="font-size:1.1rem;color:#6c757d;margin-top:8px">后端开发 · 数据基础设施 · AI Agent</p>
          </div>

          <div class="about-divider"></div>

          <div class="about-section">
            <h2 class="about-h2"><span class="about-icon">🧰</span> 技术栈</h2>
            <div class="skill-grid">
              <div class="skill-card"><span class="skill-label">语言</span><span class="skill-value">Java · Python · SQL</span></div>
              <div class="skill-card"><span class="skill-label">框架</span><span class="skill-value">Spring Boot · Spring MVC · MyBatis · LangChain</span></div>
              <div class="skill-card"><span class="skill-label">数据库</span><span class="skill-value">MySQL · Redis · Apache Doris</span></div>
              <div class="skill-card"><span class="skill-label">中间件</span><span class="skill-value">Kafka · Flink</span></div>
              <div class="skill-card"><span class="skill-label">基础设施</span><span class="skill-value">Docker · Kubernetes · Nginx</span></div>
              <div class="skill-card"><span class="skill-label">AI / Agent</span><span class="skill-value">RAG · Chroma · Prompt Engineering · MCP</span></div>
              <div class="skill-card"><span class="skill-label">工具</span><span class="skill-value">Git · Linux · PySpark</span></div>
            </div>
          </div>

          <div class="about-section">
            <h2 class="about-h2"><span class="about-icon">🎯</span> 关注方向</h2>
            <div class="focus-list">
              <div class="focus-item"><span class="focus-dot"></span> 分布式系统与微服务架构</div>
              <div class="focus-item"><span class="focus-dot"></span> OLAP 数据库与实时数仓</div>
              <div class="focus-item"><span class="focus-dot"></span> AI Agent 开发与应用</div>
              <div class="focus-item"><span class="focus-dot"></span> 后端性能优化</div>
            </div>
          </div>

          <div class="about-section">
            <h2 class="about-h2"><span class="about-icon">✈️</span> 兴趣爱好</h2>
            <p style="color:#495057;line-height:1.9;font-size:.95rem">
              热爱旅行和航空。喜欢靠窗的座位，起飞时引擎轰鸣的那一刻是旅途中最享受的瞬间。<br>
              相信眼界决定世界——去更多地方，见更多人，理解更多事。
            </p>
          </div>

          <div class="about-section">
            <h2 class="about-h2"><span class="about-icon">📝</span> 关于这个博客</h2>
            <p style="color:#495057;line-height:1.9;font-size:.95rem">
              用 Python 构建的静态站点，部署在 Vercel。外观参考 WordPress Cenote 主题。<br>
              写技术笔记、项目复盘、行业观察。不追求日更，追求每篇都值得读。
            </p>
          </div>

          <div class="about-section contact-section" style="background:#f8f9fa;border-radius:12px;padding:32px;margin-top:40px">
            <h2 class="about-h2" style="margin-top:0"><span class="about-icon">📬</span> 欢迎交流</h2>
            <div class="contact-links">
              <a href="https://github.com/hankkyy" target="_blank" class="contact-link">
                <span class="contact-icon">🐙</span> GitHub @hankkyy
              </a>
              <a href="mailto:hank.zihao@gmail.com" class="contact-link">
                <span class="contact-icon">📧</span> hank.zihao@gmail.com
              </a>
            </div>
            <p style="color:#adb5bd;font-size:.85rem;margin-top:16px">或者直接在本页面留言</p>
          </div>
        """
        (ROOT / "about" / "index.html").write_text(page_html(
            f"{about['title']} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            {about_html}
          </main>
        </div>""",
            current="/about/",
            body_class="layout--no-sidebar"))

    # 生成 sitemap.xml
    urls = [(SITE["url"], "daily")]
    for p in posts:
        urls.append((f'{SITE["url"]}posts/{p["slug"]}/', "weekly"))
    for cat_name in cats:
        urls.append((f'{SITE["url"]}categories/{cat_name.lower().replace(" ", "-")}/', "weekly"))
    for page in ["posts/", "about/"]:
        urls.append((f'{SITE["url"]}{page}', "monthly"))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, freq in urls:
        sitemap += f'  <url><loc>{url}</loc><changefreq>{freq}</changefreq></url>\n'
    sitemap += '</urlset>'
    (ROOT / "sitemap.xml").write_text(sitemap)

    # 生成 robots.txt
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}sitemap.xml\n")

    print(f"✅ 构建完成！{len(posts)} 篇文章，{len(cats)} 个分类")


if __name__ == "__main__":
    build()
