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

SITE = {"title":"纵横四海","url":"https://hankzhang.us/","desc":"但行好事，莫问前程"}
AUTHOR = "张子豪"
YEAR = str(datetime.now().year)
MENU = [("首页","/"),("文章列表","/posts/"),("留言板","/guestbook/"),("关于","/about/"),("GitHub","https://github.com/hankkyy")]
SAFE = {".git","src","vercel.json",".gitignore","README.md","pagefind"}


def menu_html(current="/"):
    parts = []
    for label, url in MENU:
        a = ' class="active"' if current == url else ""
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        parts.append(f'<li class="menu-item menu-item-type-custom menu-item-object-custom"><a href="{url}"{a}{ext}>{label}</a></li>')
    return "".join(parts)


def page_html(title_tag, body, *, current="/", desc="", is_home=False, body_class="layout--no-sidebar", extra_body_class=""):
    main_nav = menu_html(current)
    st = SITE["title"]
    site_title_tag = "h1" if is_home else "p"
    desc_meta = f'<meta name="description" content="{desc}">' if desc else ""
    pagefind_css = '<link rel="stylesheet" href="/pagefind/pagefind-ui.css">' if is_home else ""
    bc = f"{body_class} {extra_body_class}".strip()
    search_html = '<div id="search-inline" style="width:180px"></div>' if is_home else ""

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
  "@type": "{'Article' if not is_home and current != '/about/' and current != '/guestbook/' else 'WebSite'}",
  "headline": "{title_tag}",
  "description": "{desc or SITE['desc']}",
  "url": "{SITE['url']}{'' if current == '/' else current}",
  "datePublished": "2026-06-17",
  "author": {{ "@type": "Person", "name": "{AUTHOR}" }}
}}
</script>
<link rel="stylesheet" href="/css/style.css">
{pagefind_css}
</head>
<body class="{bc}">
<div id="page" class="site">
<a class="skip-link screen-reader-text" href="#content">跳到内容</a>
<header id="masthead" class="site-header tg-site-header tg-site-header--default">
  <div class="tg-header-top"><div class="container" style="display:flex;justify-content:center">{search_html}</div></div>
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
      <div class="container tg-flex-container tg-flex-space-between tg-flex-item-centered">
        <nav id="site-navigation" class="main-navigation tg-site-menu--default" style="flex:1;text-align:center">
          <div class="menu-menu-container"><ul id="primary-menu" class="nav-menu">{main_nav}</ul></div>
        </nav>
      </div>
    </div>
  </div>
</header>
<nav id="cenote-sticky-header" class="cenote-header-sticky">
  <div class="sticky-header-slide">
    <div class="cenote-reading-bar">
      <div class="container tg-flex-container tg-flex-item-centered"></div>
    </div>
    <div class="cenote-sticky-main">
      <div class="container tg-flex-container tg-flex-space-between tg-flex-item-centered">
        <nav class="main-navigation cenote-sticky-navigation tg-site-menu--default">
          <div class="menu-menu-container"><ul class="menu" style="justify-content:center">{main_nav}</ul></div>
        </nav>
      </div>
    </div>
  </div>
</nav>
<div id="content" class="site-content">
  <div class="container">
{body}
  </div>
</div>
{"<script src=\"/pagefind/pagefind-ui.js\"></script>\n<script>\n  new PagefindUI({ element: \"#search-inline\", showSubResults: false, showImages: false });\n</script>" if is_home else ""}
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
</div>
</body>
</html>"""


def parse_page(md_path):
    post = frontmatter.load(md_path)
    content_html = markdown(post.content, extensions=["extra", "codehilite"])
    plain = re.sub(r"<[^>]+>", "", content_html).strip()
    plain = re.sub(r"\s+", " ", plain)
    summary = plain[:55]
    truncated = len(plain) > 55
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
        "truncated": truncated,
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


def article_single(p, all_posts):
    idx = next((i for i, pp in enumerate(all_posts) if pp["slug"] == p["slug"]), None)
    prev_html = next_html = ""
    if idx is not None:
        if idx > 0:
            prev = all_posts[idx - 1]
            prev_html = f'<div class="nav-previous"><a href="/posts/{prev["slug"]}/" rel="prev"><span class="nav-links__label">上一篇文章</span> {prev["title"]}</a></div>'
        if idx < len(all_posts) - 1:
            nxt = all_posts[idx + 1]
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
                <p>后端开发工程师。关注 Java/Spring Boot/Redis/MySQL 传统技术栈，分布式系统，OLAP 数据库。</p>
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

    posts = []
    posts_dir = CONTENT / "posts"
    if posts_dir.exists():
        for f in posts_dir.glob("*.md"):
            posts.append(parse_page(f))
    # 按日期降序排列（最新的在前）
    posts.sort(key=lambda p: p["date"], reverse=True)

    home_title = f"{SITE['title']} – {SITE['desc']}"

    # ===== HOMEPAGE: first article full-width, rest grid =====
    first = article_card(posts[0]) if posts else ""
    rest = "\n".join(article_card(p) for p in posts[1:]) if len(posts) > 1 else ""
    home_body = f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <div class="tg-archive-featured">{first}</div>
            <div class="tg-archive-grid tg-archive-col--3">{rest}</div>
          </main>
        </div>"""
    homepage = page_html(home_title,
        home_body,
        is_home=True,
        body_class="layout--no-sidebar",
        extra_body_class="tg-archive-style--big-block")
    (ROOT / "index.html").write_text(homepage)

    # ===== /posts/ = 文章列表 (full archive, single column) =====
    (ROOT / "posts").mkdir(parents=True, exist_ok=True)
    all_cards = "\n".join(article_card(p) for p in posts)
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
            body_class="layout--right-sidebar")
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

    # ===== GUESTBOOK =====
    (ROOT / "guestbook").mkdir(parents=True, exist_ok=True)
    (ROOT / "guestbook" / "index.html").write_text(page_html(
        f"留言板 – {SITE['title']}",
        f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="page type-page status-publish hentry">
              <header class="entry-header"><h1 class="entry-title">留言板</h1></header>
              <div class="entry-content">
                <p>欢迎留言交流。</p>
              </div>
            </article>
            <div class="comments-area">
              <p class="no-comments">评论已关闭。</p>
            </div>
          </main>
        </div>""",
        current="/guestbook/",
        body_class="layout--no-sidebar"))

    # ===== ABOUT =====
    about_md = CONTENT / "about.md"
    if about_md.exists():
        about = parse_page(about_md)
        (ROOT / "about").mkdir(parents=True, exist_ok=True)
        (ROOT / "about" / "index.html").write_text(page_html(
            f"{about['title']} – {SITE['title']}",
            f"""<div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="page type-page status-publish hentry">
              <header class="entry-header"><h1 class="entry-title">{about['title']}</h1></header>
              <div class="entry-content">{about['content']}</div>
            </article>
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
    for page in ["posts/", "about/", "guestbook/"]:
        urls.append((f'{SITE["url"]}{page}', "monthly"))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, freq in urls:
        sitemap += f'  <url><loc>{url}</loc><changefreq>{freq}</changefreq></url>\n'
    sitemap += '</urlset>'
    (ROOT / "sitemap.xml").write_text(sitemap)

    # 生成 robots.txt
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}sitemap.xml\n")

    print(f"✅ 构建完成！{len(posts)} 篇文章，{len(cats)} 个分类")

    # 运行 Pagefind 生成搜索索引
    import subprocess
    try:
        result = subprocess.run(
            ["npx", "--yes", "pagefind", "--site", str(ROOT)],
            capture_output=True, text=True, timeout=60, cwd=str(ROOT)
        )
        if result.returncode == 0:
            print("✅ Pagefind 搜索索引已生成")
        else:
            print(f"⚠️ Pagefind: {result.stderr.strip()}")
    except Exception as e:
        print(f"⚠️ Pagefind 跳过: {e}")


if __name__ == "__main__":
    build()
