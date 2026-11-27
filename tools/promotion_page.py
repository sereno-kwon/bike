# -*- coding: utf-8 -*-
"""Monthly promotion page for bike.rubiworkshop.com/promotion/.

Rendered from data/promotion.json by tools/build.py. Section order follows the BMW Motorrad
monthly promotion page (promo2611): hero, highlight model, focus models, benefit table for every
eligible model, then the house benefit (build credit) explained, how it works, eligible brands,
build examples, terms, FAQ and contact.

Only the month, models and credit amounts change from month to month. The build credit text,
terms and FAQ live here because they stay the same.
This promotion is for customers who buy and build at Rubi Workshop. Rubi Supply dealers are not part of it.
"""
import json

from model_page import CONSULT, GA_ID, SITE, STORE, a, btn, img, plate

URL = SITE + "/promotion/"


def won(n):
    return f"{n:,}원"


def man(n):
    return f"{n // 10000:,}만원" if n % 10000 == 0 else won(n)


def max_credit(p):
    return max(m["credit"] for m in p["models"])


# ---------------------------------------------------------------- fixed copy

TERMS = [
    "{period} 결제하신 주문에 적용됩니다.",
    "루비워크샵(반포 쇼룸, 전화, 카카오톡 상담)에서 구매하시는 경우에만 적용되며, 다른 판매점에서 구매하신 자전거는 대상이 아닙니다.",
    "자전거 1대당 1회, 대상 모델과 함께 구성하는 부품에만 사용하실 수 있습니다.",
    "대상 브랜드 부품의 정가에서 차감됩니다. 공임, 다른 브랜드 부품, 의류와 용품에는 사용하실 수 없습니다.",
    "빌드를 확정할 때 한 번에 사용하며, 남은 금액은 소멸합니다. 현금 환급, 적립금 전환, 다음 구매로의 이월은 되지 않습니다.",
    "크레딧을 넘는 금액은 정상가로 결제하시면 됩니다.",
    "다른 할인이나 프로모션과 중복 적용되지 않습니다.",
    "빌드가 시작된 뒤 주문을 취소하시는 경우, 크레딧으로 장착한 부품은 정상가로 정산됩니다.",
    "재고 상황에 따라 대상 모델과 부품, 혜택이 기간 중 바뀌거나 일찍 마감될 수 있습니다.",
]

FAQ = [
    ("빌드 크레딧은 할인과 무엇이 다른가요?",
     "자전거 가격은 그대로이고, 크레딧 금액만큼 대상 브랜드 부품을 더 좋은 것으로 고르실 수 있습니다. 견적서에는 부품이 정가로 적히고, 아래에 빌드 크레딧이 따로 차감되어 받으시는 혜택이 그대로 보입니다."),
    ("프레임셋만 구매해도 받을 수 있나요?",
     "프레임셋과 함께 대상 브랜드 부품을 고르시면 됩니다. 헤드셋이나 페달처럼 한두 가지만 고르셔도 크레딧 안에서 사용하실 수 있습니다."),
    ("크레딧을 다 쓰지 못하면 어떻게 되나요?",
     "빌드를 확정할 때 한 번에 사용하는 방식이라 남은 금액은 소멸합니다. 상담에서 크레딧에 맞춰 구성을 함께 정해 드리니 걱정하지 않으셔도 됩니다."),
    ("크레딧보다 비싼 부품을 고르고 싶어요.",
     "크레딧을 넘는 금액만 정상가로 더하시면 됩니다. 휠 업그레이드처럼 크레딧을 보태 한 단계 위로 올라가는 구성도 많이 고르십니다."),
    ("이미 가지고 있는 자전거의 업그레이드에도 쓸 수 있나요?",
     "이번 프로모션 기간에 구매하시는 대상 모델의 빌드에만 사용하실 수 있습니다."),
    ("다른 브랜드 부품에도 쓸 수 있나요?",
     "빌드 크레딧은 루비워크샵이 공식 디스트리뷰터로 들여오는 대상 브랜드 부품에만 사용하실 수 있습니다. 그 밖의 부품은 정상가로 함께 구성해 드립니다."),
    ("서울이 아닌 지역에서도 받을 수 있나요?",
     "전화와 카카오톡 상담으로 빌드를 확정하셔도 같은 혜택이 적용됩니다."),
    ("다른 판매점에서 사도 같은 혜택이 있나요?",
     "이번 프로모션은 루비워크샵에서 직접 구매하고 빌드하시는 경우에만 적용됩니다."),
]

STEPS = [
    ("상담 신청", "신청서나 전화, 카카오톡으로 관심 모델을 알려주세요. 프로모션 대상 모델인지 함께 확인해 드립니다."),
    ("모델, 사이즈 확정", "타실 길과 몸에 맞춰 모델과 사이즈를 정합니다. 이때 그 모델의 빌드 크레딧 금액이 정해집니다."),
    ("부품 고르기", "대상 브랜드 부품 가운데 크레딧 안에서 업그레이드할 부품을 고릅니다. 구성 예를 참고하셔도 좋습니다."),
    ("견적서 확인", "부품은 정가로 적히고, 아래에 빌드 크레딧이 따로 차감됩니다. 크레딧을 넘는 금액만 더해집니다."),
    ("빌드, 출고", "루비워크샵에서 조립과 점검, 최종 피팅을 마친 뒤 자전거를 인도합니다."),
]

TABS = [("overview", "개요"), ("models", "대상 모델"), ("build-credit", "빌드 크레딧"), ("how", "사용 방법"),
        ("brands", "대상 브랜드"), ("examples", "구성 예"), ("terms", "유의사항"), ("faq", "자주 묻는 질문")]


# ---------------------------------------------------------------- sections

def sec_hero(p):
    h = p["hero"]
    y, mo = p["month"].split("-")
    return f"""<section id="overview" class="hero">
    <figure class="plate">{img(h["img"], lazy=False)}</figure>
    <div class="wrap hero-body">
      <div>
        <p class="eyebrow badge">Promotion <b>{y}. {int(mo)}</b></p>
        <h1>{h["title"]}<span class="sub">{h["sub"]}</span></h1>
        <p class="price">빌드 크레딧 최대 {won(max_credit(p))}<small>{p["period"]}</small></p>
      </div>
      <div>
        <p class="desc">{h["desc"]}</p>
        <div class="acts">
          {btn("상담 신청하기", CONSULT, solid=True, consult=True)}
          {btn("대상 모델 보기", "#models")}
        </div>
      </div>
    </div>
  </section>"""


def sec_band(p):
    return f"""<div class="band">
    <div class="wrap">
      <p>가격은 그대로, 부품은 한 단계 위로. 루비워크샵에서 직접 빌드하시는 분께 드리는 {p["monthLabel"]} 혜택입니다.</p>
      <a class="link" href="#build-credit">빌드 크레딧 알아보기</a>
    </div>
  </div>"""


def model_card(m, size="h3"):
    return f"""<a class="card" href="/{a(m["slug"])}/" data-ga="promotion-{a(m["slug"])}">
        {plate(m["img"])}
        <p class="eyebrow">{m["brand"]}</p>
        <{size}>{m["name"]}<span class="sub" style="font-size:inherit">{m["ko"]}</span></{size}>
        <p>{m["desc"]}</p>
        <p class="credit"><span>빌드 크레딧</span>{won(m["credit"])}</p>
        <span class="go">모델 페이지 보기</span>
      </a>"""


def sec_models(p):
    hl = p["highlight"]
    focus = "\n      ".join(model_card(m) for m in p["focus"])
    rows = []
    for m in p["models"]:
        tier = f' <b>{a(m["tier"])}</b>' if m.get("tier") else ""
        rows.append(
            f'<tr><th scope="row"><a href="/{a(m["slug"])}/">{m["name"]}</a>{tier}<span class="ko">{m["ko"]}</span></th>'
            f'<td>{m["price"]}</td><td class="c">{won(m["credit"])}</td></tr>')
    rows = "\n          ".join(rows)
    return f"""<section id="models" class="wrap sec">
    <div class="hd">
      <p class="eyebrow">{p["monthLabel"]} Highlight Model</p>
      <h2 class="title">{hl["brand"]} {hl["name"]}<span class="sub">{p["monthLabel"]}의 하이라이트 모델, {hl["ko"]}</span></h2>
    </div>
    <a class="card promo-hl" href="/{a(hl["slug"])}/" data-ga="promotion-highlight">
      {plate(hl["img"])}
      <div>
        <p class="desc">{hl["desc"]}</p>
        <div class="num"><div class="k">빌드 크레딧</div><div class="big">{hl["credit"] // 10000}<small>만원</small></div></div>
        <span class="go">모델 페이지 보기</span>
      </div>
    </a>

    <div class="hd" style="margin-top:96px">
      <p class="eyebrow">Focus Models</p>
      <h2 class="title">Focus Models<span class="sub">함께 추천하는 모델</span></h2>
    </div>
    <div class="cards two">
      {focus}
    </div>

    <div class="hd" style="margin-top:96px">
      <p class="eyebrow">All Eligible Models</p>
      <h2 class="title">모델별 빌드 크레딧<span class="sub">{p["period"]}</span></h2>
    </div>
    <div class="geo promo-table">
      <table>
        <thead><tr><th scope="col">모델</th><th scope="col">시작 가격</th><th scope="col">빌드 크레딧</th></tr></thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    <p class="gnote">시작 가격은 각 모델 페이지 기준이며, 실제 금액은 사이즈와 부품 구성에 따라 달라집니다.</p>
  </section>"""


def sec_credit(p):
    n_brands = len(p["brands"])
    return f"""<section id="build-credit" class="wrap sec" style="padding-top:0">
    <div class="statement" style="align-items:start">
      <div class="hd" style="margin:0">
        <p class="eyebrow">Build Credit</p>
        <h2 class="title">Build Credit<span class="sub">빌드 크레딧이란</span></h2>
      </div>
      <div>
        <p class="desc">빌드 크레딧은 자전거 가격을 깎아 드리는 대신, 그 금액만큼 부품을 더 좋은 것으로 고르실 수 있게 드리는 혜택입니다.</p>
        <p class="desc muted" style="margin-top:14px">커스텀 빌드는 프레임 위에 무엇을 올리느냐로 완성됩니다. 루비워크샵이 공식 디스트리뷰터로 들여오는 고키소, 쉬몰케, THM, 폴 컴포넌트, MKS 같은 부품은 한 번 달면 오래 쓰는 부품들이고, 같은 프레임이라도 이 부품들이 자전거의 인상과 쓰임을 바꿉니다. 빌드 크레딧은 그 선택을 조금 더 가볍게 해 드리기 위해 만들었습니다.</p>
      </div>
    </div>
    <div class="nums four" style="margin-top:64px">
      <div class="num"><div class="big">{max_credit(p) // 10000}<small>만원</small></div><div class="k">최대 빌드 크레딧</div></div>
      <div class="num"><div class="big">{n_brands}<small>브랜드</small></div><div class="k">크레딧을 쓸 수 있는 부품 브랜드</div></div>
      <div class="num"><div class="big">1<small>대 1회</small></div><div class="k">자전거 1대당 한 번, 빌드 확정 시 사용</div></div>
      <div class="num"><div class="big">{p["periodShort"].split("까지")[0]}<small>까지</small></div><div class="k">{p["period"]}</div></div>
    </div>
  </section>"""


def sec_how(p):
    items = "\n        ".join(
        f'<li><p class="n">{i:02d}</p><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(STEPS, 1))
    return f"""<section id="how" class="tint">
    <div class="wrap sec">
      <div class="hd">
        <p class="eyebrow">How It Works</p>
        <h2 class="title">How It Works<span class="sub">빌드 크레딧 사용 방법</span></h2>
        <p class="desc">상담에서 출고까지, 빌드 크레딧은 이렇게 쓰입니다.</p>
      </div>
      <ol class="olist three">
        {items}
      </ol>
      <div class="quote-sheet" aria-label="견적서 예시">
        <p class="eyebrow">견적서 예시</p>
        <dl>
          <div><dt>프레임셋</dt><dd>정가</dd></div>
          <div><dt>구동계, 타이어 등 기본 구성 부품</dt><dd>정가</dd></div>
          <div><dt>대상 브랜드 업그레이드 부품</dt><dd>정가</dd></div>
          <div class="minus"><dt>빌드 크레딧</dt><dd>&minus; 모델별 크레딧 금액</dd></div>
          <div class="sum"><dt>결제 금액</dt><dd>합계 &minus; 빌드 크레딧</dd></div>
        </dl>
      </div>
    </div>
  </section>"""


def sec_brands(p):
    items = []
    for b in p["brands"]:
        lis = "".join(f"<li>{x}</li>" for x in b["items"])
        items.append(f'<div class="pkg"><p class="eyebrow">{b["ko"]}</p><h3>{b["name"]}</h3><ul>{lis}</ul></div>')
    items = "\n        ".join(items)
    return f"""<section id="brands" class="wrap sec">
    <div class="hd">
      <p class="eyebrow">Eligible Brands</p>
      <h2 class="title">Eligible Brands<span class="sub">크레딧을 쓸 수 있는 부품 브랜드</span></h2>
      <p class="desc">루비워크샵이 한국 공식 디스트리뷰터로 들여오는 컴포넌트 브랜드입니다. 정가 기준으로 크레딧이 차감됩니다.</p>
    </div>
    <div class="pkgs four">
        {items}
    </div>
  </section>"""


def sec_examples(p):
    items = []
    for e in p["examples"]:
        lis = "".join(f"<li>{x}</li>" for x in e["items"])
        items.append(f'<div class="pkg"><p class="eyebrow">{e["eyebrow"]}</p><h3>{e["t"]}</h3><p>{e["p"]}</p><ul>{lis}</ul></div>')
    items = "\n        ".join(items)
    return f"""<section id="examples" class="tint">
    <div class="wrap sec">
      <div class="hd">
        <p class="eyebrow">Build Examples</p>
        <h2 class="title">Build Examples<span class="sub">이런 구성을 많이 고르십니다</span></h2>
        <p class="desc">고르기 어려우시면 아래 구성에서 시작해 보세요. 모델과 사이즈, 타실 길에 맞춰 상담에서 금액과 조합을 함께 정해 드립니다.</p>
      </div>
      <div class="pkgs four">
        {items}
      </div>
    </div>
  </section>"""


def sec_terms(p):
    items = "\n      ".join(f"<li>{t.format(period=p['period'])}</li>" for t in TERMS)
    return f"""<section id="terms" class="wrap sec">
    <div class="hd">
      <p class="eyebrow">Terms</p>
      <h2 class="title">Terms<span class="sub">유의사항</span></h2>
    </div>
    <ol class="terms">
      {items}
    </ol>
  </section>"""


def sec_faq(p):
    items = "\n      ".join(f"<details><summary>{q}</summary><div class=\"body\">{ans}</div></details>" for q, ans in FAQ)
    return f"""<section id="faq" class="wrap sec" style="padding-top:0">
    <div class="hd">
      <p class="eyebrow">Before you ask</p>
      <h2 class="title">FAQ<span class="sub">자주 묻는 질문</span></h2>
    </div>
    <div class="acc">
      {items}
    </div>
  </section>"""


def sec_contact(p):
    return f"""<section id="contact" class="tint">
    <div class="wrap sec">
      <div class="hd">
        <p class="eyebrow">Contact</p>
        <h2 class="title">Start Your Build<span class="sub">{p["monthLabel"]} 빌드 상담</span></h2>
        <p class="desc">가장 편한 방법으로 연락 주세요. 프로모션 대상 모델과 크레딧 금액을 함께 안내해 드립니다.</p>
      </div>
      <div class="contact">
        <div><p class="eyebrow">Showroom</p><h3>쇼룸 방문</h3><p>서울시 서초구 신반포로 320 루비빌딩<br>월~금 12:00~19:00, 토 10:00~15:30</p><a class="link" href="https://rubiworkshop.com/showroom">방문 안내</a></div>
        <div><p class="eyebrow">Call</p><h3>고객센터 1551-5320</h3><p>help@rubi.kr</p><a class="link" href="tel:15515320">전화 걸기</a></div>
        <div><p class="eyebrow">KakaoTalk</p><h3>카카오톡 상담</h3><p>루비워크샵 카카오톡 채널에서 사진과 함께 편하게 문의하세요.</p><a class="link" href="http://pf.kakao.com/_qxgqDxd/chat" target="_blank" rel="noopener">카카오톡 채널</a></div>
      </div>
      <div class="acts" style="margin-top:36px">
        {btn("상담 신청하기", CONSULT, solid=True, consult=True)}
        {btn("전체 모델 보기", "/")}
      </div>
    </div>
  </section>"""


# ---------------------------------------------------------------- head

def ld(p):
    graph = [
        {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": p["seo"]["title"],
         "description": p["seo"]["description"], "inLanguage": "ko-KR",
         "breadcrumb": {"@id": URL + "#breadcrumb"}, "publisher": {"@id": "https://rubiworkshop.com/#store"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + p["hero"]["img"]["src"]}},
        {"@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Bikes", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Promotion", "item": URL}]},
        {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in FAQ]},
        STORE,
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def tabs():
    return "\n      ".join(f'<a href="#{sid}"{" class=\"on\"" if sid == "overview" else ""}>{label}</a>' for sid, label in TABS)


def band_for_index(p):
    """Notice band under the header of index.html while a promotion is active."""
    if not p.get("active"):
        return ""
    return f"""<div class="band">
    <div class="wrap">
      <p>{p["monthLabel"]} 프로모션. 루비워크샵에서 빌드하시면 부품 업그레이드에 쓰실 수 있는 빌드 크레딧을 최대 {man(max_credit(p))}까지 드립니다.</p>
      <a class="link" href="/promotion/" data-ga="promo-band">프로모션 보기</a>
    </div>
  </div>"""


def render(p):
    seo, og = p["seo"], p["hero"]["img"]
    robots = "index,follow,max-image-preview:large" if p.get("active") else "noindex,follow"
    body = "\n\n  ".join([sec_hero(p), sec_band(p), sec_models(p), sec_credit(p), sec_how(p), sec_brands(p),
                          sec_examples(p), sec_terms(p), sec_faq(p), sec_contact(p)])
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<!-- 이 파일은 tools/build.py 가 data/promotion.json 으로 만듭니다. 직접 고치지 말고 JSON을 고친 뒤 빌드하세요. -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}', {{ content_group: 'promotion' }});
  var GA_ID = '{GA_ID}'; // used by the shared GA4 event script in /assets/site.js
</script>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{a(seo["title"])}</title>
<meta name="description" content="{a(seo["description"])}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#fafaf9">
<!-- 네이버 서치어드바이저, 구글 서치 콘솔 소유 확인 메타 태그는 이 자리에 붙여 넣습니다 -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="루비워크샵">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="{a(seo["ogTitle"])}">
<meta property="og:description" content="{a(seo["og"])}">
<meta property="og:image" content="{SITE}{a(og["src"])}">
<meta property="og:image:width" content="{og["w"]}">
<meta property="og:image:height" content="{og["h"]}">
<meta property="og:image:alt" content="{a(og["alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{a(seo["ogTitle"])}">
<meta name="twitter:description" content="{a(seo["og"])}">
<meta name="twitter:image" content="{SITE}{a(og["src"])}">
<script type="application/ld+json">
{ld(p)}
</script>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
</head>
<body data-model="promotion" style="--accent:#b5652b">
<a class="skip" href="#main">본문으로 건너뛰기</a>

<header class="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="루비워크샵 Bikes">
      <span class="logo-word">Rubi Workshop</span>
      <span class="logo-sub">Bikes</span>
    </a>
    <nav class="gnav-top" aria-label="사이트">
      <a href="/">전체 모델</a>
      <a href="/promotion/" aria-current="page">프로모션</a>
      <a href="https://rubiworkshop.com" class="opt">rubiworkshop.com</a>
    </nav>
  </div>
</header>

<nav class="modelbar" aria-label="Promotion">
  <div class="wrap">
    <span class="name">Promotion</span>
    <div class="tabs">
      {tabs()}
    </div>
    {btn("상담 신청하기", CONSULT, consult=True)}
  </div>
</nav>

<main id="main">
  {body}
</main>

<footer>
  <div class="wrap">
    <div><p class="eyebrow">루비워크샵</p><p>서울시 서초구 신반포로 320 루비빌딩</p></div>
    <div><p class="eyebrow">상담</p><p style="user-select:all">1551-5320</p><p>월~금 12:00~19:00, 토 10:00~15:30</p></div>
    <div><p class="eyebrow">Online</p><p><a href="https://rubiworkshop.com" target="_blank" rel="noopener">rubiworkshop.com</a></p><p><a href="https://instagram.com/rubi.workshop" target="_blank" rel="noopener">@rubi.workshop</a></p></div>
    <div class="copy">Founded in 2015, Seoul · Ride Tastefully · Rubi Company</div>
  </div>
</footer>

<script src="/assets/site.js" defer></script>
</body>
</html>
"""
