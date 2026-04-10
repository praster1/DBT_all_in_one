#!/usr/bin/env bash
set -euo pipefail

echo "[1] profile and adapter check"
dbt debug --target dev

echo "[2] parse project structure"
dbt parse

echo "[3] build retail published surface"
dbt build --select +fct_orders_public_v2+

echo "[4] build event dynamic table path"
dbt run --select fct_event_sessions_dt

echo "[5] build subscription current surface"
dbt build --select +fct_mrr_public_v2+

echo "[6] inspect query history by query_tag in Snowflake UI"
echo "  - dbt_local_dev::<model_name>"
