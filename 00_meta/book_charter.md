# Book Charter

## 책 정체성

- 제목: DBT All In One
- 유형: 올인원 교과서 + 실무 참고서 + 온보딩 레퍼런스
- 핵심 목적: 초보자에서 전문가까지 dbt를 단계적으로 학습하고, 세 가지 연속 예제를 실제 프로젝트처럼 확장해 보는 것

## 대상 독자

- dbt를 처음 배우는 분석가/데이터 엔지니어
- 실무 프로젝트를 맡은 중급 사용자
- 거버넌스/semantic/platform 운영을 설계하는 리드

## 포함 범위

- 핵심 개념, 모델링, 테스트, snapshots, 문서화, macros, packages
- 디버깅, artifacts, CI/CD, state/defer/clone, vars/env/hooks, 업그레이드
- governance, contracts, versions, grants, metadata
- semantic layer, python/UDF, mesh, performance, dbt platform, AI
- 세 가지 casebook과 다중 플랫폼 playbook

## 예제 트랙

1. Retail Orders
2. Event Stream
3. Subscription & Billing

각 예제는 다음을 함께 제공한다.

- 초기 raw 데이터(day1)
- 변경 상태(day2)
- expected 결과
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

## 저장소 운영 원칙

- GitHub에서 바로 읽기 좋은 Markdown을 기준으로 관리한다.
- 큰 PDF 원고를 그대로 붙이지 않고, 챕터 단위 파일과 companion code를 분리한다.
- 반복되는 플랫폼 비교 표는 본문 곳곳에 복제하지 않고 casebook / playbook / appendix로 보낸다.
- 코드 예시는 실제 실행 가능한 형태를 우선한다.
