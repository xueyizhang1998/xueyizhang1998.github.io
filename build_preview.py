#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地预览生成器 —— 读取 _data/*.yml，套用 assets/css/style.css，
输出单文件 preview.html（无需安装 Jekyll，双击即可看效果）。
这只是“所见即所得”的预览；正式部署仍由 GitHub Pages 用 Jekyll 构建。
用法：python3 build_preview.py
"""
import os, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(ROOT, "_data", name), encoding="utf-8") as f:
        return yaml.safe_load(f)

profile = load("profile.yml")
about   = load("about.yml")
news    = load("news.yml")
pubs    = load("publications.yml")
groups  = load("pub_groups.yml")
exper   = load("experience.yml") or []
projs   = load("projects.yml") or []
honors  = load("honors.yml") or []
ui      = load("ui.yml")

with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
GROUPED = cfg.get("group_publications", True)

with open(os.path.join(ROOT, "assets", "css", "style.css"), encoding="utf-8") as f:
    CSS = f.read()
with open(os.path.join(ROOT, "assets", "js", "main.js"), encoding="utf-8") as f:
    JS = f.read()

ICONS = {
 "email":'<svg viewBox="0 0 24 24"><path d="M2 4h20v16H2V4zm2 2v.5l8 5 8-5V6H4zm16 3.2-8 5-8-5V18h16V9.2z"/></svg>',
 "scholar":'<svg viewBox="0 0 24 24"><path d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3zM4 14v3.5c0 1.9 3.6 3.5 8 3.5s8-1.6 8-3.5V14l-8 4.4L4 14z"/></svg>',
 "github":'<svg viewBox="0 0 24 24"><path d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.3-1.3-1.7-1.3-1.7-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.7 1.3 3.4 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.3-1.3-5.3-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17 4.5 18 4.8 18 4.8c.6 1.6.2 2.8.1 3.1.8.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6 4.6-1.5 7.9-5.8 7.9-10.9C23.5 5.7 18.3.5 12 .5z"/></svg>',
 "dblp":'<svg viewBox="0 0 24 24"><path d="M8 2c-1 3 0 4 1 5-2 1-4 2-4 6 0 5 4 9 8 9 2 0 3-1 3-3 0-3-3-4-3-7 0-1 1-2 1-4 0-4-4-6-6-6zm2 3c1 0 2 1 2 3s-1 2-1 4c0 2 1 3 2 4 0 2-1 3-2 3-3 0-6-3-6-7 0-3 2-4 4-5-1-1-1-3-1-5z"/></svg>',
 "orcid":'<svg viewBox="0 0 24 24"><path d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24zM7.4 17.6H5.6V8.9h1.8v8.7zM6.5 7.8a1.1 1.1 0 1 1 0-2.2 1.1 1.1 0 0 1 0 2.2zm11.1 9.8H13V8.9h4.3c3 0 4.4 2 4.4 4.3 0 2.5-1.9 4.4-4.1 4.4zm-.3-7.1h-2.5v5.5h2.4c1.8 0 2.7-1.3 2.7-2.8 0-1.4-.8-2.7-2.6-2.7z"/></svg>',
 "linkedin":'<svg viewBox="0 0 24 24"><path d="M4.98 3.5A2.5 2.5 0 1 0 5 8.5a2.5 2.5 0 0 0 0-5zM3 9h4v12H3V9zm6 0h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.3c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V21H9V9z"/></svg>',
 "twitter":'<svg viewBox="0 0 24 24"><path d="M18.9 2H22l-7 8 8.3 12h-6.5l-5-6.6L5.9 22H2.8l7.5-8.6L2.3 2h6.6l4.6 6.1L18.9 2zm-1.1 18h1.7L7.3 3.8H5.5L17.8 20z"/></svg>',
 "cv":'<svg viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6V2zm8 1.5V8h4.5L14 3.5zM8 13h8v1.5H8V13zm0 3h8v1.5H8V16zm0-6h4v1.5H8V10z"/></svg>',
 "link":'<svg viewBox="0 0 24 24"><path d="M3.9 12a3.1 3.1 0 0 1 3.1-3.1h4V7H7a5 5 0 0 0 0 10h4v-1.9H7A3.1 3.1 0 0 1 3.9 12zM8 13h8v-2H8v2zm9-6h-4v1.9h4a3.1 3.1 0 0 1 0 6.2h-4V17h4a5 5 0 0 0 0-10z"/></svg>',
 "code":'<svg viewBox="0 0 24 24"><path d="M9.4 16.6 4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0 4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/></svg>',
 "video":'<svg viewBox="0 0 24 24"><path d="M4 4h16v16H4V4zm6 4v8l6-4-6-4z"/></svg>',
 "doc":'<svg viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6V2zm8 1.5V8h4.5L14 3.5z"/></svg>',
}

def rel(path):
    # 预览用相对路径，保证本机 file:// 双击也能加载图片/资源
    if isinstance(path, str) and path.startswith("/"):
        return path[1:]
    return path

def bilingual(en, zh, tag="span"):
    return f'<{tag} class="i18n-en">{en}</{tag}><{tag} class="i18n-zh">{zh}</{tag}>'

def authors_html(s):
    out = ""
    for i, p in enumerate((s or "").split("**")):
        out += p if i % 2 == 0 else f"<strong>{p}</strong>"
    return out

def icon(k): return ICONS.get(k, "")

def attr(s):
    """转义成可安全放进 HTML 属性的文本（论文标题里有引号、& 等）。"""
    return (str(s or "").replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))

def sidebar_html():
    p = profile
    s = []
    s.append('<aside class="sidebar">')
    s.append(f'<img class="avatar" src="{rel(p["avatar"])}" alt="avatar" '
             f'onerror="this.src=\'assets/img/avatar-placeholder.svg\'">')
    s.append(f'<div class="name">{bilingual(p["name"]["en"], p["name"]["zh"])}</div>')
    s.append(f'<div class="role">{bilingual(p["role"]["en"], p["role"]["zh"])}</div>')
    s.append(f'<div class="affil">'
             f'<span class="i18n-en">{(profile["department"]["en"] + ", ") if profile["department"]["en"] else ""}{p["affiliation"]["en"]}</span>'
             f'<span class="i18n-zh">{p["affiliation"]["zh"]}{(" " + p["department"]["zh"]) if p["department"]["zh"] else ""}</span></div>')
    if p.get("location", {}).get("en"):
        s.append(f'<div class="affil">{bilingual(p["location"]["en"], p["location"]["zh"])}</div>')
    if p["motto"]["en"]:
        s.append(f'<div class="motto">{bilingual(p["motto"]["en"], p["motto"]["zh"])}</div>')
    s.append('<hr>')
    if p["email"]:
        user, dom = p["email"].split("@")
        s.append(f'<div class="contact-line">{icon("email")}'
                 f'<a href="#" class="email-link" data-user="{user}" data-dom="{dom}">email</a></div>')
    s.append('<div class="social">')
    for key, ic in [("scholar","scholar"),("github","github"),("dblp","dblp"),
                    ("orcid","orcid"),("linkedin","linkedin"),("twitter","twitter"),("cv","cv")]:
        url = p["links"].get(key, "")
        if url:
            s.append(f'<a href="{url}" target="_blank" rel="noopener" title="{key}">{icon(ic)}</a>')
    s.append('</div></aside>')
    return "\n".join(s)

def pub_card(pub):
    s = ['<div class="pub">']
    img = rel(pub.get("image"))
    if img:
        cap = attr(pub["title"])
        zoom = attr(ui["labels"]["zoom"]["en"])
        s.append(f'<div class="thumb">'
                 f'<button type="button" class="zoom" data-full="{img}" data-cap="{cap}" '
                 f'aria-label="{cap} &mdash; {zoom}">'
                 f'<img src="{img}" alt="{cap}" '
                 f'onerror="this.closest(&quot;.thumb&quot;).innerHTML=&quot;<span class=\\&quot;ph\\&quot;>{pub["venue"]}</span>&quot;">'
                 f'</button></div>')
    else:
        s.append(f'<div class="thumb"><span class="ph">{pub["venue"]}</span></div>')
    s.append('<div class="body">')
    star = '<span class="star" title="Selected">&#9733;</span>' if pub.get("selected") else ""
    note = f'<span class="note">{pub["note"]}</span>' if pub.get("note") else ""
    s.append(f'<div class="title">{star}{pub["title"]}{note}</div>')
    s.append(f'<div class="authors">{authors_html(pub.get("authors",""))}</div>')
    s.append(f'<div class="venue">{pub["venue"]}</div>')
    d = pub.get("desc") or {}
    if d.get("en"):
        s.append(f'<div class="desc">{bilingual(d["en"], d.get("zh",""))}</div>')
    if pub.get("tags"):
        s.append('<div class="ptags">' + "".join(f"<span>{t}</span>" for t in pub["tags"]) + "</div>")
    links = pub.get("links") or {}
    btns = []
    lb = ui["buttons"]
    def mk(url, ic, en, zh, cls=""):
        attr = f' class="{cls}"' if cls else ""
        return (f'<a{attr} href="{url}" target="_blank" rel="noopener">{icon(ic)}'
                f'{bilingual(en, zh)}</a>')
    if links.get("paper"):   btns.append(mk(links["paper"],"doc",lb["paper"]["en"],lb["paper"]["zh"]))
    if links.get("code"):    btns.append(mk(links["code"],"code",lb["code"]["en"],lb["code"]["zh"]))
    if links.get("project"): btns.append(mk(links["project"],"link",lb["project"]["en"],lb["project"]["zh"]))
    if links.get("doi"):     btns.append(mk(links["doi"],"link",lb["doi"]["en"],lb["doi"]["zh"], cls="secondary"))
    if links.get("bibtex"):  btns.append(mk(links["bibtex"],"doc",lb["bibtex"]["en"],lb["bibtex"]["en"]))
    if links.get("video"):   btns.append(mk(links["video"],"video",lb["video"]["en"],lb["video"]["zh"]))
    s.append('<div class="links">' + "".join(btns) + '</div>')
    s.append('</div></div>')
    return "\n".join(s)

def render():
    nav, lab = ui["nav"], ui["labels"]
    body = []

    # About
    body.append('<section class="section" id="about">')
    body.append(f'<h2>{bilingual(nav["about"]["en"], nav["about"]["zh"])}</h2>')
    body.append('<div class="bio">'
                f'<div class="blk i18n-en">{about["bio"]["en"]}</div>'
                f'<div class="blk i18n-zh">{about["bio"]["zh"]}</div></div>')
    body.append(f'<div class="sub-h">{bilingual(lab["interests"]["en"], lab["interests"]["zh"])}</div>')
    body.append('<div class="keywords">'
                + "".join(f'<span class="tag i18n-en">{k}</span>' for k in about["keywords"]["en"])
                + "".join(f'<span class="tag i18n-zh">{k}</span>' for k in about["keywords"]["zh"])
                + '</div></section>')

    # News
    body.append('<section class="section" id="news">')
    body.append(f'<h2>{bilingual(nav["news"]["en"], nav["news"]["zh"])}</h2><ul class="news">')
    for n in news:
        body.append(f'<li><span class="date">{n["date"]}</span>'
                    f'<span class="what">{bilingual(n["en"], n["zh"])}</span></li>')
    body.append('</ul></section>')

    # Publications
    body.append('<section class="section" id="publications">')
    body.append(f'<h2>{bilingual(nav["publications"]["en"], nav["publications"]["zh"])}</h2>')
    body.append(f'<div class="hint">{bilingual(lab["first_author"]["en"], lab["first_author"]["zh"])}</div>')
    selected = [p for p in pubs if p.get("selected")]
    if selected:
        body.append(f'<div class="sub-h">{bilingual(lab["selected_pubs"]["en"], lab["selected_pubs"]["zh"])}</div>')
        for p in sorted(selected, key=lambda x: x.get("order",0), reverse=True):
            body.append(pub_card(p))
    if GROUPED:
        body.append(f'<div class="sub-h" style="margin-top:1.8rem">{bilingual(lab["by_topic"]["en"], lab["by_topic"]["zh"])}</div>')
        for g in groups:
            items = sorted([p for p in pubs if p.get("group")==g["id"]],
                           key=lambda x: x.get("order",0), reverse=True)
            if items:
                body.append(f'<div class="group-h">{bilingual(g["en"], g["zh"])}</div>')
                for p in items: body.append(pub_card(p))
    else:
        allpubs = sorted(pubs, key=lambda p: p.get("order", 0), reverse=True)
        body.append(f'<div class="sub-h" style="margin-top:1.8rem">{bilingual(lab["all_pubs"]["en"], lab["all_pubs"]["zh"])}</div>')
        for p in allpubs: body.append(pub_card(p))
    body.append('</section>')

    # Experience（合并工作/学历/访学，按 sort 倒序）
    if exper:
        body.append('<section class="section" id="experience">')
        body.append(f'<h2>{bilingual(nav["experience"]["en"], nav["experience"]["zh"])}</h2><div class="exp-list">')
        for x in sorted(exper, key=lambda a: a.get("sort",0), reverse=True):
            logo = x.get("logo") or ""
            inner = (f'<img src="assets/img/logo/{logo}" alt="{x.get("abbr","")}">'
                     if logo else f'<span class="abbr">{x.get("abbr","")}</span>')
            kind = ""
            if x.get("kind")=="visiting":
                kind = (f'<span class="exp-kind visiting">'
                        f'{bilingual(ui["kinds"]["visiting"]["en"], ui["kinds"]["visiting"]["zh"])}</span>')
            locen = f' · {x["location"]["en"]}' if x.get("location",{}).get("en") else ""
            loczh = f' · {x["location"]["zh"]}' if x.get("location",{}).get("zh") else ""
            adv = ""
            if x.get("advisor",{}).get("en"):
                adv = f'<div class="exp-meta">{bilingual(x["advisor"]["en"], x["advisor"]["zh"])}</div>'
            body.append(
                '<div class="exp-item">'
                f'<div class="exp-logo">{inner}</div>'
                '<div class="exp-body"><div class="exp-top">'
                f'<span class="exp-role">{bilingual(x["role"]["en"], x["role"]["zh"])}{kind}</span>'
                f'<span class="exp-period">{x["period"]}</span></div>'
                f'<div class="exp-org"><span class="i18n-en">{x["org"]["en"]}{locen}</span>'
                f'<span class="i18n-zh">{x["org"]["zh"]}{loczh}</span></div>{adv}'
                '</div></div>')
        body.append('</div></section>')

    # Projects
    if projs:
        body.append('<section class="section" id="projects">')
        body.append(f'<h2>{bilingual(nav["projects"]["en"], nav["projects"]["zh"])}</h2>')
        for pr in projs:
            per = f' · {pr["period"]}' if pr.get("period") else ""
            body.append('<div class="proj-card" style="margin-bottom:.7rem">'
                        f'<div class="pname">{bilingual(pr["name"]["en"], pr["name"]["zh"])}</div>'
                        f'<div class="pprog">{bilingual(pr["program"]["en"], pr["program"]["zh"])}{per}</div>'
                        f'<div class="prole">{bilingual(pr["role"]["en"], pr["role"]["zh"])}</div></div>')
        body.append('</section>')

    # Honors
    if honors:
        body.append('<section class="section" id="honors">')
        body.append(f'<h2>{bilingual(nav["honors"]["en"], nav["honors"]["zh"])}</h2><ul class="honors">')
        for h in honors:
            body.append(f'<li><span class="hy">{h["year"]}</span>'
                        f'<span class="ht">{bilingual(h["en"], h["zh"])}</span></li>')
        body.append('</ul></section>')

    body.append('<footer class="foot">'
                f'<span class="i18n-en">&copy; {profile["name"]["en"]}. Preview build.</span>'
                f'<span class="i18n-zh">&copy; {profile["name"]["zh"]} · 预览构建。</span></footer>')

    toolbar = ('<div class="toolbar">'
      '<button id="langBtn"><span class="i18n-en">中文</span><span class="i18n-zh">EN</span></button>'
      '</div>')

    navlinks = [("about", nav["about"]), ("news", nav["news"]), ("publications", nav["publications"])]
    if exper: navlinks.append(("experience", nav["experience"]))
    if projs: navlinks.append(("projects", nav["projects"]))
    if honors: navlinks.append(("honors", nav["honors"]))
    topnav = '<nav class="topnav">' + "".join(
        f'<a href="#{i}">{bilingual(t["en"], t["zh"])}</a>' for i, t in navlinks) + '</nav>'

    return f"""<!DOCTYPE html>
<html lang="en" class="lang-en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{profile['name']['en']} — Preview</title>
<style>{CSS}</style></head>
<body>
{toolbar}
<div class="layout">
{sidebar_html()}
<main class="main">
{topnav}
{''.join(body)}
</main>
</div>
<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Figure viewer">
<button type="button" class="lb-close" id="lbClose" aria-label="{attr(lab['close']['en'])}">&times;</button>
<figure class="lb-fig"><img id="lbImg" src="" alt=""><figcaption id="lbCap"></figcaption></figure>
</div>
<script>{JS}</script>
</body></html>"""

if __name__ == "__main__":
    outpath = os.path.join(ROOT, "preview.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(render())
    print("wrote", outpath)
