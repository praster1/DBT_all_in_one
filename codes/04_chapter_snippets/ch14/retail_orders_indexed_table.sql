{{ config(
    materialized='table',
    indexes=[
      {"columns": ["order_id"], "unique": true},
      {"columns": ["customer_id"], "type": "btree"},
      {"columns": ["order_date"], "type": "btree"}
    ]
) }}

select
    order_id,
    customer_id,
    order_date,
    gross_revenue,
    item_count
from {{ ref('fct_orders') }}
