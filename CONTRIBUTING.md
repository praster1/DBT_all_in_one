# 원고와 실습에 기여하기

[책 첫 화면](README.md) · [전체 목차](01_outline/master_toc.md)

## 기준 소스

읽는 순서는 `book.json`, 본문은 `journey/`, `patterns/`, `chapters/reference-v3/`의 Markdown이다. 통합 원고 `DBT_all_in_one_v3_Madang_Market.md`는 생성 파일이므로 직접 수정하지 않는다. 기존 `chapters/`의 원고는 보존 대상으로 유지한다. 논리적인 개정 내용은 개정 참고편에 쓴다.

그림은 `assets/figures/`의 SVG와 DOT, 결과 화면은 `assets/screenshots/`의 PNG와 화면 출처 목록을 함께 관리한다. 상대경로는 각 Markdown 파일 위치를 기준으로 작성한다. `/mnt/data/`, 개인 PC 절대경로, HTML 뷰어 내부의 `#d001` 같은 앵커를 원고 탐색 링크로 사용하지 않는다.

## 수정 후 확인

```bash
python -m pip install -r requirements-maintenance.txt
python scripts/build_markdown.py
python scripts/check_markdown_links.py
python scripts/validate_project.py
```

위 검사는 Markdown 경로·앵커·이미지, SQLite 기준 SQL·대안 모델 대사·11개 코드 단계, Python·YAML·SVG·PNG의 정적 검사를 포함한다. dbt 엔진과 각 어댑터의 실제 빌드·증분 쓰기·클라우드 권한 검사를 대신하지 않는다.

## 화면을 다시 만들 때

`python lab/run_reference.py --verify --output reports/sql-reference-validation.json` 실행 후, Playwright와 Chromium이 설치된 환경에서 `python scripts/make_screenshots.py --chromium /usr/bin/chromium`을 실행한다. 다른 운영체제에서는 실제 Chromium 경로를 지정한다. 화면은 로컬 SQLite 결과를 표시한 교육용 뷰어이며 dbt 제품 UI로 표기하지 않는다.

`python scripts/build_figures.py`에는 Graphviz가 필요하다. 폰트 파일은 저장소에 포함하지 않는다. `python scripts/build_book.py`는 필요할 때 오프라인 HTML 뷰어를 생성하며, GitHub 독자는 HTML 없이 장별 Markdown을 읽을 수 있다.

## 데이터와 주장

마당마켓의 원천 데이터는 합성 데이터만 사용한다. 개인정보, 비밀번호, 토큰, 업무 시스템 주소를 커밋하지 않는다. 설명용 설계 패턴, SQLite에서 검증한 코드, dbt·특정 플랫폼에서 검증한 코드를 명확히 구분한다. 최신 기능을 소개할 때는 공식 출처와 확인 범위를 함께 적는다.
