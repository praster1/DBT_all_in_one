select o.order_id
from {{ ref('fct_orders') }} o
left join (select order_id, sum(line_amount_cents) as amount_cents
           from {{ ref('fct_order_lines') }} group by order_id) l
on o.order_id = l.order_id
where l.order_id is null or o.amount_cents <> l.amount_cents
