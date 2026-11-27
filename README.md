# Rubi Workshop Bikes

https://bike.rubiworkshop.com 루비워크샵 자전거 상담 사이트. rubiworkshop.com/models 페이지를 독립 사이트로 옮기고, 모델마다 `bike.rubiworkshop.com/모델명` 상세 페이지를 붙입니다.

- 레이아웃: sst.rubiworkshop.com(폴스타형 모델 페이지)을 기준으로, 모델 페이지의 섹션 순서는 BMW 모토라드 S 1000 RR 페이지를 참고했습니다.
- 서체: 루비워크샵 메인 히어로 위젯과 같은 톤(영문 Pretendard, 한글 에스코어 드림 4, 굵기 400 하나).
- 정적 사이트, 빌드 도구 없이 그대로 배포됩니다. 한국어 본문은 HTML에 들어 있어 자바스크립트 없이도 읽힙니다.

## 구조

```
index.html            bike.rubiworkshop.com 메인 (상담 소개, 브랜드별 라인업, 상담 전에, 과정, FAQ, 문의)
<slug>/index.html     모델 페이지 28개 (빌드 결과물, 직접 고치지 않음)
assets/site.css       모든 페이지 공통 스타일
assets/site.js        공통 동작 (핫스팟, 갤러리, 모델 바 탭, GA4 이벤트)
data/models.json      라인업 원본 (브랜드, 모델, 카테고리, 소개, 시작 가격, 링크)
data/pages/<slug>.json 모델 페이지 원본 (문구, 사진, 수치, 빌드, 지오메트리, 사양, 가격)
tools/model_page.py   모델 페이지 템플릿 (아키타입 구조)
tools/build.py        위 데이터로 모델 페이지, index.html 라인업·필터·구조화 데이터, 404 주소 목록, sitemap.xml을 다시 만듦
images/<모델>/        모델 페이지 사진
images/models/        다른 모델 카드 사진
promotion/index.html  월별 프로모션 페이지 (빌드 결과물, 직접 고치지 않음)
data/promotion.json   프로모션 원본 (월, 기간, 하이라이트·포커스 모델, 모델별 빌드 크레딧, 대상 부품 브랜드, 구성 예)
tools/promotion_page.py 프로모션 페이지 템플릿 (빌드 크레딧 설명, 사용 방법, 유의사항, FAQ 문구 포함)
404.html, CNAME, robots.txt, sitemap.xml
```

## 모델 페이지 섹션 (archetype 기준)

| 순서 | id | 내용 | BMW 페이지 대응 |
|---|---|---|---|
| 1 | `overview` | 히어로 사진, 연식 배지, 모델명, 시작 가격, 소개, 상담 버튼, 주요 수치 4개 | 히어로 |
| 2 | | 쇼룸 띠, 스테이트먼트 | |
| 3 | `highlights` | 사진과 글이 번갈아 나오는 하이라이트 3개, 더 보기 | 피처 하이라이트, Read more |
| 4 | `figures` | 큰 숫자 4개 | 키 피겨 |
| 5 | | 인용문 | 사운드 모듈 자리 |
| 6 | `technology` | 측면 사진 위 핫스팟 4개 + 설명 | 테크니컬 피처 |
| 7 | `configure` | 그룹셋 3종 + 업그레이드 카드 | 이큅먼트 패키지 |
| 8 | `process` | 아뮬렛, 디자인 포털, 멜버른 제작 | 컬러 타일 자리 |
| 9 | `gallery` | 가로 스크롤 갤러리 | |
| 10 | | Standard 아코디언 (지오메트리, 시승, 보증, 루비케어) | |
| 11 | `specs` | 사양표 + 가격 | 데이터 & 사양 |
| 12 | `more` | 같은 브랜드 다른 모델 카드 3개 | More 카드 |
| 13 | | 마무리 수치, 버튼, 각주 | |

## 모델 페이지 수정, 추가

모든 모델 페이지는 `data/pages/<slug>.json` 하나에서 만들어집니다. 문구나 가격을 고칠 때는 JSON만 고치고 `python3 tools/build.py`를 실행합니다. (`--check`는 반영 여부만 확인)

- 섹션은 hero, band, statement, highlights, figures, quote, technology, configure, geometry, process, gallery, standard, specs, more, close, notes 순서입니다. hero와 specs 말고는 키를 빼면 그 섹션이 나오지 않습니다. 각 키의 형식은 `tools/model_page.py` 머리말과 `data/pages/archetype.json`을 보면 됩니다.
- technology 항목에 `x`, `y`(사진 기준 %)가 모두 있으면 사진 위 핫스팟이 생기고, 없으면 설명 목록만 나옵니다. 현재 핫스팟은 아키타입과 SST WIDE에만 있습니다.
- more(다른 모델 카드)는 같은 브랜드 모델을 먼저, 모자라면 다음 브랜드 모델로 자동 채웁니다.
- 새 모델은 `data/models.json`에 모델을 넣고 같은 slug로 `data/pages/<slug>.json`을 만든 뒤 빌드하면, 메인 라인업 링크, sitemap.xml, 404 주소 목록까지 함께 반영됩니다.
- 사진은 `images/<slug>/`에 1920px 이하, JPG 80% 안팎으로 줄여 넣습니다. 몰튼은 몰튼 UK CDN, SST WIDE·뉴트리노는 아임웹 CDN 사진을 주소로 불러옵니다.

## 월별 프로모션 (/promotion/)

BMW 모토라드 월별 프로모션 페이지 구성(하이라이트 모델, 포커스 모델, 모델별 혜택표, 공통 혜택, 유의사항)을 따릅니다. 혜택은 현금 할인 대신 빌드 크레딧(대상 브랜드 부품 업그레이드 전용 크레딧)입니다. 루비워크샵 직접 판매 전용이며 루비서플라이 거래처는 대상이 아닙니다.

- 매달 `data/promotion.json`의 month, monthLabel, period, periodShort, seo, highlight, focus, models만 바꾸고 `python3 tools/build.py`를 실행합니다.
- 빌드하면 `promotion/index.html`, 메인 페이지 머리의 안내 띠(`<!-- build:promo -->`), sitemap.xml, 404 주소 목록이 함께 바뀝니다.
- 프로모션이 없는 달은 `active`를 false로 둡니다. 메인 안내 띠가 빠지고 sitemap에서 제외되며 페이지는 noindex가 됩니다.
- 빌드 크레딧 설명, 사용 방법, 유의사항, FAQ 문구는 매달 같으므로 `tools/promotion_page.py`에 있습니다.

## 라인업 수정

모델 이름, 가격, 소개 문구는 `data/models.json`만 고치고 `python3 tools/build.py`를 실행합니다. `index.html`의 `<!-- build:... -->` 사이는 직접 고치지 마세요(다시 만들어지면서 덮어써집니다).

## 상담 링크

상담 신청서는 아직 아임웹(rubiworkshop.com/models의 `#rwc-form`)에 있어 모든 상담 버튼이 `https://rubiworkshop.com/models#rwc-form`으로 연결됩니다. 신청서를 이 사이트로 옮기면 `data-consult`가 붙은 링크 주소만 일괄 바꾸면 됩니다.

## 검색 최적화

- 각 페이지 머리에 대표 주소(canonical), 설명, Open Graph와 트위터 카드, 구조화 데이터가 들어 있습니다. 메인은 BicycleStore + ItemList(28개 모델), 모델 페이지는 Product + BreadcrumbList.
- `sitemap.xml`, `robots.txt`가 루트에 있습니다. 네이버 서치어드바이저, 구글 서치 콘솔에 사이트를 등록하고 소유 확인 메타 태그를 각 페이지 머리의 안내 주석 자리에 붙인 뒤 sitemap.xml을 제출합니다.
- rubiworkshop.com/models를 이 사이트로 옮기면 아임웹 쪽 페이지에서 bike.rubiworkshop.com으로 연결해 주세요.

## 구글 애널리틱스 (GA4)

sst.rubiworkshop.com과 같은 측정 ID(`G-JL1KFMCJLL`)를 씁니다. 이벤트는 `section_view`, `consulting_click`(모델 페이지에서는 model 값 포함), `model_click`(메인 라인업 카드), `dealer_click`, `social_click`, `image_view`.

## 배포

Cloudflare Pages(또는 GitHub Pages)에 이 저장소를 연결하고, 빌드 명령 없이 루트 폴더를 그대로 배포합니다. 도메인은 `bike.rubiworkshop.com`(`CNAME`), DNS에 CNAME 레코드를 추가합니다.

## 내용과 사진 출처 (1차 제작, 2026-11)

| 브랜드 | 내용 | 사진 |
|---|---|---|
| 몰튼 14종 | sereno-kwon/moulton 의 모델 데이터(UK 제품 페이지 기준) | 몰튼 UK CDN 주소 |
| 몰튼 SST WIDE | sereno-kwon/sst | 아임웹 CDN 주소 |
| 바스티온 3종 | sereno-kwon/bastion, 판테라·아크엔젤은 바스티온 공식 사이트와 해외 매체 기사 | sereno-kwon/bastion 에서 복사 |
| 츠바사 크로우 | sereno-kwon/tsubasa | sereno-kwon/tsubasa 에서 복사 |
| 팔리 2종 | sereno-kwon/parlee | sereno-kwon/parlee 에서 복사 |
| 크러스트 3종 | sereno-kwon/crust | sereno-kwon/crust 에서 복사 |
| 설리 3종 | sereno-kwon/surly | sereno-kwon/surly 에서 복사 |
| 벨로오렌지 뉴트리노 | 루비워크샵 룩북 글, 벨로오렌지 공개 사양 | 아임웹 CDN 주소 |

메인 브랜드 사진은 기존 models 페이지와 같은 주소를 그대로 불러옵니다(크러스트는 사진 없음).
