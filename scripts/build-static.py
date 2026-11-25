#!/usr/bin/env python3
"""从 markdown/ 生成纯静态 HTML，发布时不必再跑 Node 或 VitePress。"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_ROOT = ROOT / "markdown"
OUT_ROOT = ROOT

NAV_GROUPS = [
    ("开始", [
        ("总体说明", "start/overview.html"),
        ("快速上手", "start/quick-start.html"),
        ("登录与两端", "start/login.html"),
        ("角色与权限", "start/roles.html"),
    ]),
    ("业主与商机", [
        ("业主管理", "owner/owner.html"),
        ("商机初勘", "owner/opportunity.html"),
    ]),
    ("勘察与签约", [
        ("电站勘察", "survey/survey.html"),
        ("业主补贴", "survey/subsidy.html"),
        ("合同签约", "survey/contract.html"),
        ("备案登记", "survey/filing.html"),
    ]),
    ("设计与开工准备", [
        ("电站设计", "design/design.html"),
        ("电站建档", "design/archive.html"),
        ("电站备货", "design/stock.html"),
    ]),
    ("安装施工", [
        ("派工与安全打卡", "install/dispatch.html"),
        ("工程领料", "install/pick.html"),
        ("施工复核", "install/review.html"),
        ("支架报装", "install/bracket.html"),
        ("电气报装", "install/electric.html"),
        ("电表安装", "install/meter.html"),
        ("完工自检", "install/selfcheck.html"),
    ]),
    ("产权与消缺", [
        ("产权证明", "property/property.html"),
        ("消缺工单", "property/defect.html"),
    ]),
    ("审核与工单", [
        ("审核中心", "audit/audit.html"),
        ("工单中心", "audit/workorder.html"),
    ]),
    ("系统设置", [
        ("审批设置", "settings/approval.html"),
        ("现场端品牌", "settings/brand.html"),
        ("组织与安装队", "settings/org.html"),
    ]),
    ("附录", [
        ("常见提示", "appendix/tips.html"),
        ("当前未开放的能力", "appendix/not-open.html"),
        ("电站查询（简要）", "appendix/station.html"),
    ]),
]

FLAT_PAGES: list[tuple[str, str]] = []
for _, items in NAV_GROUPS:
    FLAT_PAGES.extend(items)

MD_BY_OUT = {out: MD_ROOT / out.replace(".html", ".md") for _, out in FLAT_PAGES}

FLOW_SVG = '''<div class="flow" role="img" aria-label="主流程：从商机初勘到电表安装">
<svg viewBox="0 0 720 520" xmlns="http://www.w3.org/2000/svg" font-family="Noto Sans SC, PingFang SC, Microsoft YaHei, sans-serif">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#c45c26"/>
    </marker>
  </defs>
  <style>
    .n { fill:#fff; stroke:#c45c26; stroke-width:1.4; rx:6; }
    .t { fill:#213547; font-size:13px; text-anchor:middle; dominant-baseline:middle; }
    .e { stroke:#c45c26; stroke-width:1.5; fill:none; marker-end:url(#arr); }
  </style>
  <rect class="n" x="40" y="16" width="120" height="36" rx="6"/>
  <text class="t" x="100" y="35">商机初勘</text>
  <rect class="n" x="240" y="16" width="120" height="36" rx="6"/>
  <text class="t" x="300" y="35">电站勘察</text>
  <rect class="n" x="160" y="96" width="120" height="36" rx="6"/>
  <text class="t" x="220" y="115">业主补贴</text>
  <rect class="n" x="360" y="96" width="120" height="36" rx="6"/>
  <text class="t" x="420" y="115">合同签约</text>
  <rect class="n" x="160" y="176" width="120" height="36" rx="6"/>
  <text class="t" x="220" y="195">备案登记</text>
  <rect class="n" x="360" y="176" width="120" height="36" rx="6"/>
  <text class="t" x="420" y="195">电站设计</text>
  <rect class="n" x="260" y="256" width="120" height="36" rx="6"/>
  <text class="t" x="320" y="275">电站建档</text>
  <rect class="n" x="160" y="336" width="120" height="36" rx="6"/>
  <text class="t" x="220" y="355">电站备货</text>
  <rect class="n" x="360" y="336" width="120" height="36" rx="6"/>
  <text class="t" x="420" y="355">安装队派工</text>
  <rect class="n" x="160" y="416" width="120" height="36" rx="6"/>
  <text class="t" x="220" y="435">工程领料</text>
  <rect class="n" x="360" y="416" width="120" height="36" rx="6"/>
  <text class="t" x="420" y="435">施工复核</text>
  <rect class="n" x="40" y="476" width="120" height="36" rx="6"/>
  <text class="t" x="100" y="495">支架报装</text>
  <rect class="n" x="240" y="476" width="120" height="36" rx="6"/>
  <text class="t" x="300" y="495">电气报装</text>
  <rect class="n" x="500" y="476" width="120" height="36" rx="6"/>
  <text class="t" x="560" y="495">电表安装</text>
  <path class="e" d="M160 34 H236"/>
  <path class="e" d="M300 52 V80 H220 V94"/>
  <path class="e" d="M300 52 V80 H420 V94"/>
  <path class="e" d="M220 132 V174"/>
  <path class="e" d="M420 132 V174"/>
  <path class="e" d="M220 212 V236 H320 V254"/>
  <path class="e" d="M420 212 V236 H320"/>
  <path class="e" d="M320 292 V314 H220 V334"/>
  <path class="e" d="M320 292 V314 H420 V334"/>
  <path class="e" d="M220 372 V414"/>
  <path class="e" d="M420 372 V414"/>
  <path class="e" d="M220 452 V466 H100 V476"/>
  <path class="e" d="M220 452 V466 H300 V476"/>
  <path class="e" d="M420 452 V466 H300"/>
  <path class="e" d="M420 452 V466 H560 V476"/>
  <path class="e" d="M160 494 H236"/>
  <path class="e" d="M360 494 H496"/>
</svg>
</div>'''


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def rel_to(from_page: str, to_path: str) -> str:
    if not to_path or to_path.startswith(("http://", "https://", "mailto:", "#")):
        return to_path
    frag = ""
    path = to_path
    if "#" in path:
        path, frag = path.split("#", 1)
        frag = "#" + frag
    if path.startswith("/"):
        path = path.lstrip("/")
    elif path.startswith("../images/"):
        path = "images/" + path.split("images/", 1)[1]
    if not path:
        return frag or "#"
    src = Path(from_page if from_page not in (".", "") else "index.html")
    src_dir = Path(".") if src.name == from_page or str(src.parent) == "." else src.parent
    if from_page in ("index.html", "404.html"):
        src_dir = Path(".")
    else:
        src_dir = Path(from_page).parent
    rel = Path(path)
    # relative from src_dir to path
    cur = Path(*([".."] * len(src_dir.parts))) if src_dir != Path(".") else Path(".")
    out = (cur / rel).as_posix()
    if out.startswith("./"):
        out = out[2:]
    # normalize .. with later parts already ok for one-level pages
    if src_dir == Path("."):
        out = Path(path).as_posix()
    else:
        out = ("../" * len(src_dir.parts)) + Path(path).as_posix()
    return out + frag


def root_prefix(page: str) -> str:
    return "" if page in ("index.html", "404.html") else "../" * len(Path(page).parent.parts)


def slug(title: str) -> str:
    text = title.strip()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[#?&/\\]+", "", text)
    return text or "section"


def inline(text: str, page: str) -> str:
    parts: list[str] = []
    i = 0
    n = len(text)

    def take_code(s, start):
        m = re.match(r"`([^`]+)`", s[start:])
        if not m:
            return None
        return m.end(), f"<code>{esc(m.group(1))}</code>"

    while i < n:
        if text[i] == "`":
            got = take_code(text, i)
            if got:
                i += got[0]
                parts.append(got[1])
                continue
        if text.startswith("![", i):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", text[i:])
            if m:
                alt, src = m.group(1), m.group(2)
                src = rel_to(page, src)
                parts.append(
                    f'<img class="shot" src="{esc(src)}" alt="{esc(alt)}">'
                )
                i += m.end()
                continue
        if text.startswith("[", i):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", text[i:])
            if m:
                label, href = m.group(1), m.group(2)
                href = rel_to(page, href)
                parts.append(f'<a href="{esc(href)}">{inline(label, page)}</a>')
                i += m.end()
                continue
        if text.startswith("**", i):
            m = re.match(r"\*\*(.+?)\*\*", text[i:], re.S)
            if m:
                parts.append(f"<strong>{inline(m.group(1), page)}</strong>")
                i += m.end()
                continue
        if text[i] == "*" and not text.startswith("* ", i):
            m = re.match(r"\*(.+?)\*", text[i:], re.S)
            if m and "\n" not in m.group(1):
                parts.append(f"<em>{inline(m.group(1), page)}</em>")
                i += m.end()
                continue
        # run of plain text
        j = i + 1
        while j < n and text[j] not in "`[!*":
            j += 1
        # if * might start italic, stop before it; already handled
        parts.append(esc(text[i:j]))
        i = j
    return "".join(parts)



def render_qr_block(lines: list[str], page: str) -> str:
    """将 ::: qr 块渲染为并排的入口二维码卡片。"""
    cards: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        parts = [c.strip() for c in line.split("|")]
        if len(parts) != 3:
            raise SystemExit(f"qr 块格式应为「标签 | URL | 图片路径」，得到：{raw!r}")
        label, url, img = parts
        if not url.startswith("https://") or " " in url:
            raise SystemExit(f"qr 块 URL 无效：{url!r}")
        src = rel_to(page, img)
        alt = f"{label}入口二维码，内容为 {url}"
        cards.append(
            "<figure class=\"qr-card\">"
            f'<img class="qr" src="{esc(src)}" alt="{esc(alt)}" width="208" height="208">'
            "<figcaption>"
            f'<span class="qr-label">{esc(label)}</span>'
            f'<a class="qr-link" href="{esc(url)}">{esc(url)}</a>'
            "</figcaption></figure>"
        )
    if not cards:
        raise SystemExit("qr 块没有条目")
    return '<div class="qr-row">' + "".join(cards) + "</div>"


def split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_sep_row(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def md_to_html(src: str, page: str) -> tuple[str, list[tuple[int, str, str]]]:
    text = src.replace("\r\n", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5:]
    text = re.sub(
        r"```mermaid\n.*?```",
        lambda m: "\n\n<!--FLOW-->\n\n",
        text,
        flags=re.S,
    )
    lines = text.split("\n")
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    i = 0
    used: dict[str, int] = {}

    def unique(sid: str) -> str:
        if sid not in used:
            used[sid] = 1
            return sid
        used[sid] += 1
        return f"{sid}-{used[sid]}"

    while i < len(lines):
        line = lines[i]
        if line.strip() == "<!--FLOW-->":
            out.append(FLOW_SVG)
            i += 1
            continue
        if line.startswith("::: "):
            kind_title = line[4:].strip()
            parts = kind_title.split(None, 1)
            kind = parts[0]
            title = parts[1] if len(parts) > 1 else kind
            buf = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                buf.append(lines[i])
                i += 1
            i += 1
            if kind == "qr":
                out.append(render_qr_block(buf, page))
                continue
            inner, _ = md_to_html("\n".join(buf), page)
            out.append(
                f'<div class="custom-block {esc(kind)}"><p class="custom-block-title">{esc(title)}</p>{inner}</div>'
            )
            continue
        if line.startswith("#"):
            m = re.match(r"^(#{1,3})\s+(.+)$", line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                sid = unique(slug(title))
                if level >= 2:
                    toc.append((level, sid, title))
                out.append(f"<h{level} id=\"{esc(sid)}\">{inline(title, page)}</h{level}>")
                i += 1
                continue
        if re.match(r"^\s*\|", line) and i + 1 < len(lines) and is_sep_row(lines[i + 1]):
            headers = split_table_row(line)
            i += 2
            rows = []
            while i < len(lines) and re.match(r"^\s*\|", lines[i]):
                rows.append(split_table_row(lines[i]))
                i += 1
            html_t = ["<table><thead><tr>"]
            html_t += [f"<th>{inline(h, page)}</th>" for h in headers]
            html_t.append("</tr></thead><tbody>")
            for row in rows:
                html_t.append("<tr>")
                for idx in range(len(headers)):
                    cell = row[idx] if idx < len(row) else ""
                    html_t.append(f"<td>{inline(cell, page)}</td>")
                html_t.append("</tr>")
            html_t.append("</tbody></table>")
            out.append("".join(html_t))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it, page)}</li>" for it in items) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(it, page)}</li>" for it in items) + "</ol>")
            continue
        if line.strip() == "---" or line.strip() == "***":
            out.append("<hr>")
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith(":::") and not re.match(r"^\s*\|", lines[i]) and not re.match(r"^\s*[-*]\s+", lines[i]) and not re.match(r"^\s*\d+\.\s+", lines[i]):
            buf.append(lines[i])
            i += 1
        para = " ".join(x.strip() for x in buf)
        if re.fullmatch(r"\*.+\*", para) and not para.startswith("**"):
            out.append(f'<p class="caption">{inline(para[1:-1], page)}</p>')
        else:
            out.append(f"<p>{inline(para, page)}</p>")
    return "\n".join(out), toc


def sidebar_html(page: str) -> str:
    chunks = []
    for group, items in NAV_GROUPS:
        open_cls = ""
        lis = []
        for title, href in items:
            if href == page:
                open_cls = " open"
            cls = ' class="active"' if href == page else ""
            lis.append(f'<a href="{esc(rel_to(page, href))}"{cls}>{esc(title)}</a>')
        # 开始 / 业主与商机 default open if nothing in group is current? keep current group + 开始 + 业主
        if group in ("开始", "业主与商机") and not open_cls:
            # keep 开始 open on home; otherwise only current
            if page in ("index.html", "404.html") or group == "开始" and page.startswith("start/"):
                open_cls = " open"
            if page == "index.html" and group in ("开始", "业主与商机"):
                open_cls = " open"
        chunks.append(
            f'<div class="sidebar-group{open_cls}">'
            f'<button type="button" class="sidebar-title">{esc(group)}'
            f'<svg class="caret" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 6l6 6-6 6"/></svg>'
            f"</button><div class=\"sidebar-items\">" + "".join(lis) + "</div></div>"
        )
    return "".join(chunks)


def toc_html(toc: list[tuple[int, str, str]]) -> str:
    if not toc:
        return ""
    links = []
    for level, sid, title in toc:
        cls = "l3" if level >= 3 else "l2"
        links.append(f'<a class="{cls}" href="#{esc(sid)}">{esc(title)}</a>')
    return '<nav class="toc" aria-label="本页目录"><h2>本页目录</h2>' + "".join(links) + "</nav>"


def pager_html(page: str) -> str:
    if page == "index.html":
        return ""
    keys = [href for _, href in FLAT_PAGES]
    try:
        idx = keys.index(page)
    except ValueError:
        return ""
    prev_l = next_l = ""
    if idx > 0:
        title, href = FLAT_PAGES[idx - 1]
        prev_l = f'<a class="prev" href="{esc(rel_to(page, href))}"><span class="label">上一页</span>{esc(title)}</a>'
    else:
        prev_l = "<span></span>"
    if idx < len(keys) - 1:
        title, href = FLAT_PAGES[idx + 1]
        next_l = f'<a class="next" href="{esc(rel_to(page, href))}"><span class="label">下一页</span>{esc(title)}</a>'
    return f'<nav class="pager">{prev_l}{next_l}</nav>'


def shell(page: str, title: str, body: str, toc: str, extra_class: str = "") -> str:
    prefix = root_prefix(page)
    page_title = title if title.startswith("国华") else f"{title} · 国华光伏建设管理系统"
    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-root="{esc(prefix)}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(page_title)}</title>
  <meta name="description" content="国华光伏建设管理系统使用说明：电脑端与现场端各模块的操作指南">
  <link rel="icon" href="{esc(prefix)}images/logo.svg">
  <link rel="stylesheet" href="{esc(prefix)}assets/css/style.css">
</head>
<body class="{esc(extra_class)}">
  <header class="site-header">
    <a class="brand" href="{esc(rel_to(page, 'index.html'))}">
      <img src="{esc(prefix)}images/logo.svg" alt="国华光伏标志">
      <span>国华光伏 <span class="full">使用说明</span></span>
    </a>
    <button type="button" class="header-search" data-open-search>搜索 <kbd>Ctrl K</kbd></button>
    <button type="button" class="hamburger" aria-label="打开目录"><span></span></button>
  </header>
  <div class="sidebar-mask"></div>
  <div class="layout">
    <aside class="sidebar" aria-label="站点目录">{sidebar_html(page)}</aside>
    <div class="content-wrap">
      <main class="content">{body}{pager_html(page)}
        <p class="site-footer">国华光伏建设管理系统 · 使用说明（按当前演示环境整理）<br>操作以线上实际界面为准</p>
      </main>
    </div>
    {toc}
  </div>
  <div class="search-mask" role="dialog" aria-label="搜索">
    <div class="search-box">
      <input class="search-input" type="search" placeholder="搜索使用说明…" autocomplete="off">
      <div class="search-results"><div class="search-hint">输入关键词，例如「派工」「电表」「勘察」。</div></div>
    </div>
  </div>
  <script src="{esc(prefix)}assets/js/app.js"></script>
</body>
</html>
"""


def home_body(page: str) -> str:
    note = md_to_html(
        "请先阅读 [总体说明](/start/overview.html)，其中包含系统介绍、主流程和角色分工。左侧目录可以展开或收起，右上角可以搜索，每一页右侧是本页目录。",
        page,
    )[0]
    return f"""
<section class="home-hero">
  <div>
    <h1>国华光伏建设管理系统<br>使用说明</h1>
    <p class="lead">户用分布式光伏从线索、勘察、签约到施工、装表的操作手册。电脑端适合审核、查询和集中办理，现场端适合登记、定位、拍照和提交。两端共用同一套账号和数据。</p>
    <div class="home-actions">
      <a class="btn btn-brand" href="{esc(rel_to(page, 'start/overview.html'))}">总体说明</a>
      <a class="btn btn-alt" href="{esc(rel_to(page, 'start/login.html'))}">登录与两端</a>
    </div>
  </div>
  <img class="home-logo" src="{esc(rel_to(page, 'images/logo.svg'))}" alt="国华光伏标志">
</section>
<section class="features">
  <article class="feature"><h2>电脑端</h2><p>审核中心、电站查询、审批设置和现场端品牌配置，以及各业务单据的集中办理。演示地址见「登录与两端」。</p></article>
  <article class="feature"><h2>现场端</h2><p>现场端是用手机浏览器打开的 H5 页面（也可编译为小程序）。底部导航为「首页」「应用」「我的」。业务入口在「应用」的「开发/交付」分类中。</p></article>
  <article class="feature"><h2>按角色办理</h2><p>开发经理、现勘员、设计师、项目经理、仓储、安装队负责人和审核员各有菜单和数据范围。没有写权限时只能查看，不能保存或提交。</p></article>
</section>
{note}
"""


def strip_tags(text: str) -> str:
    text = re.sub(r"<script[\s\S]*?</script>", " ", text)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def heading_of(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def main() -> None:
    search = []
    # home
    body = home_body("index.html")
    write(OUT_ROOT / "index.html", shell("index.html", "国华光伏建设管理系统", body, "", "home"))
    search.append({"title": "使用说明首页", "url": "index.html", "text": strip_tags(body)})

    for title, out in FLAT_PAGES:
        md_path = MD_BY_OUT[out]
        if not md_path.exists():
            raise SystemExit(f"缺少 Markdown：{md_path}")
        raw = md_path.read_text(encoding="utf-8")
        page_title = heading_of(raw, title)
        body, toc = md_to_html(raw, out)
        html_page = shell(out, page_title, body, toc_html(toc))
        write(OUT_ROOT / out, html_page)
        search.append({
            "title": page_title,
            "url": out,
            "text": strip_tags(body)[:4000],
        })

    notfound = shell(
        "404.html",
        "页面不存在",
        '<h1>页面不存在</h1><p>请回到 <a href="index.html">使用说明首页</a>，或从左侧目录进入各模块。</p>',
        "",
    )
    write(OUT_ROOT / "404.html", notfound)

    idx_js = "window.SEARCH_INDEX = " + json.dumps(search, ensure_ascii=False, indent=2) + ";\n"
    write(OUT_ROOT / "assets" / "js" / "search-index.js", idx_js)
    print("done", len(FLAT_PAGES) + 2, "pages")


if __name__ == "__main__":
    main()
