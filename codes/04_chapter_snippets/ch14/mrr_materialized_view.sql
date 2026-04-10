{{ config(
    materialized='materialized_view',
    on_configuration_change='apply',
    indexes=[
      {"columns": ["metric_date"], "type": "btree"},
      {"columns": ["customer_segment"], "type": "btree"}
    ]
) }}

select
    metric_date,
    customer_segment,
    sum(mrr_amount) as mrr_amount
from {{ ref('fct_mrr_v2') }}
group by 1, 2
