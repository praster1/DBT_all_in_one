# 🏗️ Platform Bootstrap Pack

This directory provides raw-data bootstrap assets for all three companion examples.

## Included example tracks

- `retail`
- `events`
- `subscription`

## What each SQL platform folder contains

- `setup_day1.sql` — create raw schema/tables and load the initial day1 state
- `apply_day2.sql` — replace mutable raw tables with the day2 state for snapshot/incremental labs

## Supported SQL targets

- duckdb
- mysql
- postgres
- bigquery
- clickhouse
- snowflake
- trino (`memory` catalog for a fast local trial)

## NoSQL + SQL Layer path

- `nosql_sql_layer_mongodb_via_trino/` — JSONL files + `mongoimport` helpers
- `trino_catalog_examples/` — sample Trino catalog properties (`memory`, `mongodb`, `elasticsearch`)

---

The SQL scripts are intentionally compact and explicit. They prioritize readability over bulk-load performance so examples are easy to inspect, edit, and debug while following the book.
