{{
  config(
    materialized='materialized_view',
    schedule={
      'cron': '0 0/30 * * * ? *',
      'time_zone_value': 'Etc/UTC'
    },
    liquid_clustered_by=['account_id'],
    databricks_tags={'domain': 'billing', 'surface': 'current_mrr'},
    tblproperties={
      'delta.autoOptimize.optimizeWrite': 'true',
      'delta.autoOptimize.autoCompact': 'true'
    },
    query_tags={'casebook': 'subscription_billing', 'surface': 'published_current'}
  )
}}

select
    account_id,
    subscription_id,
    mrr,
    status,
    plan_name,
    effective_date,
    current_timestamp() as refreshed_at
from {{ ref('fct_mrr_current') }}
where is_current = true
