#!/usr/bin/env python3
"""Rebuild the Xandra LLC site with a lightweight design, keeping the same copy and structure.

Reads the original static pages from a checkout of the `main` branch and writes ../site."""
import html
import os
import re
import shutil
from pathlib import Path

from bs4 import BeautifulSoup, Comment
from PIL import Image

HERE = Path(__file__).parent
SRC = Path(os.environ.get("XANDRA_SRC", Path.home() / "Sites/xandrallc-site-main"))
OUT = HERE.parent / "site"
PAGES = ["", "services", "about", "contact"]
CALENDLY = "https://calendly.com/xandrallc"
GTAG_ID, HOTJAR_ID = "GT-NBPRQ54", "1889176"

ICONS = {
    "icon-pictures": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    "icon-search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "icon-target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "icon-briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "fa-phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "fa-globe": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "fa-envelope": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}


def svg(name, cls="i"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ------------------------------------------------------------------ images
IMG = OUT / "img"
WIDTHS = [480, 800, 1200, 1600]
_cache = {}


def variants(src):
    if src in _cache:
        return _cache[src]
    p = SRC / src.lstrip("/")
    with Image.open(p) as im:
        alpha = im.mode in ("RGBA", "LA", "P")
        im = im.convert("RGBA" if alpha else "RGB")
        W, H = im.size
        stem = re.sub(r"[^a-z0-9-]+", "-", p.stem.lower()).strip("-")[:50]
        widths = sorted({w for w in WIDTHS if w < W} | {min(W, WIDTHS[-1])})
        srcset = []
        for w in widths:
            name = f"{stem}-{w}.webp"
            d = IMG / name
            if not d.exists():
                d.parent.mkdir(parents=True, exist_ok=True)
                im.resize((w, round(H * w / W)), Image.LANCZOS).save(d, "WEBP", quality=78, method=6)
            srcset.append(f"/img/{name} {w}w")
    default = [s for s in srcset if int(s.split()[-1][:-1]) <= 1200][-1].split()[0]
    _cache[src] = {"src": default, "srcset": ", ".join(srcset), "w": W, "h": H}
    return _cache[src]


class Ctx:
    def __init__(self):
        self.first = True
        self.preload = None
        self.preload_sizes = None


def img_tag(ctx, src, alt="", sizes="(max-width: 780px) 100vw, 50vw", cls="", eager=None):
    v = variants(src)
    lcp = ctx.first if eager is None else eager
    if lcp and ctx.first:
        ctx.first = False
        ctx.preload, ctx.preload_sizes = v, sizes
    loading = 'fetchpriority="high"' if lcp else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{v["src"]}" srcset="{v["srcset"]}" sizes="{sizes}" width="{v["w"]}" height="{v["h"]}" '
            f'alt="{html.escape(alt or "")}" {loading} decoding="async">')


# ------------------------------------------------------------------ content helpers
def inner(el):
    """Semantic inner HTML: drop classes/styles and wrapper divs."""
    if el is None:
        return ""
    el = BeautifulSoup(el.decode_contents(), "html.parser")
    for c in el.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in el.find_all(True):
        if t.name in ("div", "span", "sup") and t.name != "sup":
            t.unwrap()
            continue
        t.attrs = {k: v for k, v in t.attrs.items() if k in ("href", "target", "rel")}
    s = str(el).strip()
    return re.sub(r"<p>\s*</p>", "", s)


def txt(el):
    return el.get_text(" ", strip=True) if el else ""


def button(a, cls="btn"):
    href = a.get("href", "#")
    ext = href.startswith("http")
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{html.escape(href)}"{tgt}>{html.escape(txt(a))}{svg("arrow") if cls == "btn" else ""}</a>'


def heading(sec_heading):
    if not sec_heading:
        return ""
    parts = []
    for el in sec_heading.find_all(["h1", "h2", "h3", "h4", "h5", "p"], recursive=False):
        if el.name == "p":
            if txt(el):
                parts.append(f"<p>{inner(el)}</p>")
        else:
            lvl = "h2" if el.name in ("h3", "h4") else el.name
            parts.append(f"<{lvl}>{inner(el)}</{lvl}>")
    left = " left" if "left" in (sec_heading.get("class") or []) else ""
    return f'<div class="sec-head{left}">{"".join(parts)}</div>'


# ------------------------------------------------------------------ section renderers
def hero(ctx, el):
    bg = el.find("img")
    h1, p, a = el.find("h1"), el.find("p"), el.find("a", class_="butn")
    pic = img_tag(ctx, bg["src"], "", "100vw", "hero-bg", eager=True)
    return (f'<section class="hero">{pic}<div class="wrap hero-inner"><h1>{inner(h1)}</h1>'
            f'<p class="lead">{inner(p)}</p><p>{button(a)}</p></div></section>')


def page_title(ctx, el):
    crumbs = [txt(li) for li in el.select("ul li")]
    trail = ""
    if len(crumbs) >= 2:
        trail = (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">{html.escape(crumbs[0])}</a></li>'
                 f'<li aria-current="page">{html.escape(crumbs[-1])}</li></ol></nav>')
    return (f'<section class="page-title">{img_tag(ctx, "/assets/images/header.jpg", "", "100vw", "hero-bg", eager=True)}'
            f'<div class="wrap"><h1>{inner(el.find("h1"))}</h1>{trail}</div></section>')


def clients(ctx, el):
    logos = "".join(f'<li>{img_tag(ctx, i["src"], i.get("alt", ""), "200px", "logo-img", eager=False)}</li>' for i in el.find_all("img"))
    return f'<section class="logos hide-sm" aria-label="Professional affiliations"><div class="wrap"><ul>{logos}</ul></div></section>'


def cta_band(ctx, el):
    h = el.select_one(".section-heading")
    a = el.find("a", class_="butn")
    return (f'<section class="band"><div class="wrap band-inner"><div><h2>{inner(h.find(["h3", "h4"]))}</h2>'
            f'<p>{inner(h.find("p"))}</p></div><p>{button(a, "btn btn-light")}</p></div></section>')


def feature_card(ctx, el):
    ic = next((c for c in el.find("i").get("class", []) if c in ICONS), None) if el.find("i") else None
    icon = f'<span class="card-icon">{svg(ic)}</span>' if ic else ""
    return (f'<div class="card">{icon}'
            f'<h3>{inner(el.find("h4"))}</h3><p>{inner(el.find("p"))}</p></div>')


def price_card(ctx, el):
    hi = " featured" if "highlight" in el.get("class", []) else ""
    price = el.select_one(".pricing-list-price")
    amount = txt(price.find("h2")).replace("$", "").strip()
    unit = txt(price.find("span"))
    items = "".join(f"<li>{inner(li)}</li>" for li in el.select("ul > li"))
    items = re.sub(r"(<br/>\s*)+</li>", "</li>", items)
    a = el.select_one(".pricing-list-button a")
    return (f'<div class="price-card{hi}"><span class="card-icon">{svg("icon-briefcase")}</span><h3>{inner(el.find("h4"))}</h3>'
            f'<p class="price"><sup>$</sup>{html.escape(amount)}<span>{html.escape(unit)}</span></p>'
            f'<ul>{items}</ul>{button(a, "btn btn-block") if a else ""}</div>')


def project_card(ctx, el):
    img = el.select_one(".project-grid-img img")
    ov = el.select_one(".project-grid-overlay")
    return (f'<article class="project">{img_tag(ctx, img["src"], txt(ov.find("h4")), "(max-width: 780px) 100vw, 380px", "project-img", eager=False)}'
            f'<div class="project-body"><h3>{html.escape(txt(ov.find("h4")))}</h3><p>{inner(ov.find("p"))}</p></div></article>')


def faq(ctx, el):
    cols = []
    for acc in el.select(".accordion-style"):
        items = "".join(
            f'<details><summary>{html.escape(txt(card.find("button")))}{svg("chev", "i chev")}</summary>'
            f'<div class="answer">{inner(card.select_one(".card-body"))}</div></details>'
            for card in acc.select(".card"))
        cols.append(f'<div class="faq-col">{items}</div>')
    return (f'<section class="sec tone-mist"><div class="wrap">{heading(el.select_one(".section-heading"))}'
            f'<div class="faq">{"".join(cols)}</div></div></section>')


def contact_section(ctx, el):
    form = el.find("form")
    fields = []
    for inp in form.find_all(["input", "textarea"]):
        if inp.get("type") == "hidden" or inp.get("type") == "submit" or inp.get("name") == "bot-field":
            continue
        name, ph = inp["name"], (inp.get("placeholder") or "").rstrip(":")
        full = " full" if inp.name == "textarea" else ""
        typ = inp.get("type", "text")
        auto = {"fullname": "name", "youremail": "email", "phone": "tel"}.get(name, "off")
        ctrl = (f'<textarea id="f-{name}" name="{name}" rows="6"></textarea>' if inp.name == "textarea"
                else f'<input id="f-{name}" name="{name}" type="{typ}" autocomplete="{auto}"{" required" if inp.has_attr("required") else ""}>')
        fields.append(f'<p class="field{full}"><label for="f-{name}">{html.escape(ph)}</label>{ctrl}</p>')
    submit = form.find("input", type="submit")
    form_html = (f'<form class="form-card" name="contact" method="POST" action="/contact/thanks/" data-netlify="true" netlify-honeypot="bot-field">'
                 f'<input type="hidden" name="form-name" value="contact"><p class="hp"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'
                 f'<div class="fields">{"".join(fields)}</div><button class="btn" type="submit">{html.escape(submit["value"])}</button></form>')
    form_head = form.find_previous(["h3", "h4"])
    blocks = []
    for sec in (el.select_one(".contact-info-box") or el).select(".contact-info-section"):
        h = txt(sec.find("h4"))
        items = []
        for li in sec.select("ul > li"):
            if not txt(li):
                continue
            i = li.find("i")
            ic = next((c for c in i.get("class", []) if c in ICONS), None) if i else None
            icon = f'<span class="card-icon">{svg(ic)}</span>' if ic else ""
            items.append(f"<li>{icon}<div>{inner(li)}</div></li>")
        if items:
            blocks.append((f"<h3>{html.escape(h)}</h3>" if h else "") + f"<ul>{''.join(items)}</ul>")
        elif h:
            blocks.append(f"<h2>{html.escape(h)}</h2>")
    return (f'<section class="sec"><div class="wrap contact-grid"><div><h2>{inner(form_head)}</h2>{form_html}</div>'
            f'<aside class="contact-info">{"".join(blocks)}</aside></div></section>')


def split_section(ctx, el):
    """Image column + text column (founder quote on home, company intro on About)."""
    row = el.select_one(".row")
    cols = row.find_all("div", recursive=False)
    img_col = next(c for c in cols if c.find("img"))
    txt_col = next(c for c in cols if c is not img_col)
    imgs = "".join(img_tag(ctx, i["src"], i.get("alt", ""), "(max-width: 780px) 100vw, 420px", "media", eager=False) for i in img_col.find_all("img"))
    h = txt_col.select_one(".section-heading")
    quote = h.find(["h3", "h4"]) if h else None
    is_quote = quote is not None and txt(quote).startswith(('"', "“"))
    head = (f'<blockquote class="pull">{inner(quote)}</blockquote>' if is_quote else f"<h2>{inner(quote)}</h2>") if quote else ""
    body = "".join(f"<p>{inner(p)}</p>" for p in txt_col.find_all("p") if txt(p) and not p.find_parent(class_="section-heading"))
    lis = "".join(f"<li>{inner(li)}</li>" for li in txt_col.select("ul li"))
    a = txt_col.find("a", class_="butn")
    return (f'<section class="sec"><div class="wrap split"><div class="split-media">{imgs}</div>'
            f'<div class="split-text">{head}<div class="prose">{body}</div>{f"<ul>{lis}</ul>" if lis else ""}'
            f'{f"<p>{button(a)}</p>" if a else ""}</div></div></section>')


def team(ctx, el):
    members = []
    for m in el.select(".team-style1"):
        img = m.find("img")
        info = [d for d in m.find_all("div") if not d.find("div") and not d.find("img") and txt(d)]
        name, role = (info + [None, None])[:2]
        members.append(f'<figure class="member">{img_tag(ctx, img["src"], txt(name), "(max-width: 780px) 90vw, 360px", "member-img", eager=False)}'
                       f'<figcaption><h3>{html.escape(txt(name))}</h3><p>{html.escape(txt(role))}</p></figcaption></figure>')
    return (f'<section class="sec tone-mist"><div class="wrap">{heading(el.select_one(".section-heading"))}'
            f'<div class="team">{"".join(members)}</div></div></section>')


def generic(ctx, el, tone=""):
    parts = [heading(el.select_one(".section-heading"))]
    feats = el.select(".feature-box-01")
    prices = el.select(".pricing-list")
    projects = el.select(".project-grid")
    if feats:
        parts.append(f'<div class="cards cards-3">{"".join(feature_card(ctx, f) for f in feats)}</div>')
    if prices:
        parts.append(f'<div class="cards cards-{min(len(prices), 3)} pricing">{"".join(price_card(ctx, p) for p in prices)}</div>')
    if projects:
        parts.append(f'<div class="cards cards-3">{"".join(project_card(ctx, p) for p in projects)}</div>')
    return f'<section class="sec {tone}"><div class="wrap">{"".join(parts)}</div></section>'


def render_page(ctx, soup):
    out = []
    main = soup.select_one(".main-wrapper")
    for el in main.find_all(["section", "div"], recursive=False):
        cls = el.get("class", [])
        if el.select_one(".rev_slider"):
            out.append(hero(ctx, el))
        elif "d-block" in cls and "d-lg-none" in cls:
            continue  # mobile copy of the hero; the new hero is responsive
        elif "section-clients" in cls:
            out.append(clients(ctx, el))
        elif "page-title-section" in cls:
            out.append(page_title(ctx, el))
        elif "bg-black" in cls:
            out.append(cta_band(ctx, el))
        elif el.select_one(".accordion-style"):
            out.append(faq(ctx, el))
        elif el.find("form"):
            out.append(contact_section(ctx, el))
        elif el.select_one(".team-style1"):
            out.append(team(ctx, el))
        elif el.select_one(".feature-box-01, .pricing-list, .project-grid"):
            out.append(generic(ctx, el, "tone-mist" if "bg-grey" in cls else ""))
        elif el.find("img") and el.select_one(".section-heading"):
            out.append(split_section(ctx, el))
        elif el.select_one(".section-heading"):
            out.append(generic(ctx, el, "tone-mist" if "bg-grey" in cls else ""))
    return "\n".join(out)


# ------------------------------------------------------------------ shell
CSS = (HERE / "site.css").read_text(encoding="utf-8")
JS = (HERE / "site.js").read_text(encoding="utf-8")
NAV = [("/services/", "Services"), ("/about/", "About"), ("/contact/", "Contact")]


def head_tags(soup):
    keep = [str(soup.title)]
    for m in soup.head.find_all("meta"):
        if m.get("charset") or m.get("http-equiv") or m.get("name") in ("viewport", "generator"):
            continue
        keep.append(str(m))
    can = soup.head.find("link", rel="canonical")
    if can:
        keep.append(str(can))
    keep += [str(s) for s in soup.find_all("script", type="application/ld+json")]
    return "\n  ".join(keep)


def shell(soup, body, ctx, active, extra_head=""):
    preload = ""
    if ctx.preload:
        preload = (f'\n  <link rel="preload" as="image" href="{ctx.preload["src"]}" imagesrcset="{ctx.preload["srcset"]}" '
                   f'imagesizes="{ctx.preload_sizes}" fetchpriority="high">')
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{h}"{cur if h == active else ""}>{l}</a></li>' for h, l in NAV)
    logo = variants("/assets/images/logo.png")
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {head_tags(soup)}{extra_head}
  <link rel="icon" href="/img/favicon.png">
  <link rel="preload" href="/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>{preload}
  <style>{CSS}</style>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-head">
    <div class="wrap head-inner">
      <a class="logo" href="/" aria-label="Xandra LLC home"><img src="/img/logo-480.webp" srcset="{logo["srcset"]}" sizes="96px" width="{logo["w"]}" height="{logo["h"]}" alt="Xandra LLC"></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu">{svg("menu")}</button>
      <nav id="nav" class="nav" aria-label="Main"><ul>{nav}</ul></nav>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="site-foot"><div class="wrap"><p>&copy;2026 Xandra, LLC</p></div></footer>
  <script>window.XANDRA={{gtag:"{GTAG_ID}",hj:{HOTJAR_ID}}};{JS}</script>
</body>
</html>
'''


# ------------------------------------------------------------------ build
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "fonts").mkdir(parents=True)
shutil.copy2(HERE / "fonts/montserrat-latin.woff2", OUT / "fonts/montserrat-latin.woff2")
IMG.mkdir(parents=True, exist_ok=True)
shutil.copy2(SRC / "assets/images/favicon.png", IMG / "favicon.png")
variants("/assets/images/logo.png")

for slug in PAGES:
    soup = BeautifulSoup((SRC / slug / "index.html").read_text(encoding="utf-8"), "html.parser")
    ctx = Ctx()
    body = render_page(ctx, soup)
    active = f"/{slug}/" if slug else "/"
    dest = OUT / slug / "index.html" if slug else OUT / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(shell(soup, body, ctx, active), encoding="utf-8")

    if slug == "contact":
        # Thank-you page shown after the Netlify form posts: same page, form replaced by a message.
        tctx = Ctx()
        thanks = render_page(tctx, soup)
        thanks = re.sub(r'<form class="form-card".*?</form>',
                        '<div class="form-card thanks"><h3>Thank you!</h3><p>Your message has been sent. We&rsquo;ll be in touch shortly.</p>'
                        f'<p><a class="btn" href="/">Back to home{svg("arrow")}</a></p></div>', thanks, flags=re.S)
        page = shell(soup, thanks, tctx, "/contact/", '\n  <meta name="robots" content="noindex">')
        page = re.sub(r'<link rel="canonical"[^>]*>\s*', "", page)
        (OUT / "contact/thanks").mkdir(parents=True, exist_ok=True)
        (OUT / "contact/thanks/index.html").write_text(page, encoding="utf-8")

# Social share images referenced by og/twitter tags.
for rel in ["assets/uploads/2021/06/facebook-og-image.jpg", "assets/uploads/2021/06/twitter-card.png"]:
    if (SRC / rel).exists():
        (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / rel, OUT / rel)

(HERE.parent / "netlify.toml").write_text('''[build]
  publish = "site"

[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/fonts/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[redirects]]
  from = "/wp-admin/*"
  to = "/"
  status = 301

[[redirects]]
  from = "/wp-login.php"
  to = "/"
  status = 301
''', encoding="utf-8")

size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"built {len(list(OUT.rglob('index.html')))} pages, {len(list(IMG.glob('*')))} images, {size / 1024:.0f} KiB")
