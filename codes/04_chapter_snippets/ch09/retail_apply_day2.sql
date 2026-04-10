-- Retail Orders · day2 change injection
UPDATE raw_retail.orders
SET status = 'shipped',
    total_amount = 230.00,
    updated_at = '2026-04-03 09:05:00'
WHERE order_id = 5003;
