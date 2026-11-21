#!/usr/bin/env python3
"""bike.rubiworkshop.com builder.

data/models.json 하나를 원본으로 삼아 아래를 다시 씁니다.
  - index.html 의 <!-- build:filters --> ... <!-- /build:filters --> 브랜드 필터
  - index.html 의 <!-- build:lineup --> ... <!-- /build:lineup --> 브랜드별 모델 목록
  - index.html 의 <!-- build:itemlist --> ... <!-- /build:itemlist --> 구조화 데이터(ItemList)
  - sitemap.xml (루트 + page: true 인 모델 상세 페이지)

  - <slug>/index.html (data/pages/<slug>.json 이 있는 모델마다, tools/model_page.py 템플릿)
  - 404.html 의 모델 주소 목록

사용법: python3 tools/build.py          # 다시 쓰기
        python3 tools/build.py --check  # 바뀔 내용이 있으면 실패 (CI 용)
"""
import datetime
import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model_page  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://bike.rubiworkshop.com"


def esc(s):
    return html.escape(str(s), quote=True)


def is_external(url):
    return url.startswith("http")


def model_li(m):
    url = m["url"]
    ext = ' target="_blank" rel="noopener"' if is_external(url) else ""
    cats = " · ".join(esc(c) for c in m.get("cat", []))
    badge = f' <b>{esc(m["badge"])}</b>' if m.get("badge") else ""
    ko = f'<span class="sub">{esc(m["ko"])}</span>' if m.get("ko") else ""
    page = ""
    return (
        f'<li><a href="{esc(url)}"{ext} data-model="{esc(m["slug"])}">'
        f'<span class="cat">{cats}{badge}</span>'
        f'<h3>{esc(m["name"])}{ko}</h3>'
        f'<p>{esc(m["summary"])}</p>'
        f'<span class="price">{esc(m["price"])}{page}</span>'
        f"</a></li>"
    )


def brand_section(b):
    n = len(b["models"])
    count = f"{n} Model" + ("s" if n > 1 else "")
    if b.get("link"):
        ext = ' target="_blank" rel="noopener"' if is_external(b["link"]) else ""
        acts = f'<div class="acts"><a class="btn" href="{esc(b['link'])}"{ext}>{esc(b['linkLabel'])}</a></div>'
    else:
        acts = ""
    if b.get("image"):
        plate = (
            f'<figure class="plate"><img src="{esc(b["image"])}" alt="{esc(b["imageAlt"])}" '
            f'loading="lazy" decoding="async" referrerpolicy="no-referrer"></figure>'
        )
    else:
        plate = ""
    tag = f'<span class="tag">{esc(b["tag"])}</span>' if b.get("tag") else ""
    items = "\n        ".join(model_li(m) for m in b["models"])
    return f"""<section id="{esc(b['id'])}" class="brand" aria-labelledby="h-{esc(b['id'])}">
    <div class="wrap">
      <div class="brand-head{'' if b.get('image') else ' noimg'}">
        <div>
          <h2 class="title" id="h-{esc(b['id'])}">{esc(b['name'])}<span class="sub">{esc(b['ko'])}</span></h2>
          <p class="count">{count}</p>
          <p class="desc">{esc(b['desc'])}</p>
          {tag}
          {acts}
        </div>
        {plate}
      </div>
      <ul class="models">
        {items}
      </ul>
    </div>
  </section>"""


def filters(brands):
    total = sum(len(b["models"]) for b in brands)
    out = [f'<a href="#lineup" aria-current="true">All <span>{total}</span></a>']
    for b in brands:
        out.append(f'<a href="#{esc(b["id"])}">{esc(b["filter"])} <span>{len(b["models"])}</span></a>')
    return "\n        ".join(out)


def itemlist(brands):
    items, pos = [], 1
    for b in brands:
        for m in b["models"]:
            url = m["url"] if is_external(m["url"]) else SITE + m["url"]
            items.append({"@type": "ListItem", "position": pos, "url": url,
                          "name": f'{b["filter"]} {m["name"]}'})
            pos += 1
    data = {"@context": "https://schema.org", "@type": "ItemList",
            "name": "루비워크샵 상담 가능 자전거", "numberOfItems": len(items), "itemListElement": items}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>"


def replace_block(text, name, body):
    pat = re.compile(rf"(<!-- build:{name} -->)(.*?)(<!-- /build:{name} -->)", re.S)
    if not pat.search(text):
        sys.exit(f"index.html 에 build:{name} 표시가 없습니다")
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(3), text)


def sitemap(brands, today):
    urls = [SITE + "/"]
    for b in brands:
        for m in b["models"]:
            if m.get("page"):
                urls.append(SITE + m["url"])
    rows = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n  </url>" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n")


def load_pages():
    pages = {}
    for f in sorted((ROOT / "data/pages").glob("*.json")):
        pages[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    return pages


def link_models(brands, pages):
    """A model with data/pages/<slug>.json gets its own page on this site."""
    for b in brands:
        for m in b["models"]:
            if m["slug"] in pages:
                m["url"] = f"/{m['slug']}/"
                m["page"] = True


def more_items(p, brands, pages):
    flat = [(b, m) for b in brands for m in b["models"]]
    same = [(b, m) for b, m in flat if b["id"] == p["brand"] and m["slug"] != p["slug"]]
    others = [(b, m) for b, m in flat if b["id"] != p["brand"]]
    # other brands: start right after this brand in the lineup so neighbours differ per brand
    ids = [b["id"] for b in brands]
    start = ids.index(p["brand"]) if p["brand"] in ids else 0
    others.sort(key=lambda bm: (ids.index(bm[0]["id"]) - start - 1) % len(ids))
    out = []
    for b, m in same + others:
        q = pages.get(m["slug"])
        if not q:
            continue
        card = q.get("card", {}).get("img") or q["hero"]["img"]
        out.append({"href": f"/{m['slug']}/", "img": card, "eyebrow": f"{b['filter']} · {q['category']}",
                    "t": q["name"], "p": m["summary"]})
        if len(out) == 3:
            break
    return out


def main():
    check = "--check" in sys.argv
    data = json.loads((ROOT / "data/models.json").read_text(encoding="utf-8"))
    brands = data["brands"]
    pages = load_pages()
    link_models(brands, pages)

    outputs = {}
    for slug, p in pages.items():
        outputs[ROOT / slug / "index.html"] = model_page.render(p, more_items(p, brands, pages))

    index_path = ROOT / "index.html"
    old_index = index_path.read_text(encoding="utf-8")
    new_index = replace_block(old_index, "filters", "        " + filters(brands) + "\n        ")
    new_index = replace_block(new_index, "lineup", "  " + "\n\n  ".join(brand_section(b) for b in brands) + "\n  ")
    new_index = replace_block(new_index, "itemlist", itemlist(brands))
    outputs[index_path] = new_index

    p404 = ROOT / "404.html"
    old404 = p404.read_text(encoding="utf-8")
    lst = ", ".join(f"'/{s}'" for s in pages)
    outputs[p404] = re.sub(r"var pages = \[[^\]]*\];", f"var pages = [{lst}];", old404)

    sm_path = ROOT / "sitemap.xml"
    old_sm = sm_path.read_text(encoding="utf-8") if sm_path.exists() else ""
    m = re.search(r"<lastmod>([\d-]+)</lastmod>", old_sm)
    keep = m.group(1) if m else datetime.date.today().isoformat()
    changed = any((not f.exists()) or f.read_text(encoding="utf-8") != t for f, t in outputs.items())
    new_sm = sitemap(brands, keep)
    if changed or new_sm != old_sm:
        new_sm = sitemap(brands, datetime.date.today().isoformat())
    outputs[sm_path] = new_sm

    stale = [f for f, t in outputs.items() if (not f.exists()) or f.read_text(encoding="utf-8") != t]
    if check:
        if stale:
            sys.exit("다시 빌드가 필요합니다: " + ", ".join(str(f.relative_to(ROOT)) for f in stale))
        print("ok")
        return
    for f in stale:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(outputs[f], encoding="utf-8")
    n = sum(len(b["models"]) for b in brands)
    print(f"built: {len(brands)} brands, {n} models, {len(pages)} model pages, {len(stale)} files written")


if __name__ == "__main__":
    main()
