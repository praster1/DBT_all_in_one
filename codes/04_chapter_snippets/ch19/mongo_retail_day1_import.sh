#!/usr/bin/env bash
set -euo pipefail

MONGO_URI="${MONGO_URI:-mongodb://localhost:27017}"

mongoimport --uri "$MONGO_URI" --db raw_retail --collection customers --drop --file customers.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection products --drop --file products.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection order_items --drop --file order_items.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection orders --drop --file orders_day1.jsonl
