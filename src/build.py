#!/usr/bin/env python3
"""构建脚本 — 把 src/content/ 中的 Markdown → 项目根目录的 HTML"""

import re
from datetime import datetime
from pathlib import Path

import frontmatter
from markdown import markdown

SRC = Path(__file__).parent          # src/
ROOT = SRC.parent                    # myblog/ 项目根
CONTENT = SRC / "content"
THEME = SRC / "themes" / "cenote-style"
CSS_DIR = ROOT / "css"

SITE_TITLE = "新的原野"
SITE_URL = "https://hankzhang.us/"
SITE_DESC = "一片新的原野，一个充满爱与善良的博客"
MENU_ITEMS = [("首页", "/"), ("关于", "/about/")]
CURRENT_YEAR = str(datetime.now().year)

# 不会被清理的安全目录/文件
SAFE = {".git", "src", "vercel.json", ".gitignore", "README.md"}


def make_menu_html(current_path="/"):
    parts = []
    for label, url in MENU_ITEMS:
        active = ' class="active"' if url == current_path else ""
        parts.append(f'        <a href="{url}"{active}>{label}</a>')
    return "\n".join(parts)


def make_cat_links(categories):
    if not categories:
        return ""
    parts = ['      <span class="cat-links">']
    for cat in categories:
        slug = cat.lower().replace(" ", "-")
        parts.append(f'        <a href="/categories/{slug}/">{cat}</a>')
    parts.append("      </span>")
    return "\n".join(parts)


def build_html(title_tag, body_html, output_path, current_menu="/", description=""):
    header = f"""<header class="site-header">
  <div class="header-top">
    <div class="container">
      <nav>
{make_menu_html(current_menu)}
      </nav>
      <div></div>
    </div>
  </div>
  <div class="header-bottom">
    <div class="header-bottom-top">
      <div class="container">
        <div class="site-branding">
          <h1 class="site-title"><a href="{SITE_URL}">{SITE_TITLE}</a></h1>
          <p class="site-description">{SITE_DESC}</p>
        </div>
      </div>
    </div>
  </div>
  <div class="header-bottom-bottom">
    <div class="container">
      <nav class="main-navigation">
{make_menu_html(current_menu)}
      </nav>
    </div>
  </div>
</header>"""

    footer = f"""<footer class="site-footer">
  <div class="container">
    Copyright &copy; {CURRENT_YEAR}
    <a href="{SITE_URL}">{SITE_TITLE}</a>.
    All rights reserved.
    Powered by <a href="https://gohugo.io">Hugo</a>.
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
{header}

  <div class="site-content">
    <div class="container">
{body_html}
    </div>
  </div>

{footer}
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


def article_list_item(post):
    return f"""      <article>
        <div class="entry-meta">
{make_cat_links(post['categories'])}
          <span class="posted-on">
            <a href="/posts/{post['slug']}/">
              <time datetime="{post['date_iso']}">{post['date_formatted']}</time>
            </a>
          </span>
        </div>
        <header class="entry-header">
          <h2 class="entry-title">
            <a href="/posts/{post['slug']}/">{post['title']}</a>
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
    return f"""      <main class="content-area single">
        <article>
          <div class="entry-meta">
{make_cat_links(post['categories'])}
            <span class="posted-on">
              <time datetime="{post['date_iso']}">{post['date_formatted']}</time>
            </span>
          </div>
          <header class="entry-header">
            <h1 class="entry-title">{post['title']}</h1>
          </header>
          <div class="entry-content">
            {post['content']}
          </div>
        </article>
      </main>"""


def clean_output():
    """安全清理：只删 HTML 目录，不删 src/"""
    for item in ROOT.iterdir():
        if item.name in SAFE:
            continue
        if item.is_dir():
            import shutil
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

    # 读取所有文章
    posts_dir = CONTENT / "posts"
    posts = []
    if posts_dir.exists():
        for md_file in sorted(posts_dir.glob("*.md"), reverse=True):
            posts.append(parse_page(md_file))

    # 首页
    list_items = "\n".join(article_list_item(p) for p in posts)
    home_body = f'      <main class="content-area">\n{list_items}\n      </main>'
    (ROOT / "index.html").write_text(build_html(SITE_TITLE, home_body, ""))

    # /posts/
    (ROOT / "posts").mkdir(parents=True, exist_ok=True)
    (ROOT / "posts" / "index.html").write_text(
        build_html(SITE_TITLE, home_body, "")
    )

    # 每篇文章
    for post in posts:
        body = article_full(post)
        page = build_html(
            f"{post['title']} – {SITE_TITLE}",
            body,
            "",
            description=post["description"],
        )
        post_dir = ROOT / "posts" / post["slug"]
        post_dir.mkdir(parents=True, exist_ok=True)
        (post_dir / "index.html").write_text(page)

    # 关于页
    about_md = CONTENT / "about.md"
    if about_md.exists():
        about = parse_page(about_md)
        body = f"""      <main class="content-area single">
        <article>
          <header class="entry-header">
            <h1 class="entry-title">{about['title']}</h1>
          </header>
          <div class="entry-content">
            {about['content']}
          </div>
        </article>
      </main>"""
        page = build_html(
            f"{about['title']} – {SITE_TITLE}", body, "", current_menu="/about/"
        )
        (ROOT / "about").mkdir(parents=True, exist_ok=True)
        (ROOT / "about" / "index.html").write_text(page)

    print(f"✅ 构建完成！")


if __name__ == "__main__":
    build()
