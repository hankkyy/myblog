# 纵横四海

> 但行好事，莫问前程。

个人技术博客，用 Python 构建的静态站点，部署在 [Vercel](https://vercel.com) 上。

## 技术栈

- **构建**：Python + Markdown → 静态 HTML
- **样式**：参考 WordPress Cenote 主题，Roboto + Catamaran 字体
- **部署**：Vercel（自动部署）
- **搜索**：已移除

## 本地运行

```bash
# 构建
python3 src/build.py

# 本地预览
python3 -m http.server 8080
# 打开 http://localhost:8080
```

## 文章管理

所有文章在 `src/content/posts/` 目录下，Markdown 格式，YAML frontmatter：

```markdown
---
title: "文章标题"
date: 2025-01-15T12:00:00+08:00
categories: ["技术"]
description: "文章描述"
---

正文内容...
```

## 结构

```
├── index.html          # 首页
├── posts/              # 文章详情页
├── categories/         # 分类页
├── about/              # 关于页
├── page/               # 分页
├── css/                # 样式
├── src/
│   ├── build.py        # 构建脚本
│   ├── content/        # Markdown 源文件
│   └── themes/         # 主题
└── vercel.json         # Vercel 配置
```

## License

MIT
