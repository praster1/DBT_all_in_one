#!/usr/bin/env bash
set -euo pipefail

ES_URL="${ES_URL:-http://localhost:9200}"

curl -sS -H 'Content-Type: application/x-ndjson'   -XPOST "$ES_URL/events_raw/_bulk?refresh=true"   --data-binary @events_day2.ndjson
