with src as (
    select *
    from {{ source('search_events', 'events_raw') }}
)

select
    cast(event_id as varchar) as event_id,
    cast(user_id as varchar) as user_id,
    cast(event_name as varchar) as event_name,
    cast(session_id as varchar) as session_id,
    cast(platform as varchar) as platform,
    cast(country_code as varchar) as country_code,
    cast(event_ts as timestamp) as event_ts,
    cast(ingest_ts as timestamp) as ingest_ts
from src
where event_id is not null
