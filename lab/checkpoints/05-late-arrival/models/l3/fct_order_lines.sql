select i.item_id, i.order_id, o.customer_id, o.order_date, i.product_id,
       i.quantity, i.unit_price_cents, i.quantity * i.unit_price_cents as line_amount_cents,
       case when o.status in ('paid','shipped','delivered')
            then i.quantity * i.unit_price_cents else 0 end as recognized_cents
from {{ ref('stg_items_current') }} i
join {{ ref('int_orders_valid') }} o on i.order_id = o.order_id
