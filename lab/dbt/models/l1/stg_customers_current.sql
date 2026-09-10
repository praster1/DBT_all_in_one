with ranked as (
 select *, row_number() over (partition by customer_id order by source_seq desc, ingestion_id desc) as version_rank
 from {{ source('shop_raw', 'customer_changes') }}
)
select customer_id, segment from ranked where version_rank = 1
