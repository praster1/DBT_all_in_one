with ranked as (
 select *, row_number() over (partition by subscription_id order by source_seq desc, ingestion_id desc) as version_rank
 from {{ source('shop_raw', 'subscriptions') }}
)
select subscription_id, customer_id, status, monthly_cents
from ranked where version_rank = 1
