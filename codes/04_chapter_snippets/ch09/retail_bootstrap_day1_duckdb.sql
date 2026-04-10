-- Retail Orders · day1 bootstrap (DuckDB)
CREATE SCHEMA IF NOT EXISTS raw_retail;

DROP TABLE IF EXISTS raw_retail.customers;
CREATE TABLE raw_retail.customers (
    customer_id INTEGER,
    first_name VARCHAR,
    last_name VARCHAR,
    customer_segment VARCHAR,
    signup_date DATE,
    country_code VARCHAR
);

INSERT INTO raw_retail.customers VALUES
    (101, 'Mina', 'Kim', 'vip',     '2025-11-03', 'KR'),
    (102, 'Jin',  'Park', 'regular', '2026-01-05', 'KR'),
    (103, 'Alex', 'Cho', 'regular', '2026-01-18', 'US');

DROP TABLE IF EXISTS raw_retail.products;
CREATE TABLE raw_retail.products (
    product_id INTEGER,
    product_name VARCHAR,
    category_name VARCHAR
);

INSERT INTO raw_retail.products VALUES
    (2001, 'Wireless Mouse', 'accessory'),
    (2002, 'Mechanical Keyboard', 'accessory'),
    (2003, '27in Monitor', 'display');

DROP TABLE IF EXISTS raw_retail.orders;
CREATE TABLE raw_retail.orders (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    status VARCHAR,
    total_amount DECIMAL(18,2),
    updated_at TIMESTAMP
);

INSERT INTO raw_retail.orders VALUES
    (5001, 101, '2026-04-01', 'placed',  120.00, '2026-04-01 09:00:00'),
    (5002, 101, '2026-04-01', 'paid',     90.00, '2026-04-01 10:15:00'),
    (5003, 102, '2026-04-02', 'paid',    210.00, '2026-04-02 08:30:00'),
    (5004, 103, '2026-04-02', 'shipped', 140.00, '2026-04-02 12:00:00');

DROP TABLE IF EXISTS raw_retail.order_items;
CREATE TABLE raw_retail.order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(18,2)
);

INSERT INTO raw_retail.order_items VALUES
    (5001, 2001, 1,  40.00),
    (5001, 2002, 1,  80.00),
    (5002, 2001, 1,  90.00),
    (5003, 2002, 1, 120.00),
    (5003, 2003, 1,  90.00),
    (5004, 2003, 1, 140.00);
