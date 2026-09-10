-- 변경 이벤트 중복 제거: 재전송은 ingestion_id만 새로 생긴다.
with ranked as (
 select *, row_number() over (partition by change_id order by ingestion_id desc) as delivery_rank
 from {{ source('shop_raw', 'order_changes') }}
)
select change_id, order_id, customer_id, order_date, lower(trim(status)) as status,
       amount_cents, source_seq, op, ingestion_id, ingested_at
from ranked where delivery_rank = 1
