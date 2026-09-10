select order_id, status, amount_cents from {{ source('shop_raw', 'order_changes') }}
