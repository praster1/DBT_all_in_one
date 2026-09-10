-- 도메인별 원시 팩트를 먼저 공통 고객 grain으로 집계한다.
create view cmp_order_customer as
select customer_id,sum(recognized_cents) as sales_cents from {{ ref('fct_orders') }} group by customer_id;
create view cmp_subscription_customer as
select customer_id,sum(case when status='active' then monthly_cents else 0 end) as mrr_cents
from {{ ref('stg_subscriptions_current') }} group by customer_id;
create view cmp_bus_result as
select c.customer_id,coalesce(o.sales_cents,0) as sales_cents,coalesce(s.mrr_cents,0) as mrr_cents
from {{ ref('dim_customers') }} c
left join cmp_order_customer o on c.customer_id=o.customer_id
left join cmp_subscription_customer s on c.customer_id=s.customer_id;
