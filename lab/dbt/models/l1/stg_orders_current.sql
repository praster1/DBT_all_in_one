-- 삭제를 먼저 거르면 과거 행이 되살아난다. 최신 행 선택 후 삭제를 적용한다.
with ranked as (
 select *, row_number() over (partition by order_id order by source_seq desc, ingestion_id desc) as version_rank
 from {{ ref('stg_order_changes') }}
)
select order_id, customer_id, order_date, status, amount_cents, source_seq
from ranked where version_rank = 1 and op <> 'D'
