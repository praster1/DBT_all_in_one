with subs as (
    select * from {{ ref('stg_subscriptions') }}
),
plans as (
    select * from {{ ref('stg_plans') }}
)
select
    s.subscription_id,
    s.account_id,
    s.plan_id,
    p.plan_tier,
    s.subscription_status,
    s.started_at,
    s.cancelled_at,
    s.monthly_amount,
    case
        when s.subscription_status in ('active', 'trialing') then true
        else false
    end as contributes_to_committed_mrr,
    case
        when s.subscription_status = 'active' then true
        else false
    end as contributes_to_active_mrr,
    s.updated_at
from subs s
left join plans p
  on s.plan_id = p.plan_id
