# 🧪 dbt_all_in_one_lab_pack

> `DBT 올인원 교과서`와 함께 사용하는 학습/참고용 Companion Pack입니다.

## 📦 구성 개요

| 디렉터리 | 역할 | 핵심 내용 |
|---|---|---|
| `01_duckdb_runnable_project/` | 실행형 실습 | DuckDB 기반 runnable path (Retail / Events / Subscription) |
| `02_reference_patterns/` | 참조 패턴 | governance, semantic layer, UDF/functions, mesh, microbatch, Jinja/commands |
| `03_platform_bootstrap/` | 플랫폼 부트스트랩 | 플랫폼별 raw 데이터 초기 셋업 및 day1/day2 상태 재현 |

## 1) `01_duckdb_runnable_project/`

- 실제로 따라 실행 가능한 학습 경로
- 하나의 프로젝트에서 `source → staging → marts`, tests, snapshots, exposures, selectors 기본 흐름 재현
- 세 트랙(Retail / Events / Subscription)을 통합 운영

## 2) `02_reference_patterns/`

- 버전/엔진/플랜에 따라 차이가 날 수 있는 고급 예시 모음
- 참고용 중심 디렉터리이며, 적용 전 반드시 사용 중인 dbt 버전/엔진 문서 재확인 권장

> ⚠️ 안내: 일부 패턴은 어댑터/버전에 따라 지원 범위가 달라질 수 있습니다.

## 3) `03_platform_bootstrap/`

- 플랫폼별로 동일 예제를 빠르게 시험할 수 있도록 raw 데이터/셋업 스크립트 제공
- 지원 축: DuckDB / MySQL / PostgreSQL / BigQuery / ClickHouse / Snowflake / Trino(memory)
- NoSQL + SQL Layer 실습: MongoDB JSONL + `mongoimport` + Trino catalog 예시 포함

---

## 🚀 권장 학습 순서

1. `01_duckdb_runnable_project/README.md`
2. 책의 Platform/고급 챕터와 함께 `02_reference_patterns/`
3. 플랫폼별 실습이 필요할 때 `03_platform_bootstrap/README.md`
