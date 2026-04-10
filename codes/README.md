# Companion Pack Guide

`codes/` 디렉터리는 책과 함께 실행해 볼 수 있는 예제 프로젝트, 플랫폼 bootstrap 파일, reference patterns, chapter snippets를 모아 둔 곳이다.

## 디렉터리 구성

| 경로 | 역할 |
| --- | --- |
| `01_duckdb_runnable_project/` | DuckDB에서 바로 따라 해 볼 수 있는 runnable path |
| `02_reference_patterns/` | semantic, governance, mesh, command/Jinja reference 등 고급 참고 예시 |
| `03_platform_bootstrap/` | DBMS별 raw 데이터 초기 셋업 SQL, 스크립트, import 예시 |
| `04_chapter_snippets/` | 장과 부록에서 직접 링크하는 snippet 모음 |

## 권장 시작 순서

1. `01_duckdb_runnable_project/README.md`
2. 책 본문 Chapter 01~11
3. 필요한 플랫폼의 `03_platform_bootstrap/`
4. 필요할 때 `04_chapter_snippets/`와 `02_reference_patterns/`

## 예제 트랙

- Retail Orders
- Event Stream
- Subscription & Billing

세 예제는 day1/day2 데이터와 expected 결과를 기준으로 서로 다른 플랫폼에서 반복 실행할 수 있도록 구성했다.

## 플랫폼 관련 경로

- DuckDB runnable path: `01_duckdb_runnable_project/`
- DBMS별 raw bootstrap: `03_platform_bootstrap/`
- Trino 운영형 예시: `04_chapter_snippets/ch18/`
- Databricks snippets: `04_chapter_snippets/ch20/`
- NoSQL + SQL Layer snippets: `04_chapter_snippets/ch19/`
