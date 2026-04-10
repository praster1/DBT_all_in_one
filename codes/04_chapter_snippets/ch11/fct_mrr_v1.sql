with basis as (
    select * from {{ ref('int_subscription_mrr_basis') }}
)
select
    plan_id,
    count(case when contributes_to_committed_mrr then 1 end) as committed_subscription_count,
    sum(case when contributes_to_committed_mrr then monthly_amount else 0 end) as committed_mrr
from basis
group by 1
