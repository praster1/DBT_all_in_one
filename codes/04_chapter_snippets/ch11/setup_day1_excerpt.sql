insert into raw_billing.accounts (account_id, account_name, region)
values
  ('acc_1001', 'Acme Retail', 'APAC'),
  ('acc_1002', 'Northwind', 'US'),
  ('acc_1003', 'Blue Orbit', 'APAC');

insert into raw_billing.plans (plan_id, plan_tier, monthly_amount)
values
  ('plan_basic', 'basic', 50),
  ('plan_pro', 'pro', 120),
  ('plan_enterprise', 'enterprise', 300);

insert into raw_billing.subscriptions (
  subscription_id, account_id, plan_id, status, started_at, cancelled_at, monthly_amount, updated_at
)
values
  ('sub_2001', 'acc_1001', 'plan_basic', 'active',   '2026-04-01', null, 50, '2026-04-01 09:00:00'),
  ('sub_2002', 'acc_1002', 'plan_pro',   'active',   '2026-04-02', null, 120, '2026-04-02 10:00:00'),
  ('sub_2003', 'acc_1003', 'plan_basic', 'trialing', '2026-04-03', null, 50, '2026-04-03 11:00:00');
