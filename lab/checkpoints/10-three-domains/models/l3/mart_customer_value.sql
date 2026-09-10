select customer_id, count(*) as order_count, sum(recognized_cents) as recognized_cents
from {{ ref('fct_orders') }} group by customer_id
