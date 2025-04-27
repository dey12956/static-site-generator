# static-site-generator


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?logo=github)](https://dey12956.github.io/static-site-generator/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

This is a lightweight **Static Site Generator** written in pure Python.

It takes Markdown files and a base HTML template, and automatically generates a complete static website.
The generator also correctly handles asset paths (CSS, images, links) for deployment on GitHub Pages or any static hosting service.

## Features

- Converts **Markdown** files into structured **HTML** pages
- **Parses inline markdown** (bold, italic, code, links, images)
- **Maintains directory structure** when copying content and assets
- **Flexible template engine** with {{ Title }} and {{ Content }} placeholders
- **Basepath configuration** for clean deployment under custom GitHub Pages URLs
- **Automatic static asset** copying (static/ to docs/)
- **Fully self-contained** output inside the docs/ folder, ready for GitHub Pages
- **Recursive page generation** for nested content folders
- **Error handling** for malformed markdown
- Built from scratch without external libraries (except os, shutil, and re)

## How It Works

1.	**Markdown Parsing**
Markdown files are parsed into a tree of TextNodes and HTMLNodes.
2.	**Template Injection**
The parsed content is injected into an HTML template, replacing {{ Title }} and {{ Content }} placeholders.
3.	**Asset Handling**
Static files (images, CSS) are copied into the output directory, and their paths are rewritten to match the site’s basepath.
4.	**Basepath Adjustment**
All internal links, images, and CSS links are automatically adjusted to match the deployment path (e.g., /repo-name/ on GitHub Pages).
5.	**Site Generation**
The complete site structure is generated recursively into a docs/ folder.

## Live Deployment

The generated site is designed for easy deployment on [GitHub Pages](https://pages.github.com) under the /docs folder.
Just push the latest docs/ to your main branch and configure GitHub Pages to deploy from /docs.

## Skills Demonstrated
- Recursive file and folder manipulation
- Parsing and transforming text data (Markdown to HTML)
- Building a simple static templating engine
- Understanding of HTML, Markdown standards
- Handling relative vs absolute URLs for static hosting
- Error handling, code modularization
- Automating project builds
- Careful attention to deployment details (basepath issues, GitHub Pages quirks)