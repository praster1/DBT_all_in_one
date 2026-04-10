update raw_billing.subscriptions
set status = 'canceled',
    cancelled_at = '2026-04-08',
    updated_at = '2026-04-08 09:00:00'
where subscription_id = 'sub_2001';

update raw_billing.subscriptions
set plan_id = 'plan_enterprise',
    monthly_amount = 300,
    updated_at = '2026-04-08 09:30:00'
where subscription_id = 'sub_2002';

update raw_billing.subscriptions
set status = 'active',
    updated_at = '2026-04-08 10:00:00'
where subscription_id = 'sub_2003';
