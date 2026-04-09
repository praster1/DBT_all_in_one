{{ config(
    materialized='incremental',
    unique_key='event_id',
    on_schema_change='append_new_columns'
) }}

with src as (
    select *
    from {{ ref('stg_events') }}
    {% if is_incremental() %}
      where event_time >= (
        select coalesce(max(event_time) - interval '2 hour', cast('1900-01-01' as timestamp))
        from {{ this }}
      )
    {% endif %}
)
select
    event_id,
    user_id,
    session_id,
    event_time,
    event_type,
    device_type,
    event_date
from src
