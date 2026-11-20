# -*- coding: utf-8 -*-
"""Model page template for bike.rubiworkshop.com/<slug>/.

Every model page is rendered from data/pages/<slug>.json by tools/build.py.
Section order follows the Bastion Archetype page (SST layout + BMW S 1000 RR order):
hero, band, statement, highlights, figures, quote, technology, configure, geometry,
process, gallery, standard, specs, more, close, notes.
Every section except hero and specs is optional: leave the key out and it is not rendered.

Text fields may contain simple inline HTML (<sup>, <br>, <em>). Attributes are escaped.
Image values: {"src": "/images/x.jpg" or "https://...", "alt": "...", "w": 1920, "h": 1280, "pos": "50% 60%"}
"""
import html
import json

SITE = "https://bike.rubiworkshop.com"
GA_ID = "G-JL1KFMCJLL"
CONSULT = "https://rubiworkshop.com/models#rwc-form"
SHOWROOM = "https://rubiworkshop.com/showroom"


def a(s):
    return html.escape(str(s), quote=True)


def absu(src):
    return SITE + src if src.startswith("/") else src


def img(i, lazy=True, extra=""):
    if not i:
        return ""
    wh = f' width="{i["w"]}" height="{i["h"]}"' if i.get("w") and i.get("h") else ""
    style = f' style="object-position:{a(i["pos"])}"' if i.get("pos") else ""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    ref = ' referrerpolicy="no-referrer"' if i["src"].startswith("http") else ""
    return f'<img src="{a(i["src"])}" alt="{a(i.get("alt", ""))}"{wh}{style}{load}{ref}{extra}>'


def plate(i, cls="plate", lazy=True, style=""):
    st = f' style="{style}"' if style else ""
    return f'<figure class="{cls}"{st}>{img(i, lazy)}</figure>'


def title(t, sub=None, tag="h2"):
    s = f'<span class="sub">{sub}</span>' if sub else ""
    return f'<{tag} class="title">{t}{s}</{tag}>'


def hd(d, extra_style=""):
    st = f' style="{extra_style}"' if extra_style else ""
    eb = f'<p class="eyebrow">{d["eyebrow"]}</p>' if d.get("eyebrow") else ""
    desc = f'<p class="desc">{d["desc"]}</p>' if d.get("desc") else ""
    return f'<div class="hd"{st}>{eb}{title(d["title"], d.get("sub"))}{desc}</div>'


def stats(items):
    out = []
    for s in items:
        cur = f'<span class="cur">{s["cur"]}</span>' if s.get("cur") else ""
        out.append(f'<div class="stat"><div class="k">{s["k"]}</div><div class="v">{cur}{s["v"]}</div></div>')
    return '<div class="stats">' + "".join(out) + "</div>"


def btn(label, href, solid=False, consult=False, ext=False):
    cls = "btn solid" if solid else "btn"
    dc = " data-consult" if consult else ""
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return f'<a class="{cls}" href="{a(href)}"{dc}{tgt}>{label}</a>'


# ---------------------------------------------------------------- sections

def sec_hero(p):
    h = p["hero"]
    style = "background:#0d0d0d" if h.get("dark") else ""
    price = ""
    if h.get("price"):
        note = f'<small>{h["priceNote"]}</small>' if h.get("priceNote") else ""
        price = f'<p class="price">{h["price"]}{note}</p>'
    return f"""<section id="overview" class="hero">
    {plate(h["img"], lazy=False, style=style)}
    <div class="wrap hero-body">
      <div>
        <p class="eyebrow badge"><b>{p["badge"]}</b> {p["category"]} · {p["brandName"]}</p>
        <h1>{p["name"]}</h1>
        <p class="sub">{p["ko"]}</p>
        {price}
        <p class="desc">{h["desc"]}</p>
        <div class="acts">
          {btn("상담 신청하기", CONSULT, solid=True, consult=True)}
          {btn("사양 보기", "#specs")}
        </div>
      </div>
      {stats(h["stats"])}
    </div>
  </section>"""


def sec_band(p):
    if not p.get("band"):
        return ""
    return f"""<div class="band">
    <div class="wrap">
      <p>{p["band"]}</p>
      <a class="link" href="{SHOWROOM}">쇼룸 안내</a>
    </div>
  </div>"""


def sec_statement(p):
    s = p.get("statement")
    if not s:
        return ""
    acts = ""
    if s.get("acts", True):
        links = [btn("하이라이트 보기", "#highlights")] if p.get("highlights") else []
        if p.get("process"):
            links.append(btn(p["process"].get("tab", "제작 과정"), "#process"))
        elif p.get("configure"):
            links.append(btn("구성 보기", "#configure"))
        acts = '<div class="acts">' + "".join(links) + "</div>" if links else ""
    fig = plate(s["img"]) if s.get("img") else ""
    return f"""<div class="wrap sec">
    <div class="statement"{'' if fig else ' style="grid-template-columns:1fr"'}>
      <div>
        <p class="eyebrow" style="margin-bottom:14px">{s.get("eyebrow", "")}</p>
        {title(s["title"], s.get("sub"))}
        <p class="desc muted" style="margin-top:20px;max-width:52ch">{s["desc"]}</p>
        {acts}
      </div>
      {fig}
    </div>
  </div>"""


def sec_highlights(p):
    h = p.get("highlights")
    if not h:
        return ""
    rows = []
    for i, r in enumerate(h["rows"], 1):
        more = ""
        if r.get("more"):
            more = f'<details class="more-text"><summary>더 보기</summary><p class="desc">{r["more"]}</p></details>'
        sub = f'<span class="sub">{r["s"]}</span>' if r.get("s") else ""
        rows.append(f"""<article class="hl-row">
        {plate(r["img"])}
        <div>
          <p class="n">{i:02d}</p>
          <h3>{r["t"]}{sub}</h3>
          <p class="desc">{r["desc"]}</p>
          {more}
        </div>
      </article>""")
    head = dict(h, eyebrow=h.get("eyebrow", "Highlights"))
    top = "" if p.get("statement") else ""
    return f"""<section id="highlights" class="wrap sec"{' style="padding-top:0"' if p.get("statement") else top}>
    {hd(head)}
    <div class="hl">
      {"".join(rows)}
    </div>
  </section>"""


def sec_figures(p):
    f = p.get("figures")
    if not f:
        return ""
    items = "".join(
        f'<div class="num"><div class="big">{x["big"]}<small>{x.get("unit", "")}</small></div><div class="k">{x["k"]}</div></div>'
        for x in f["items"])
    four = " four" if len(f["items"]) == 4 else ""
    return f"""<section id="figures" class="tint">
    <div class="wrap sec">
      <div class="hd" style="margin-bottom:44px">{title(f.get("title", p["nameShort"]), f.get("sub", "숫자로 보는 " + p["koShort"]))}</div>
      <div class="nums{four}">{items}</div>
    </div>
  </section>"""


def sec_quote(p):
    q = p.get("quote")
    if not q:
        return ""
    return f"""<div class="wrap sec">
    <figure class="quote" style="margin:0">
      <blockquote>“{q["text"]}”</blockquote>
      <cite>{q["cite"]}</cite>
    </figure>
  </div>"""


def sec_technology(p):
    t = p.get("technology")
    if not t:
        return ""
    hot = all("x" in i and "y" in i for i in t["items"]) and t.get("img")
    dots, lis = [], []
    for n, i in enumerate(t["items"]):
        on = n == 0
        sub = f'<span class="s">{i["s"]}</span>' if i.get("s") else ""
        inner = f'<span class="n">{n + 1:02d}</span><span class="t">{i["t"]}</span>{sub}<span class="d">{i["d"]}</span>'
        if hot:
            dots.append(f'<button type="button" class="hot{" on" if on else ""}" data-f="{n}" data-x="{i["x"]}" data-y="{i["y"]}" aria-label="{a(i["t"])}">{n + 1}</button>')
            lis.append(f'<li><button type="button"{" class=\"on\"" if on else ""} data-f="{n}" aria-pressed="{"true" if on else "false"}">{inner}</button></li>')
        else:
            lis.append(f'<li><div class="fitem">{inner}</div></li>')
    fig = ""
    if t.get("img"):
        ratio = t.get("ratio", "3/2")
        bg = "#0d0d0d" if t.get("dark") else ""
        style = f"aspect-ratio:{ratio}" + (f";background:{bg}" if bg else "")
        fig = f'<figure class="plate" style="{style}">{img(t["img"])}{"".join(dots)}</figure>'
    cols = len(t["items"])
    return f"""<section id="technology" class="wrap feat" style="padding-bottom:72px"{' data-hotspots' if hot else ''}>
    {hd(dict(t, eyebrow=t.get("eyebrow", "Technology")))}
    {fig}
    <ul class="flist c{cols}">
      {"".join(lis)}
    </ul>
  </section>"""


def sec_configure(p):
    c = p.get("configure")
    if not c:
        return ""
    pk = []
    for x in c["pkgs"]:
        im = plate(x["img"]) if x.get("img") else ""
        lst = "<ul>" + "".join(f"<li>{l}</li>" for l in x["list"]) + "</ul>" if x.get("list") else ""
        para = f'<p>{x["p"]}</p>' if x.get("p") else ""
        price = f'<p class="pp">{x["price"]}</p>' if x.get("price") else ""
        pk.append(f'<div class="pkg{" has-img" if im else ""}">{im}<p class="eyebrow">{x.get("eyebrow", "")}</p><h3>{x["t"]}</h3>{para}{lst}{price}</div>')
    n = len(c["pkgs"])
    grid = " four" if n % 4 == 0 else (" three" if n % 3 == 0 else "")
    return f"""<section id="configure" class="tint">
    <div class="wrap sec">
      {hd(dict(c, eyebrow=c.get("eyebrow", "Configure")))}
      <div class="pkgs{grid}">
        {"".join(pk)}
      </div>
      <div class="acts" style="margin-top:36px">
        {btn(c.get("cta", "이 구성으로 상담하기"), CONSULT, consult=True)}
      </div>
    </div>
  </section>"""


def sec_geometry(p):
    g = p.get("geometry")
    if not g:
        return ""
    head = "".join(f"<th scope=\"col\">{s}</th>" for s in g["sizes"])
    rows = "".join(
        f'<tr><th scope="row">{r[0]}</th>' + "".join(f"<td>{v}</td>" for v in r[1:]) + "</tr>"
        for r in g["rows"])
    note = f'<p class="gnote">{g["note"]}</p>' if g.get("note") else ""
    return f"""<section id="geometry" class="wrap sec">
    {hd(dict(eyebrow="Fit & Geometry", title=g.get("title", "Geometry"), sub=g.get("sub", "지오메트리"), desc=g.get("desc")))}
    <div class="geo" tabindex="0">
      <table>
        <thead><tr><th scope="col">{g.get("unit", "단위 mm, 각도 °")}</th>{head}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    {note}
  </section>"""


def sec_process(p):
    pr = p.get("process")
    if not pr:
        return ""
    steps = []
    for i, s in enumerate(pr["steps"], 1):
        im = plate(s["img"]) if s.get("img") else ""
        steps.append(f'<article class="step">{im}<p class="n">{i:02d}</p><h3>{s["t"]}</h3><p>{s["p"]}</p></article>')
    cls = "steps" + (" noimg" if not any(s.get("img") for s in pr["steps"]) else "")
    return f"""<section id="process" class="wrap sec">
    {hd(dict(pr, eyebrow=pr.get("eyebrow", "Process")))}
    <div class="{cls}">
      {"".join(steps)}
    </div>
  </section>"""


def sec_gallery(p):
    g = p.get("gallery")
    if not g:
        return ""
    figs = "".join(plate(i) for i in g)
    return f"""<section id="gallery" class="wrap sec" style="padding-top:0" data-gallery="{a(p["slug"])}">
    <div class="ghead">
      {title("Gallery", "갤러리")}
      <div class="gnav">
        <button type="button" data-prev aria-label="이전 사진"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M10 3L5 8l5 5"/></svg></button>
        <button type="button" data-next aria-label="다음 사진"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 3l5 5-5 5"/></svg></button>
      </div>
    </div>
    <div class="gallery" tabindex="0">
      {figs}
    </div>
    <div class="gcount">1 / {len(g)}</div>
  </section>"""


def sec_standard(p):
    s = p.get("standard")
    if not s:
        return ""
    items = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{x["t"]}</summary><div class="body">{x["body"]}</div></details>'
        for i, x in enumerate(s))
    return f"""<div class="wrap sec std" style="padding-top:0">
    <div class="hd">{title("Standard", "모든 " + p["koShort"] + "에 포함됩니다")}</div>
    <div class="acc">{items}</div>
  </div>"""


def sec_specs(p):
    s = p["specs"]
    groups = s.get("groups") or [{"rows": s["rows"]}]
    blocks = []
    for g in groups:
        h = f'<h3 class="spec-h">{g["t"]}</h3>' if g.get("t") else ""
        rows = "".join(f"<div><dt>{r[0]}</dt><dd>{r[1]}</dd></div>" for r in g["rows"])
        blocks.append(f'{h}<dl class="spec">{rows}</dl>')
    prices = "".join(
        f'<div><span class="eyebrow">{x.get("eyebrow", "")}</span><b>{x["v"]}<small>{x.get("unit", "")}</small></b><span class="eyebrow">{x.get("note", "")}</span></div>'
        for x in s.get("prices", []))
    side = f'<div class="side"><h3>가격{s.get("priceSup", "")}</h3><div class="g">{prices}</div></div>' if prices else ""
    return f"""<section id="specs" class="wrap sec specs"{' style="padding-top:0"' if not p.get("geometry") else ''}>
    <div class="specs-grid{'' if side else ' one'}">
      <div>
        <div class="hd">{title("Specifications", "사양")}</div>
        {"".join(blocks)}
      </div>
      {side}
    </div>
  </section>"""


def sec_more(p, more_items):
    if not more_items:
        return ""
    m = p.get("more", {})
    cards = []
    for x in more_items[:3]:
        ext = ' target="_blank" rel="noopener"' if x["href"].startswith("http") else ""
        cards.append(f"""<a class="card" href="{a(x["href"])}"{ext}>
          {plate(x["img"])}
          <p class="eyebrow">{x["eyebrow"]}</p><h3>{x["t"]}</h3>
          <p>{x["p"]}</p>
          <span class="go">자세히 보기</span>
        </a>""")
    return f"""<section id="more" class="tint">
    <div class="wrap sec">
      {hd(dict(eyebrow=m.get("eyebrow", "More from " + p["brandShort"]), title=m.get("title", "같은 브랜드의 다른 모델"), sub=m.get("sub")))}
      <div class="cards">
        {"".join(cards)}
      </div>
    </div>
  </section>"""


def sec_close(p):
    c = p.get("close", {})
    links = [btn("상담 신청하기", CONSULT, solid=True, consult=True), btn("전체 모델 보기", "/")]
    for l in p.get("links", []):
        links.append(btn(l["label"], l["href"], ext=l["href"].startswith("http")))
    st = stats(c["stats"]) if c.get("stats") else ""
    return f"""<div class="close">
    <div class="wrap sec">
      <div class="hd">{title(p["name"], c.get("sub", "반포 쇼룸에서 상담하세요."))}</div>
      {st}
      <div class="acts" style="margin-top:36px">
        {"".join(links)}
      </div>
    </div>
  </div>"""


def sec_notes(p):
    n = p.get("notes")
    if not n:
        return ""
    ol = "<ol>" + "".join(f"<li>{x}</li>" for x in n.get("ol", [])) + "</ol>" if n.get("ol") else ""
    ul = "<ul>" + "".join(f"<li>{x}</li>" for x in n.get("ul", [])) + "</ul>" if n.get("ul") else ""
    return f"""<div class="notes">
    <div class="wrap">
      {ol}{ul}
    </div>
  </div>"""


TABS = [("overview", "개요", None), ("highlights", "하이라이트", "highlights"), ("technology", "테크놀로지", "technology"),
        ("configure", "구성", "configure"), ("geometry", "지오메트리", "geometry"), ("process", "제작", "process"),
        ("specs", "사양", None)]


def tabs(p):
    out = []
    for sid, label, key in TABS:
        if key and not p.get(key):
            continue
        if sid == "process":
            label = p["process"].get("tab", label)
        if sid == "technology":
            label = p["technology"].get("tab", label)
        out.append(f'<a href="#{sid}"{" class=\"on\"" if sid == "overview" else ""}>{label}</a>')
    return "\n      ".join(out)


# ---------------------------------------------------------------- head

def ld(p):
    url = f"{SITE}/{p['slug']}/"
    images = [absu(p["hero"]["img"]["src"])] + [absu(i["src"]) for i in (p.get("gallery") or [])[:3]]
    seen, imgs = set(), []
    for i in images:
        if i not in seen:
            seen.add(i)
            imgs.append(i)
    product = {
        "@type": "Product", "@id": url + "#product", "name": p["name"], "alternateName": p["ko"],
        "description": p["seo"]["product"], "image": imgs, "category": p.get("ldCategory", "자전거"),
        "brand": {"@type": "Brand", "name": p["brandName"]},
    }
    if p.get("manufacturerUrl"):
        product["manufacturer"] = {"@type": "Organization", "name": p["brandName"], "url": p["manufacturerUrl"]}
    off = p.get("offers")
    if off:
        if off.get("low") and off.get("high") and off["low"] != off["high"]:
            product["offers"] = {"@type": "AggregateOffer", "url": url, "lowPrice": str(off["low"]),
                                 "highPrice": str(off["high"]), "priceCurrency": "KRW",
                                 "offerCount": str(off.get("count", 2)), "seller": {"@id": "https://rubiworkshop.com/#store"}}
        else:
            product["offers"] = {"@type": "Offer", "url": url, "price": str(off.get("low") or off.get("high")),
                                 "priceCurrency": "KRW", "availability": "https://schema.org/PreOrder" if off.get("preorder") else "https://schema.org/InStock",
                                 "seller": {"@id": "https://rubiworkshop.com/#store"}}
    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["seo"]["title"], "inLanguage": "ko-KR",
         "about": {"@id": url + "#product"}, "breadcrumb": {"@id": url + "#breadcrumb"},
         "publisher": {"@id": "https://rubiworkshop.com/#store"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bikes", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": p["brandShort"], "item": f"{SITE}/#{p['brand']}"},
            {"@type": "ListItem", "position": 3, "name": p["nameShort"], "item": url}]},
        product,
        STORE,
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


STORE = {
    "@type": "BicycleStore", "@id": "https://rubiworkshop.com/#store", "name": "루비워크샵", "alternateName": "Rubi Workshop",
    "url": "https://rubiworkshop.com/", "telephone": "1551-5320",
    "address": {"@type": "PostalAddress", "streetAddress": "신반포로 320 루비빌딩", "addressLocality": "서초구",
                "addressRegion": "서울특별시", "addressCountry": "KR"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "12:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "15:30"}],
    "sameAs": ["https://www.instagram.com/rubi.workshop/"],
}


def render(p, more_items):
    url = f"{SITE}/{p['slug']}/"
    seo = p["seo"]
    og = p["hero"]["img"]
    ogwh = f'\n<meta property="og:image:width" content="{og["w"]}">\n<meta property="og:image:height" content="{og["h"]}">' if og.get("w") else ""
    body = "\n\n  ".join(x for x in [
        "<!-- 1. Hero -->\n  " + sec_hero(p), sec_band(p), sec_statement(p), sec_highlights(p), sec_figures(p), sec_quote(p),
        sec_technology(p), sec_configure(p), sec_geometry(p), sec_process(p), sec_gallery(p), sec_standard(p),
        sec_specs(p), sec_more(p, more_items), sec_close(p), sec_notes(p)] if x)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<!-- 이 파일은 tools/build.py 가 data/pages/{p['slug']}.json 으로 만듭니다. 직접 고치지 말고 JSON을 고친 뒤 빌드하세요. -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}', {{ content_group: 'model' }});
  var GA_ID = '{GA_ID}'; // used by the shared GA4 event script in /assets/site.js
</script>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{a(seo["title"])}</title>
<meta name="description" content="{a(seo["description"])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#fafaf9">
<!-- 네이버 서치어드바이저, 구글 서치 콘솔 소유 확인 메타 태그는 이 자리에 붙여 넣습니다 -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="루비워크샵">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{a(seo["ogTitle"])}">
<meta property="og:description" content="{a(seo["og"])}">
<meta property="og:image" content="{a(absu(og["src"]))}">{ogwh}
<meta property="og:image:alt" content="{a(og.get("alt", ""))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{a(seo["ogTitle"])}">
<meta name="twitter:description" content="{a(seo["og"])}">
<meta name="twitter:image" content="{a(absu(og["src"]))}">
<script type="application/ld+json">
{ld(p)}
</script>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body data-model="{a(p["slug"])}" style="--accent:{a(p.get("accent", "#a8834a"))}">
<a class="skip" href="#main">본문으로 건너뛰기</a>

<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="루비워크샵 Bikes">
      <span class="logo-word">Rubi Workshop</span>
      <span class="logo-sub">Bikes</span>
    </a>
    <nav class="gnav-top" aria-label="사이트">
      <a href="/">전체 모델</a>
      <a href="/#{p["brand"]}" class="opt">{p["brandShort"]}</a>
      <a href="https://rubiworkshop.com" class="opt">rubiworkshop.com</a>
    </nav>
  </div>
</header>

<nav class="modelbar" aria-label="{a(p["name"])}">
  <div class="wrap">
    <span class="name">{p["name"]}</span>
    <div class="tabs">
      {tabs(p)}
    </div>
    {btn("상담 신청하기", CONSULT, consult=True)}
  </div>
</nav>

<main id="main">
  {body}
</main>

<footer>
  <div class="wrap">
    <div><p class="eyebrow">{p.get("footerRole", "한국 공식 디스트리뷰터")}</p><p>루비워크샵, 서울 반포</p><p>서울시 서초구 신반포로 320 루비빌딩</p></div>
    <div><p class="eyebrow">상담</p><p style="user-select:all">1551-5320</p><p>월~금 12:00~19:00, 토 10:00~15:30</p></div>
    <div><p class="eyebrow">Online</p><p><a href="https://rubiworkshop.com" target="_blank" rel="noopener">rubiworkshop.com</a></p><p><a href="https://instagram.com/rubi.workshop" target="_blank" rel="noopener">@rubi.workshop</a></p></div>
    <div class="copy">{p.get("footerCopy", p["brandName"] + " · Rubi Company, Seoul")}</div>
  </div>
</footer>

<script src="/assets/site.js" defer></script>
</body>
</html>
"""
