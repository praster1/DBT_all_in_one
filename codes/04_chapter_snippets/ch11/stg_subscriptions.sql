select
    subscription_id,
    account_id,
    plan_id,
    lower(status) as subscription_status,
    cast(started_at as date) as started_at,
    case
        when cancelled_at is null or cancelled_at = '' then null
        else cast(cancelled_at as date)
    end as cancelled_at,
    cast(monthly_amount as numeric) as monthly_amount,
    cast(updated_at as timestamp) as updated_at
from {{ source('raw_billing', 'subscriptions') }}
