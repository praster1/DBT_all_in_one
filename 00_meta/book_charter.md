# Book Charter

## 책 정체성

- 제목: DBT All In One
- 유형: 올인원 교과서 + 실무 참고서 + 팀 온보딩 레퍼런스
- 핵심 목적: 초보자에서 전문가까지 dbt를 단계적으로 학습하고, 세 가지 연속 예제를 실제 프로젝트처럼 확장해 보는 것

## 대상 독자

- dbt를 처음 배우는 분석가, 데이터 엔지니어, 분석 엔지니어
- 실무 프로젝트를 맡아 모델링, 테스트, 운영을 직접 해야 하는 중급 사용자
- semantic layer, governance, platform strategy를 설계하는 리드와 플랫폼 오너

## 포함 범위

- 핵심 개념, source/ref, selectors, layered modeling, grain, materializations
- tests, seeds, snapshots, documentation, macros, packages
- debugging, artifacts, runbook, anti-patterns
- CI/CD, state/defer/clone, vars/env/hooks, upgrades
- governance, contracts, versions, grants, quality metadata
- semantic layer, Python/UDF, mesh, performance, dbt platform, AI
- 세 가지 casebook과 아홉 가지 platform playbook
- bootstrap, command reference, Jinja reference, troubleshooting appendix

## 예제 트랙

1. Retail Orders
2. Event Stream
3. Subscription & Billing

각 예제는 다음 자료와 함께 움직인다.

- day1 raw 데이터
- day2 변경 데이터
- expected 결과
- chapter snippets
- DBMS별 bootstrap SQL 또는 스크립트

## 플랫폼 범위

- DuckDB
- MySQL
- PostgreSQL
- BigQuery
- ClickHouse
- Snowflake
- Trino
- NoSQL + SQL Layer
- Databricks

## 저장소 운영 원칙

- GitHub에서 바로 읽기 쉬운 Markdown 구조를 기준으로 관리한다.
- 본문 Markdown은 `chapters/` 아래에 두고, 모든 그림은 `chapters/images/`에서 참조한다.
- 실행 가능한 예제와 부트스트랩 파일은 `codes/` 아래에 모은다.
- 중복되는 요약 표보다 casebook, platform playbook, appendix를 통해 구조적으로 재사용한다.
- 코드 예시는 실제 실행 가능한 형태를 우선하고, 플랫폼별 차이는 platform playbook에서 모아 설명한다.
