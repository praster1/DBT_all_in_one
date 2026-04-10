#!/usr/bin/env bash
set -euo pipefail

# 1) day1 raw bootstrap
duckdb retail_lab.duckdb < retail_bootstrap_day1_duckdb.sql

# 2) build the retail models
dbt build --select retail_orders

# 3) inspect the tracked order
dbt show --select fct_orders --inline "select * from {{ ref('fct_orders') }} where order_id = 5003"

# 4) apply day2 change
duckdb retail_lab.duckdb < retail_apply_day2.sql

# 5) refresh freshness and snapshots
dbt source freshness --select source:raw_retail.orders
dbt snapshot --select orders_snapshot

# 6) rebuild the affected range
dbt build --select +fct_orders
