#!/usr/bin/env bash
set -euo pipefail

dbt debug
dbt ls -s stg_orders+
dbt build -s stg_orders+
dbt test -s fct_orders+
dbt docs generate
