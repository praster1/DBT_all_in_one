#!/usr/bin/env bash
set -euo pipefail

cd codes/01_duckdb_runnable_project/dbt_all_in_one_lab

python ../bootstrap/load_duckdb.py --db ./lab.duckdb --variant day1 --raw-dir ../raw_csv

dbt debug
dbt seed
dbt ls -s stg_orders+
dbt compile -s stg_orders
dbt run -s stg_orders
dbt test -s stg_orders
dbt docs generate
