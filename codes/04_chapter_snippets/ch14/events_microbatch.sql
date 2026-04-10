{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    event_time='event_time',
    unique_key='event_id',
    indexes=[
      {"columns": ["event_time"], "type": "btree"},
      {"columns": ["user_id"], "type": "btree"}
    ]
) }}

select
    event_id,
    user_id,
    session_id,
    event_time,
    event_type,
    page_url
from {{ ref('stg_events') }}
