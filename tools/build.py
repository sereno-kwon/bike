#!/usr/bin/env python3
"""bike.rubiworkshop.com builder.

data/models.json 하나를 원본으로 삼아 아래를 다시 씁니다.
  - index.html 의 <!-- build:filters --> ... <!-- /build:filters --> 브랜드 필터
  - index.html 의 <!-- build:lineup --> ... <!-- /build:lineup --> 브랜드별 모델 목록
  - index.html 의 <!-- build:itemlist --> ... <!-- /build:itemlist --> 구조화 데이터(ItemList)
  - sitemap.xml (루트 + page: true 인 모델 상세 페이지)

사용법: python3 tools/build.py          # 다시 쓰기
        python3 tools/build.py --check  # 바뀔 내용이 있으면 실패 (CI 용)
"""
import datetime
import html
import json
import pathlib
import re
import sys

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
    page = '<span class="page">상세 페이지</span>' if m.get("page") else ""
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
    ext = ' target="_blank" rel="noopener"' if is_external(b["link"]) else ""
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
          <div class="acts"><a class="btn" href="{esc(b['link'])}"{ext}>{esc(b['linkLabel'])}</a></div>
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


def main():
    check = "--check" in sys.argv
    data = json.loads((ROOT / "data/models.json").read_text(encoding="utf-8"))
    brands = data["brands"]

    index_path = ROOT / "index.html"
    old_index = index_path.read_text(encoding="utf-8")
    new_index = replace_block(old_index, "filters", "        " + filters(brands) + "\n        ")
    new_index = replace_block(new_index, "lineup", "  " + "\n\n  ".join(brand_section(b) for b in brands) + "\n  ")
    new_index = replace_block(new_index, "itemlist", itemlist(brands))

    sm_path = ROOT / "sitemap.xml"
    old_sm = sm_path.read_text(encoding="utf-8") if sm_path.exists() else ""
    # lastmod moves to today only when index.html changes or the URL list changes,
    # so running the build twice (or --check) is stable
    m = re.search(r"<lastmod>([\d-]+)</lastmod>", old_sm)
    keep = m.group(1) if m else datetime.date.today().isoformat()
    new_sm = sitemap(brands, keep)
    if new_sm != old_sm or new_index != old_index:
        new_sm = sitemap(brands, datetime.date.today().isoformat())

    if check:
        if new_index != old_index or new_sm != old_sm:
            sys.exit("index.html 또는 sitemap.xml 이 models.json 과 다릅니다. python3 tools/build.py 를 실행하세요.")
        print("ok")
        return
    index_path.write_text(new_index, encoding="utf-8")
    sm_path.write_text(new_sm, encoding="utf-8")
    n = sum(len(b["models"]) for b in brands)
    print(f"built: {len(brands)} brands, {n} models")


if __name__ == "__main__":
    main()
