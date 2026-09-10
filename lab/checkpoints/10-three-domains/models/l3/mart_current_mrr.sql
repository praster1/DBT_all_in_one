-- 단일 통화·월간 요금만 있는 실습. MRR은 주문 매출과 합산하지 않는다.
select sum(case when status = 'active' then monthly_cents else 0 end) as mrr_cents
from {{ ref('stg_subscriptions_current') }}
