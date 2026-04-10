with src as (
    select *
    from {{ source('nosql_subscription', 'subscriptions') }}
)

select
    cast(_id as varchar) as raw_document_id,
    cast(subscription_id as varchar) as subscription_id,
    cast(account_id as varchar) as account_id,
    cast(plan_code as varchar) as plan_code,
    lower(cast(status as varchar)) as status,
    cast(mrr as decimal(18, 2)) as mrr,
    cast(effective_at as timestamp) as effective_at,
    cast(loaded_at_ts as timestamp) as loaded_at_ts
from src
where subscription_id is not null
