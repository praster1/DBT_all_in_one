-- Retail Orders
select order_id, customer_id, gross_revenue, item_count
from fct_orders
where order_id = 5003;

-- Event Stream
select event_date, event_count, active_users
from fct_events_daily
order by event_date desc
limit 7;

-- Subscription & Billing
select subscription_id, plan_code, status, current_mrr
from fct_mrr_current
where subscription_id = 'sub_2003';

-- Snapshot sanity checks
select subscription_id, dbt_valid_from, dbt_valid_to
from snap_subscription_status
where subscription_id = 'sub_2003'
order by dbt_valid_from;
