select order_date, count(*) as order_count, sum(recognized_cents) as recognized_cents
from {{ ref('fct_orders') }} group by order_date
