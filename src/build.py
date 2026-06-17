#!/usr/bin/env python3
"""构建脚本 — 完整复刻 sinyalee.com/blog 布局"""

import re
from datetime import datetime
from pathlib import Path

import frontmatter
from markdown import markdown

SRC = Path(__file__).parent
ROOT = SRC.parent
CONTENT = SRC / "content"
THEME = SRC / "themes" / "cenote-style"
CSS_DIR = ROOT / "css"

SITE_TITLE = "新的原野"
SITE_URL = "https://hankzhang.us/"
SITE_DESC = "一片新的原野，一个充满爱与善良的博客"
MENU_ITEMS = [("首页", "/"), ("技术", "/categories/技术/"), ("杂谈", "/categories/杂谈/"), ("关于", "/about/")]
CURRENT_YEAR = str(datetime.now().year)
AUTHOR = "张子豪"

SAFE = {".git", "src", "vercel.json", ".gitignore", "README.md"}


def nav_html(current_path="/"):
    top_parts = []
    main_parts = []
    for label, url in MENU_ITEMS:
        active = ' class="active"' if current_path.startswith(url) and url != "/" else ""
        if url == "/" and current_path == "/":
            active = ' class="active"'
        top_parts.append(f'<li><a href="{url}"{active}>{label}</a></li>')
        main_parts.append(f'<a href="{url}"{active}>{label}</a>')
    return "<ul>" + "".join(top_parts) + "</ul>", "\n          ".join(main_parts)


def sidebar_html(posts):
    """侧边栏：推荐文章 + 分类标签"""
    recent = ""
    for p in posts[:5]:
        recent += f'<li><a href="/posts/{p["slug"]}/">{p["title"]}</a></li>\n'

    cats = set()
    for p in posts:
        for c in p.get("categories", []):
            cats.add(c)

    tag_html = ""
    for c in sorted(cats):
        slug = c.lower().replace(" ", "-")
        tag_html += f'<a href="/categories/{slug}/">{c}</a>\n'

    return f"""          <aside id="secondary" class="widget-area">
            <section class="widget widget_recent_entries">
              <h2 class="widget-title">近期文章</h2>
              <ul>
                {recent}              </ul>
            </section>
            <section class="widget widget_tag_cloud">
              <h2 class="widget-title">分类</h2>
              <div class="tagcloud">
                {tag_html}              </div>
            </section>
          </aside>"""


def build_html(title_tag, body_html, current_menu="/", description="", is_home=False, posts=None, body_class="layout--no-sidebar"):
    top_nav, main_nav = nav_html(current_menu)
    site_title_tag = "h1" if is_home else "p"

    sidebar = ""
    if posts and "right-sidebar" in body_class:
        sidebar = sidebar_html(posts)

    header = f"""<header id="masthead" class="site-header">
  <div class="header-top">
    <div class="container"><nav>{top_nav}</nav></div>
  </div>
  <div class="header-bottom">
    <div class="header-bottom-top">
      <div class="container">
        <div class="site-branding">
          <{site_title_tag} class="site-title"><a href="{SITE_URL}" rel="home">{SITE_TITLE}</a></{site_title_tag}>
          <p class="site-description">{SITE_DESC}</p>
        </div>
      </div>
    </div>
    <div class="header-bottom-bottom">
      <div class="container">
        <nav class="main-navigation">{main_nav}</nav>
      </div>
    </div>
  </div>
</header>"""

    footer = f"""<footer id="colophon" class="site-footer">
  <div class="container">
    <div class="site-info">Copyright &copy; {CURRENT_YEAR} <a href="{SITE_URL}">{SITE_TITLE}</a>. All rights reserved.</div>
  </div>
</footer>"""

    desc_meta = f'<meta name="description" content="{description}">' if description else ""

    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_tag}</title>
  <link rel="stylesheet" href="/css/style.css">
  {desc_meta}
</head>
<body class="{body_class}">
<div id="page" class="site">

{header}

  <div id="content" class="site-content">
    <div class="container">
      <div class="tg-flex-container tg-flex-space-between">
{body_html}
{sidebar}
      </div>
    </div>
  </div>

{footer}

</div>
</body>
</html>"""


def parse_page(md_path):
    post = frontmatter.load(md_path)
    content_html = markdown(post.content, extensions=["extra", "codehilite"])
    summary_html = content_html[:300]
    if len(content_html) > 300:
        lt = summary_html.rfind('<')
        gt = summary_html.rfind('>')
        if lt > gt:
            summary_html = summary_html[:lt]
    truncated = len(content_html) > 300

    date = post.get("date", datetime.now())
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            date = datetime.now()

    # 日期格式：2026年6月17日（无前导零，和原版一致）
    month = date.month
    day = date.day
    date_formatted = f"{date.year}年{month}月{day}日"

    return {
        "title": post.get("title", "Untitled"),
        "date": date,
        "date_formatted": date_formatted,
        "date_iso": date.strftime("%Y-%m-%d"),
        "categories": post.get("categories", []),
        "description": post.get("description", ""),
        "content": content_html,
        "summary": summary_html,
        "truncated": truncated,
        "slug": md_path.stem,
    }


def cat_links(categories, in_footer=False):
    if not categories:
        return ""
    if in_footer:
        links = "".join(f'<a href="/categories/{c.lower().replace(" ", "-")}/" rel="category">{c}</a>' for c in categories)
        return f'<span class="cat-links">分类： {links}</span>'
    links = "".join(f'<a href="/categories/{c.lower().replace(" ", "-")}/" rel="category">{c}</a>' for c in categories)
    return f'<span class="cat-links">{links}</span>'


def posted_on(post):
    return f'<span class="posted-on"><a href="/posts/{post["slug"]}/" rel="bookmark"><time class="entry-date published" datetime="{post["date_iso"]}">{post["date_formatted"]}</time></a></span>'


def article_list_item(post):
    return f"""          <article class="post type-post hentry">
            <div class="entry-meta">
              {cat_links(post['categories'])}{posted_on(post)}
            </div>
            <header class="entry-header">
              <h2 class="entry-title"><a href="/posts/{post['slug']}/" rel="bookmark">{post['title']}</a></h2>
            </header>
            <div class="entry-content">
              {post['summary']}{'&hellip;' if post['truncated'] else ''}
            </div>
            <footer class="entry-footer">
              <a href="/posts/{post['slug']}/" class="read-more">阅读更多</a>
            </footer>
          </article>"""


def article_full(post, all_posts):
    # Post navigation
    idx = None
    for i, p in enumerate(all_posts):
        if p["slug"] == post["slug"]:
            idx = i
            break

    prev_html = ""
    next_html = ""
    if idx is not None:
        if idx > 0:
            prev_post = all_posts[idx - 1]
            prev_html = f"""<div class="nav-previous">
            <a href="/posts/{prev_post['slug']}/" rel="prev">
              <span class="nav-links__label">上一篇文章</span>
              {prev_post['title']}
            </a>
          </div>"""
        if idx < len(all_posts) - 1:
            next_post = all_posts[idx + 1]
            next_html = f"""<div class="nav-next">
            <a href="/posts/{next_post['slug']}/" rel="next">
              <span class="nav-links__label">下一篇文章</span>
              {next_post['title']}
            </a>
          </div>"""

    nav = ""
    if prev_html or next_html:
        nav = f"""          <nav class="navigation post-navigation">
            <h2 class="screen-reader-text">文章导航</h2>
            <div class="nav-links">
              {prev_html}
              {next_html}
            </div>
          </nav>"""

    return f"""        <div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="post type-post hentry single">
              <div class="entry-meta">
                <span class="byline"><span class="author vcard"><a class="url fn n" href="/about/">{AUTHOR}</a></span></span><span class="posted-on"><a href="/posts/{post['slug']}/" rel="bookmark"><time class="entry-date published" datetime="{post['date_iso']}">{post['date_formatted']}</time></a></span>
              </div>
              <header class="entry-header">
                <h1 class="entry-title">{post['title']}</h1>
              </header>
              <div class="entry-content">
                {post['content']}
              </div>
              <footer class="entry-footer">
                {cat_links(post['categories'], in_footer=True)}
              </footer>
            </article>
            {nav}
          </main>
        </div>"""


def list_page(posts, title_tag, current_menu="/", page_header=""):
    items = "\n".join(article_list_item(p) for p in posts)
    body = f"""        <div id="primary" class="content-area">
          <main id="main" class="site-main">
            {page_header}
            {items}
          </main>
        </div>"""
    return build_html(title_tag, body, current_menu=current_menu, is_home=(current_menu == "/"))


def category_page(posts, category_name, category_slug):
    page_header = f"""            <header class="page-header">
              <h1 class="page-title">分类： <span>{category_name}</span></h1>
            </header>"""
    items = "\n".join(article_list_item(p) for p in posts)
    body = f"""        <div id="primary" class="content-area">
          <main id="main" class="site-main">
            {page_header}
            {items}
          </main>
        </div>"""
    return build_html(f"{category_name} – {SITE_TITLE}", body, current_menu=f"/categories/{category_slug}/")


def clean_output():
    import shutil
    for item in ROOT.iterdir():
        if item.name in SAFE:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def build():
    clean_output()

    import shutil
    CSS_DIR.mkdir(exist_ok=True)
    css_src = THEME / "static" / "css" / "style.css"
    if css_src.exists():
        shutil.copy(css_src, CSS_DIR / "style.css")

    # Read all posts
    posts_dir = CONTENT / "posts"
    posts = []
    if posts_dir.exists():
        for md_file in sorted(posts_dir.glob("*.md"), reverse=True):
            posts.append(parse_page(md_file))

    HOME_TITLE = f"{SITE_TITLE} – {SITE_DESC}"

    # ======= HOMEPAGE =======
    (ROOT / "index.html").write_text(list_page(posts[:10], HOME_TITLE))

    # /posts/ list
    (ROOT / "posts").mkdir(parents=True, exist_ok=True)
    (ROOT / "posts" / "index.html").write_text(list_page(posts[:10], SITE_TITLE))

    # ======= SINGLE POST PAGES =======
    for post in posts:
        body = article_full(post, posts)
        page = build_html(
            f"{post['title']} – {SITE_TITLE}",
            body,
            description=post["description"],
            posts=posts,
            body_class="layout--right-sidebar",
        )
        post_dir = ROOT / "posts" / post["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(page)

    # ======= CATEGORY PAGES =======
    cats = {}
    for p in posts:
        for c in p.get("categories", []):
            cats.setdefault(c, []).append(p)

    for cat_name, cat_posts in cats.items():
        cat_slug = cat_name.lower().replace(" ", "-")
        cat_dir = ROOT / "categories" / cat_slug
        cat_dir.mkdir(parents=True, exist_ok=True)
        (cat_dir / "index.html").write_text(
            category_page(cat_posts, cat_name, cat_slug)
        )

    # ======= ABOUT PAGE =======
    about_md = CONTENT / "about.md"
    if about_md.exists():
        about = parse_page(about_md)
        body = f"""        <div id="primary" class="content-area">
          <main id="main" class="site-main">
            <article class="page type-page hentry">
              <header class="entry-header">
                <h1 class="entry-title">{about['title']}</h1>
              </header>
              <div class="entry-content">{about['content']}</div>
            </article>
          </main>
        </div>"""
        page = build_html(f"{about['title']} – {SITE_TITLE}", body, current_menu="/about/")
        (ROOT / "about").mkdir(parents=True, exist_ok=True)
        (ROOT / "about" / "index.html").write_text(page)

    print(f"✅ 构建完成！{len(posts)} 篇文章, {len(cats)} 个分类")


if __name__ == "__main__":
    build()
