with src as (
    select *
    from {{ source('nosql_retail', 'orders') }}
)

select
    cast(_id as varchar) as raw_document_id,
    cast(sale_id as varchar) as sale_id,
    cast(customer_id as varchar) as customer_id,
    lower(cast(order_status as varchar)) as order_status,
    cast(total_amount as decimal(18, 2)) as total_amount,
    cast(loaded_at_ts as timestamp) as loaded_at_ts
from src
where sale_id is not null
