{{
  config(
    materialized='incremental',
    file_format='delta',
    incremental_strategy='microbatch',
    event_time='event_date',
    partition_by=['event_date'],
    databricks_compute='WH_TRANSFORM',
    query_tags={'casebook': 'event_stream', 'surface': 'daily_metric'}
  )
}}

with events as (
    select
        cast(event_ts as date) as event_date,
        user_id,
        event_name
    from {{ ref('stg_app_events') }}
)

select
    event_date,
    count(*) as event_count,
    count(distinct user_id) as dau
from events
group by 1
