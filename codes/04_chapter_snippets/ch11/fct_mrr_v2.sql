with basis as (
    select * from {{ ref('int_subscription_mrr_basis') }}
)
select
    current_date as metric_date,
    plan_id,
    count(case when contributes_to_committed_mrr then 1 end) as committed_subscription_count,
    count(case when contributes_to_active_mrr then 1 end) as active_subscription_count,
    sum(case when contributes_to_committed_mrr then monthly_amount else 0 end) as committed_mrr,
    sum(case when contributes_to_active_mrr then monthly_amount else 0 end) as active_mrr
from basis
group by 1, 2
