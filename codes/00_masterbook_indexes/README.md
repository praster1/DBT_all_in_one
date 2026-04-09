# 🗃️ DBT All-in-One Masterbook Companion Index

교재의 최신 구조 기준으로 Companion ZIP의 핵심 경로를 빠르게 찾기 위한 인덱스입니다.

## 크게 보면

| 경로 | 설명 |
|---|---|
| `01_duckdb_runnable_project/` | DuckDB 기준 실행형 runnable project |
| `02_reference_patterns/` | semantic/governance/CI/quality/platform profiles/Jinja/commands 참조 패턴 |
| `03_platform_bootstrap/` | DBMS별 day1/day2 상태 부트스트랩 스크립트 |
| `03_platform_bootstrap/nosql_sql_layer_mongodb_via_trino/` | MongoDB + Trino SQL Layer 패턴 |

## 교재 구조와 매핑

### Casebook I · Retail Orders
- `01_duckdb_runnable_project/dbt_all_in_one_lab/models/retail/`
- `03_platform_bootstrap/retail/`

### Casebook II · Event Stream
- `01_duckdb_runnable_project/dbt_all_in_one_lab/models/events/`
- `03_platform_bootstrap/events/`

### Casebook III · Subscription & Billing
- `01_duckdb_runnable_project/dbt_all_in_one_lab/models/subscription/`
- `03_platform_bootstrap/subscription/`

### Platform Playbooks
- DuckDB / MySQL / PostgreSQL / BigQuery / ClickHouse / Snowflake / Trino
  - `02_reference_patterns/platform_profiles/`
  - `03_platform_bootstrap/<example>/<platform>/`

### Trino + NoSQL + SQL Layer
- `03_platform_bootstrap/nosql_sql_layer_mongodb_via_trino/`
- `02_reference_patterns/platform_profiles/nosql_sql_layer_via_trino.md`

---

## ✅ 먼저 열어볼 파일

1. `01_duckdb_runnable_project/README.md`
2. `03_platform_bootstrap/README.md`
3. `02_reference_patterns/commands/dbt_command_reference.md`
4. `02_reference_patterns/jinja/jinja_reference.md`
