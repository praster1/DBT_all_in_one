with orders as (
    select *
    from {{ ref('stg_orders') }}
),
items as (
    select *
    from {{ ref('stg_order_items') }}
),
products as (
    select *
    from {{ ref('stg_products') }}
)
select
    i.order_item_id,
    i.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.payment_method,
    i.product_id,
    p.product_name,
    p.category_name,
    i.quantity,
    i.unit_price,
    i.discount_amount,
    i.line_amount
from items i
join orders o using (order_id)
join products p using (product_id)
