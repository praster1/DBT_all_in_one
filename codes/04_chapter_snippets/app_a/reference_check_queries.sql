-- Appendix A · 빠른 기준값 점검용 SQL
-- 실제 schema/catalog 이름은 각 플랫폼 profile과 bootstrap에 맞게 조정한다.

-- -------------------------------------------------------------------
-- Retail Orders · order_id = 5003
-- -------------------------------------------------------------------
select *
from raw_retail.orders
where order_id = 5003;

select *
from stg_orders
where order_id = 5003;

select *
from int_order_lines
where order_id = 5003
order by order_id, product_id;

select *
from fct_orders
where order_id = 5003;

-- snapshot relation 이름은 프로젝트 구현에 맞게 조정한다.
select *
from orders_snapshot
where order_id = 5003
order by dbt_valid_from;

-- -------------------------------------------------------------------
-- Event Stream · late-arriving event e1010 / DAU for 2026-04-01
-- -------------------------------------------------------------------
select *
from raw_events.events
where event_id = 'e1010';

select event_date, count(distinct user_id) as dau
from fct_daily_active_users
where event_date = date '2026-04-01'
group by 1;

select *
from fct_sessions
where session_id in ('s02', 's06')
order by session_id;

-- -------------------------------------------------------------------
-- Subscription & Billing · subscription_id = sub_2003
-- -------------------------------------------------------------------
select *
from raw_billing.subscriptions
where subscription_id = 'sub_2003';

select *
from stg_subscriptions
where subscription_id = 'sub_2003';

select *
from int_subscription_mrr_basis
where subscription_id = 'sub_2003';

select *
from fct_mrr
where subscription_id = 'sub_2003';

select *
from subscriptions_status_snapshot
where subscription_id = 'sub_2003'
order by dbt_valid_from;
