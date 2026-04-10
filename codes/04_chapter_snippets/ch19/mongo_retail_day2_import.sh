#!/usr/bin/env bash
set -euo pipefail

MONGO_URI="${MONGO_URI:-mongodb://localhost:27017}"

# Replace or upsert day2 changes.
mongoimport --uri "$MONGO_URI" --db raw_retail --collection orders --mode upsert --upsertFields sale_id --file orders_day2_patch.jsonl
