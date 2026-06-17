#!/usr/bin/env python3
"""构建脚本 — 复刻 sinyalee.com/blog 的 HTML 结构"""

import re
from datetime import datetime
from pathlib import Path

import frontmatter
from markdown import markdown

SRC = Path(__file__).parent          # src/
ROOT = SRC.parent                    # myblog/
CONTENT = SRC / "content"
THEME = SRC / "themes" / "cenote-style"
CSS_DIR = ROOT / "css"

SITE_TITLE = "新的原野"
SITE_URL = "https://hankzhang.us/"
SITE_DESC = "一片新的原野，一个充满爱与善良的博客"
MENU_ITEMS = [("首页", "/"), ("关于", "/about/")]
CURRENT_YEAR = str(datetime.now().year)

SAFE = {".git", "src", "vercel.json", ".gitignore", "README.md"}


def nav_html(current_path="/"):
    """顶部导航 + 主导航 HTML"""
    parts_top = []
    parts_main = []
    for label, url in MENU_ITEMS:
        active = ' class="active"' if url == current_path else ""
        parts_top.append(f'<li><a href="{url}"{active}>{label}</a></li>')
        parts_main.append(f'<a href="{url}"{active}>{label}</a>')
    top = f'<ul>{"".join(parts_top)}</ul>'
    main = "\n          ".join(parts_main)
    return top, main


def build_html(title_tag, body_html, current_menu="/", description="", is_home=False):
    """组装完整 HTML 页面"""
    top_nav, main_nav = nav_html(current_menu)

    # 主页用 h1.site-title，内页用 p.site-title
    site_title_tag = "h1" if is_home else "p"

    header = f"""<header id="masthead" class="site-header">
  <div class="header-top">
    <div class="container">
      <nav>
        {top_nav}
      </nav>
    </div>
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
        <nav class="main-navigation">
          {main_nav}
        </nav>
      </div>
    </div>
  </div>
</header>"""

    footer = f"""<footer id="colophon" class="site-footer">
  <div class="container">
    <div class="site-info">
      Copyright &copy; {CURRENT_YEAR}
      <a href="{SITE_URL}" title="{SITE_TITLE}">{SITE_TITLE}</a>.
      All rights reserved.
    </div>
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
<body>
<div id="page" class="site">

{header}

  <div id="content" class="site-content">
    <div class="container">
      <div id="primary" class="content-area">
        <main id="main" class="site-main">
{body_html}
        </main>
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
    plain = re.sub(r"<[^>]+>", "", content_html).strip()
    summary = plain[:200]
    truncated = len(plain) > 200

    date = post.get("date", datetime.now())
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date)
        except ValueError:
            date = datetime.now()

    return {
        "title": post.get("title", "Untitled"),
        "date": date,
        "date_formatted": date.strftime("%Y年%m月%d日"),
        "date_iso": date.strftime("%Y-%m-%d"),
        "categories": post.get("categories", []),
        "description": post.get("description", ""),
        "content": content_html,
        "summary": summary,
        "truncated": truncated,
        "slug": md_path.stem,
    }


def entry_meta_cats(categories):
    """分类链接（首页 - 纯文字，蓝色，大写）"""
    if not categories:
        return ""
    parts = []
    for cat in categories:
        slug = cat.lower().replace(" ", "-")
        parts.append(f'<a href="/categories/{slug}/" rel="category">{cat}</a>')
    return f'<span class="cat-links">{"".join(parts)}</span>'


def entry_meta_posted_on(post):
    """发布日期（带 before 横线）"""
    return f"""<span class="posted-on">
              <a href="/posts/{post['slug']}/" rel="bookmark">
                <time class="entry-date published" datetime="{post['date_iso']}">{post['date_formatted']}</time>
              </a>
            </span>"""


def entry_byline():
    """作者行（单页）"""
    return f"""<span class="byline">
              <span class="author vcard">
                <a class="url fn n" href="/about/">Sinya</a>
              </span>
            </span>"""


def article_list_item(post):
    """首页文章条目"""
    meta = f"""{entry_meta_cats(post['categories'])}
            {entry_meta_posted_on(post)}"""

    return f"""          <article class="post type-post hentry">
            <div class="entry-meta">
              {meta}
            </div>
            <header class="entry-header">
              <h2 class="entry-title">
                <a href="/posts/{post['slug']}/" rel="bookmark">{post['title']}</a>
              </h2>
            </header>
            <div class="entry-content">
              <p>{post['summary']}{'&hellip;' if post['truncated'] else ''}</p>
            </div>
            <footer class="entry-footer">
              <a href="/posts/{post['slug']}/" class="read-more">阅读更多</a>
            </footer>
          </article>"""


def article_full(post):
    """文章详情页"""
    footer_cats = ""
    if post["categories"]:
        cats_html = "".join(
            f'<a href="/categories/{c.lower().replace(" ", "-")}/" rel="category">{c}</a>'
            for c in post["categories"]
        )
        footer_cats = f"""<span class="cat-links">分类： {cats_html}</span>"""

    return f"""          <article class="post type-post hentry">
            <div class="entry-meta">
              {entry_byline()}
              <span class="posted-on">
                <a href="/posts/{post['slug']}/" rel="bookmark">
                  <time class="entry-date published" datetime="{post['date_iso']}">{post['date_formatted']}</time>
                </a>
              </span>
            </div>
            <header class="entry-header">
              <h1 class="entry-title">{post['title']}</h1>
            </header>
            <div class="entry-content">
              {post['content']}
            </div>
            <footer class="entry-footer">
              {footer_cats}
            </footer>
          </article>"""


def clean_output():
    """安全清理输出目录"""
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

    # 复制 CSS
    CSS_DIR.mkdir(exist_ok=True)
    css_src = THEME / "static" / "css" / "style.css"
    if css_src.exists():
        import shutil
        shutil.copy(css_src, CSS_DIR / "style.css")

    # 读取文章
    posts_dir = CONTENT / "posts"
    posts = []
    if posts_dir.exists():
        for md_file in sorted(posts_dir.glob("*.md"), reverse=True):
            posts.append(parse_page(md_file))

    # 首页
    list_items = "\n".join(article_list_item(p) for p in posts)
    (ROOT / "index.html").write_text(
        build_html(SITE_TITLE, list_items, is_home=True)
    )

    # /posts/ 列表
    (ROOT / "posts").mkdir(parents=True, exist_ok=True)
    (ROOT / "posts" / "index.html").write_text(
        build_html(SITE_TITLE, list_items)
    )

    # 每篇文章
    for post in posts:
        body = article_full(post)
        page = build_html(
            f"{post['title']} – {SITE_TITLE}",
            body,
            description=post["description"],
        )
        post_dir = ROOT / "posts" / post["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(page)

    # 关于页
    about_md = CONTENT / "about.md"
    if about_md.exists():
        about = parse_page(about_md)
        body = f"""          <article class="page type-page hentry">
            <header class="entry-header">
              <h1 class="entry-title">{about['title']}</h1>
            </header>
            <div class="entry-content">
              {about['content']}
            </div>
          </article>"""
        page = build_html(
            f"{about['title']} – {SITE_TITLE}",
            body,
            current_menu="/about/",
        )
        (ROOT / "about").mkdir(parents=True, exist_ok=True)
        (ROOT / "about" / "index.html").write_text(page)

    print(f"✅ 构建完成！")


if __name__ == "__main__":
    build()
