select f.*, d.segment as segment_at_order
from {{ ref('fct_orders') }} f
left join {{ ref('dim_customer_history') }} d
 on f.customer_id = d.customer_id
 and (f.order_date || ' 00:00:00') >= d.valid_from
 and ((f.order_date || ' 00:00:00') < d.valid_to or d.valid_to is null)
