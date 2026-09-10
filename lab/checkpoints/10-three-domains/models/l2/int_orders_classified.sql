select o.*, c.segment, t.line_amount_cents,
 case when o.amount_cents is null or o.amount_cents < 0 then 'invalid_amount'
      when o.status is null or o.status not in ('placed','paid','shipped','delivered','cancelled') then 'invalid_status'
      when c.customer_id is null then 'missing_customer'
      when t.order_id is null then 'missing_items'
      when o.amount_cents <> t.line_amount_cents then 'header_line_mismatch'
      else 'accepted' end as quality_status
from {{ ref('stg_orders_current') }} o
left join {{ ref('stg_customers_current') }} c on o.customer_id = c.customer_id
left join {{ ref('int_order_totals') }} t on o.order_id = t.order_id
