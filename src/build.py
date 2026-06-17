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

SITE = {"title":"纵横四海","url":"https://hankzhang.us/","desc":"「但行好事，莫问前程」"}
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
        travel_map = """
          <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
          <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
          <h3 style="margin-top:40px">✈️ 飞行日志</h3>
          <div id="travel-map" style="height:420px;border-radius:8px;margin:20px 0"></div>
          <script>
          var map = L.map('travel-map', {scrollWheelZoom: false}).setView([30, 110], 3);
          L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OSM contributors'
          }).addTo(map);

          var places = [
            // 美国
            {name:'哥伦布', lat:40.00, lng:-83.01},
            {name:'西雅图', lat:47.61, lng:-122.33},
            {name:'洛杉矶', lat:34.05, lng:-118.24},
            {name:'旧金山', lat:37.77, lng:-122.42},
            {name:'拉斯维加斯', lat:36.17, lng:-115.14},
            {name:'丹佛', lat:39.74, lng:-104.99},
            {name:'达拉斯', lat:32.78, lng:-96.80},
            {name:'休斯敦', lat:29.76, lng:-95.37},
            {name:'亚特兰大', lat:33.75, lng:-84.39},
            {name:'底特律', lat:42.33, lng:-83.05},
            {name:'波特兰', lat:45.52, lng:-122.68},
            {name:'圣安东尼奥', lat:29.42, lng:-98.49},
            {name:'坦帕', lat:27.95, lng:-82.46},
            {name:'劳德代尔堡', lat:26.12, lng:-80.14},
            {name:'里诺', lat:39.53, lng:-119.81},
            {name:'长滩', lat:33.77, lng:-118.19},
            {name:'伯克利', lat:37.87, lng:-122.27},
            {name:'奥克兰', lat:37.80, lng:-122.27},
            // 中国
            {name:'武汉', lat:30.59, lng:114.31},
            {name:'北京', lat:39.90, lng:116.41},
            {name:'上海', lat:31.23, lng:121.47},
            {name:'深圳', lat:22.54, lng:114.06},
            {name:'香港', lat:22.32, lng:114.17},
            {name:'厦门', lat:24.48, lng:118.09},
            {name:'三亚', lat:18.25, lng:109.51},
            {name:'桂林', lat:25.27, lng:110.29},
            {name:'太原', lat:37.87, lng:112.55},
            {name:'琼海', lat:19.25, lng:110.47},
            {name:'福州', lat:26.07, lng:119.30},
            {name:'南昌', lat:28.68, lng:115.86},
            {name:'宁波', lat:29.87, lng:121.55},
            {name:'南京', lat:32.06, lng:118.80},
            {name:'无锡', lat:31.49, lng:120.31},
            // 日本
            {name:'大阪', lat:34.69, lng:135.50},
            {name:'京都', lat:35.01, lng:135.77},
            {name:'神户', lat:34.69, lng:135.20},
            {name:'奈良', lat:34.69, lng:135.83},
            {name:'镰仓', lat:35.32, lng:139.55},
            // 韩国
            {name:'首尔', lat:37.57, lng:126.98},
          ];

          // Draw markers with glow effect
          places.forEach(function(p) {
            var marker = L.circleMarker([p.lat, p.lng], {
              radius: 5, fillColor: '#146bb7', color: '#fff', weight: 1.5,
              fillOpacity: 0.85
            }).addTo(map).bindPopup(p.name);
            marker.on('mouseover', function() { this.setRadius(8); });
            marker.on('mouseout', function() { this.setRadius(5); });
          });

          // Draw key flight routes
          var routes = [
            ['武汉','哥伦布'], ['哥伦布','旧金山'], ['旧金山','洛杉矶'],
            ['旧金山','西雅图'], ['哥伦布','纽约'], ['上海','大阪'],
            ['上海','首尔'], ['大阪','京都'],
          ];
          var lookup = {};
          places.forEach(function(p) { lookup[p.name] = p; });
          routes.forEach(function(r) {
            var a = lookup[r[0]], b = lookup[r[1]];
            if (!a || !b) return;
            var latlngs = [];
            var from = L.latLng(a.lat, a.lng);
            var to = L.latLng(b.lat, b.lng);
            var mid = L.latLng((a.lat+b.lat)/2+10, (a.lng+b.lng)/2);
            for (var t = 0; t <= 1; t += 0.02) {
              var la = (1-t)*(1-t)*from.lat + 2*(1-t)*t*mid.lat + t*t*to.lat;
              var ln = (1-t)*(1-t)*from.lng + 2*(1-t)*t*mid.lng + t*t*to.lng;
              latlngs.push([la, ln]);
            }
            L.polyline(latlngs, {
              color: '#146bb7', weight: 1.2, opacity: 0.35, dashArray: '4 6'
            }).addTo(map);
          });
          </script>
          <p style="text-align:center;color:#adb5bd;font-size:.85rem;margin-top:8px">拖拽地图查看航线</p>
        """
        (ROOT / "about" / "index.html").write_text(page_html(
            f"{about['title']} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="page type-page status-publish hentry">
              <header class="entry-header"><h1 class="entry-title">{about['title']}</h1></header>
              <div class="entry-content">{about['content']}</div>
            </article>
            {travel_map}
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
