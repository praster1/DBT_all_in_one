with ranked as (
 select *, row_number() over (partition by event_id order by ingestion_id desc) as delivery_rank
 from {{ source('shop_raw', 'events') }}
)
select event_id, customer_id, event_time, substr(event_time,1,10) as event_date, event_type
from ranked where delivery_rank = 1
