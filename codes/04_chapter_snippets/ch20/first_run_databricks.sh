#!/usr/bin/env bash
set -euo pipefail

dbt debug
dbt parse
dbt ls -s source:*
dbt source freshness -s source:bronze_retail
dbt build -s ch09_casebook_i+  # adjust selectors to your project
dbt build -s ch10_casebook_ii+
dbt build -s ch11_casebook_iii+
