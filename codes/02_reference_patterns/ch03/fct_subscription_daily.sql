with changes as (
    select *
    from {{ ref('int_subscription_changes') }}
),
daily as (
    select
        customer_id,
        subscription_id,
        snapshot_date,
        sum(mrr_delta) as mrr_change,
        max(is_active) as is_active
    from changes
    group by 1, 2, 3
)
select
    customer_id,
    subscription_id,
    snapshot_date,
    sum(mrr_change) over (
        partition by customer_id, subscription_id
        order by snapshot_date
        rows between unbounded preceding and current row
    ) as ending_mrr,
    is_active
from daily
