{{ config(
    materialized='dynamic_table',
    schema='MART_CORE',
    alias='fct_event_sessions_dt',
    snowflake_warehouse='TRANSFORMING_L',
    target_lag='10 minutes',
    cluster_by=['session_start', 'user_id']
) }}

with page_events as (
    select
        session_id,
        user_id,
        event_time
    from {{ ref('stg_events') }}
    where event_type = 'page_view'
),

sessionized as (
    select
        session_id,
        user_id,
        min(event_time) as session_start,
        max(event_time) as session_end,
        count(*) as page_view_count
    from page_events
    group by 1, 2
)

select * from sessionized
