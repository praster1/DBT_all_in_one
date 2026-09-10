with ranked as (
 select *, row_number() over (partition by item_id order by source_seq desc, ingestion_id desc) as version_rank
 from {{ source('shop_raw', 'item_changes') }}
)
select item_id, order_id, product_id, quantity, unit_price_cents
from ranked where version_rank = 1 and op <> 'D'
