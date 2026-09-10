# DBT All In One

## 통계마당 · 마당마켓 에디션

**처음 쓰는 SQL부터 데이터 설계, 품질, 재처리와 운영까지.** 통계마당에서 이름을 딴 가상의 온라인 상점 **마당마켓(Madang Market)**을 처음부터 끝까지 발전시키며 dbt를 배운다. 주문·고객·웹 방문·구독 자료는 모두 교육용 합성 데이터이며 실제 회사의 거래·고객 데이터가 아니다.

> 이 저장소에서는 **Markdown 원고가 책의 기준 소스**다. 아래 목차에서 바로 읽을 수 있으며, ZIP을 받거나 HTML 뷰어를 실행할 필요가 없다. 기존 원고와 코드는 보존하고 확장편을 연결했다.

![마당마켓의 다섯 데이터 단계](assets/figures/journey.svg)

### 바로 읽기

[전체 목차](01_outline/master_toc.md) · [처음부터 배우기](journey/00-madang-market.md) · [설계 패턴 찾아보기](patterns/README.md) · [통합 Markdown 원고](DBT_all_in_one_v3_Madang_Market.md)

| 읽는 목적 | 시작할 문서 |
| --- | --- |
| dbt와 데이터 설계를 처음 배운다 | [마당마켓 연속 실습 J00–J16 · 17장](journey/README.md) |
| 메달리온 이외의 설계 대안을 비교한다 | [설계 패턴 P00–P25 · 26장](patterns/README.md) |
| 명령·Jinja·플랫폼·운영 내용을 찾아본다 | [개정 기초·플랫폼·부록 · 25편](chapters/reference-v3/README.md) |
| 팀의 데이터 관리 기준을 만든다 | [계약·ADR·계층 정책·운영 문서](governance/README.md) |
| 코드를 실행하고 예상 결과를 확인한다 | [마당마켓 실습과 11개 코드 체크포인트](lab/README.md) |
| 기존 책과 Companion Pack을 본다 | [기존 본문](chapters/README.md) · [기존 코드](codes/README.md) |

## 하나의 상점을 끝까지 발전시킨다

첫 주문 조회 → staging과 중복 제거 → 테이블의 한 행과 조인 → 메달리온·L0–L3 책임 → 매출 마트 → 지연 도착 → 정정·취소·삭제 → 고객 이력 → 격리와 복구 → 증분 처리 → 주문·방문·구독 통합 → 설정·검증·발행으로 이어진다.

같은 주문 `5003`, 고객 `103`, 지연 도착 주문 `5005`를 계속 추적한다. 초기 값이 맞는지만 확인하지 않고, 데이터가 바뀌거나 같은 배치가 재실행되어도 결과가 설명되는지 확인한다. 각 단계의 완전한 코드는 `lab/stages/`에 있다.

## 메달리온을 넘어서는 설계 패턴

메달리온, 허브앤스포크, Kimball 버스, 람다·카파, 레이크하우스, 데이터 메시·패브릭·연합, Data Vault, Anchor Modeling, 스타·스노플레이크·넓은 테이블, 사실 테이블, SCD·시점 설계, CDC·Outbox·이벤트 소싱·CQRS, 증분·재생, 품질 계약·격리, 소유권·설정 분리, 컴포넌트 통합, CI/CD·교체 전략, 관측성과 외부 제공을 비교한다.

모든 패턴을 한꺼번에 도입하는 것이 목표는 아니다. [아키텍처 비교표](patterns/25-architecture-comparison-atlas.md)와 [설계 리뷰 워크북](patterns/23-design-review-workbook.md)에서 해결할 문제, 적용 조건, 비용과 피해야 할 경우를 함께 판단한다.

## 저장소 구조

| 경로 | 역할 |
| --- | --- |
| `01_outline/master_toc.md` | 전체 책의 Markdown 목차 |
| `journey/` | 마당마켓 연속 실습 17장과 장별 이동 링크 |
| `patterns/` | 설계 패턴 26장과 비교·선택 기준 |
| `chapters/reference-v3/` | 개정 dbt 기초·플랫폼·부록 25편 |
| `chapters/`, `chapters/images/` | 기존 원고 25편과 원래 그림 70개 보존 |
| `assets/figures/`, `assets/screenshots/` | 확장 개념도 34개와 로컬 SQL 결과 화면 12개 |
| `lab/` | 새 실습 데이터·SQL·dbt 프로젝트·체크포인트·대사 코드 |
| `codes/` | 기존 Companion Pack 보존 |
| `governance/`, `00_meta/` | 데이터 계약·운영 정책·책의 편집 기준 |
| `references/` | 공식 출처와 확인 범위 |
| `scripts/`, `reports/` | 원고 생성·링크 검사·실행 검증·원본 보존 근거 |
| `DBT_all_in_one_v3_Madang_Market.md` | 장별 원고에서 생성하는 통합 Markdown 사본 |

## 실습을 바로 실행하기

저장소 루트에서 Python 3.10 이상으로 실행한다. 아래 세 명령은 외부 패키지 없이 동작하는 **SQLite 기준 SQL 실습**이며 dbt 엔진 실행과는 다르다.

```bash
python lab/run_reference.py --verify --output reports/sql-reference-validation.json
python lab/run_stage.py --stage 11
python lab/run_comparisons.py --output reports/model-comparisons.json
```

실제 dbt를 사용하는 별도 경로는 [실습 안내](lab/README.md)를 따른다. `lab/requirements-dbt.in`은 잠금 파일이 아니다. 기준 SQL 검사 통과를 dbt 어댑터·MERGE·클라우드·동시성·운영 권한 검증으로 해석하지 않는다.

**본편의 데이터 기준은 `lab/data/`와 `lab/expected/`다.** 기존 `codes/`의 day1/day2 자료와 단위 테스트 fixture를 섞지 않는다. 모델명이나 주문번호가 같아도 같은 데이터 버전이라고 가정하지 않는다.

## 그림과 화면

SVG 개념도는 각 Markdown 장 안에서 바로 열리며 PNG 화면은 실제 로컬 SQL 결과 뷰어를 캡처한 것이다. 상용 dbt UI나 dbt 성공 로그를 모사한 화면이 아니다. [그림 목록](assets/figure-manifest.json)과 [화면 출처](assets/screenshot-manifest.json)에서 제작 소스를 확인할 수 있다.

## 원고를 수정하고 검증하기

장별 `.md` 파일을 수정한 다음 아래 명령으로 통합 Markdown과 링크 검사 결과를 갱신한다.

```bash
python -m pip install -r requirements-book.txt
python scripts/build_markdown.py
python scripts/check_markdown_links.py
```

[기여·편집 안내](CONTRIBUTING.md)에 파일별 역할과 검증 명령을 정리했다. HTML 뷰어가 필요할 때는 `python scripts/build_book.py`로 로컬에서 생성한다. HTML은 파생 산출물이며 Markdown 원고를 대체하지 않는다.

## 원본과 검증 범위

기존 `chapters/`의 본문·부록 25편은 같은 경로와 내용으로 보존했다. 개정 참고편만 `chapters/reference-v3/`에 따로 두었다. [원본 해시 목록](reports/original-preservation.json), [기존 목차](01_outline/master_toc_original.md), Git 이력으로 비교할 수 있다.

[v3 제작 시점의 검증](reports/delivery-validation.md)과 [GitHub 반영판의 검증](reports/github-publication.md)을 구분해 기록한다. 이 책은 ChatGPT를 적극 활용해 작성되었으며, 검수를 거쳤어도 잘못된 정보나 오류가 있을 수 있다. 플랫폼별 적용 전에는 해당 버전과 권한 환경에서 별도 검증해야 한다.

[변경 기록](CHANGELOG.md) · [공식 출처](references/README.md) · [저작권·라이선스 안내](LICENSE-NOTE.md)
