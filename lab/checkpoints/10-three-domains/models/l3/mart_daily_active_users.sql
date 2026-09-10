select event_date, count(distinct customer_id) as active_users
from {{ ref('stg_events') }} group by event_date
