select quality_status, count(*) as row_count
from {{ ref('int_orders_classified') }} group by quality_status
