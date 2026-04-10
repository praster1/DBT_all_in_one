{{
  config(
    materialized='incremental',
    file_format='delta',
    incremental_strategy='merge',
    unique_key='order_id',
    partition_by=['order_date'],
    databricks_compute='WH_TRANSFORM',
    query_tags={'casebook': 'retail_orders', 'surface': 'fact'}
  )
}}

with lines as (
    select * from {{ ref('int_order_lines') }}
)

select
    order_id,
    customer_id,
    min(order_date) as order_date,
    sum(line_amount) as gross_revenue,
    sum(quantity) as item_count,
    current_timestamp() as dw_updated_at
from lines
group by 1,2

{% if is_incremental() %}
  -- simple example: only merge orders newer than max seen order_date
  having min(order_date) >= (
    select coalesce(max(order_date), date'1900-01-01') from {{ this }}
  )
{% endif %}
