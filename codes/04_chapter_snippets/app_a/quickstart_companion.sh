#!/usr/bin/env bash
set -euo pipefail

# Companion Pack Quickstart
# 가장 안전한 학습 순서는 DuckDB → 한 예제 완주 → 다른 플랫폼 확장이다.

echo "[1] Python 환경 준비"
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
python -m pip install dbt-core dbt-duckdb

echo "[2] profile 점검"
dbt debug

echo "[3] seed + build"
dbt seed
dbt build --select retail+

echo "[4] day2 상태 반영 후 재실행 예시"
# DuckDB 로더를 사용하는 프로젝트라면 예:
# python scripts/load_raw_to_duckdb.py --database ./dbt_book_lab.duckdb --day day2
# dbt snapshot --select orders_snapshot

echo "[5] 다른 플랫폼으로 확장"
echo "Postgres  : psql -f codes/03_platform_bootstrap/retail/postgres/setup_day1.sql"
echo "BigQuery  : bq query --use_legacy_sql=false < codes/03_platform_bootstrap/events/bigquery/setup_day1.sql"
echo "Trino     : trino --file codes/03_platform_bootstrap/retail/trino/setup_day1.sql"
echo "NoSQL+SQL : bash codes/03_platform_bootstrap/nosql_sql_layer_mongodb_via_trino/retail/setup_day1_mongodb.sh"

echo "[6] 기준 레코드 점검"
echo "  - Retail Orders        : order_id = 5003"
echo "  - Event Stream         : event_id = e1010, date = 2026-04-01"
echo "  - Subscription/Billing : subscription_id = sub_2003"
