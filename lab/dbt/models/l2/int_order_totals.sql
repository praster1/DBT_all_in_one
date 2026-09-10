select order_id, sum(quantity * unit_price_cents) as line_amount_cents,
       count(*) as line_count
from {{ ref('stg_items_current') }} group by order_id
