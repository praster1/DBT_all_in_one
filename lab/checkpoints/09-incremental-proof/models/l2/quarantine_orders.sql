select * from {{ ref('int_orders_classified') }} where quality_status <> 'accepted'
