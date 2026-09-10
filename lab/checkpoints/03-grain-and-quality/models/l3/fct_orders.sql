select order_id, customer_id, order_date, status, amount_cents,
       case when status in ('paid','shipped','delivered') then amount_cents else 0 end as recognized_cents
from {{ ref('int_orders_valid') }}
