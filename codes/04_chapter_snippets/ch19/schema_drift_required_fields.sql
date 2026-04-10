select *
from {{ ref('stg_orders_from_mongo') }}
where sale_id is null
   or customer_id is null
   or loaded_at_ts is null
