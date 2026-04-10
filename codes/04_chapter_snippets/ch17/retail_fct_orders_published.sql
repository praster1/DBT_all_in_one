{{ config(
    materialized='table',
    schema='MART_PUBLISHED',
    alias='fct_orders_public_v2',
    contract={'enforced': true},
    copy_grants=true,
    snowflake_warehouse='TRANSFORMING_XS',
    tags=['published', 'finance']
) }}

with orders as (
    select * from {{ ref('fct_orders') }}
)

select
    order_id,
    customer_id,
    order_date,
    gross_revenue,
    item_count,
    refund_amount,
    net_revenue
from orders
