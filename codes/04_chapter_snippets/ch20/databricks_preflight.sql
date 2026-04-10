-- Databricks preflight checks
show catalogs;
show schemas in dev;

select current_catalog(), current_schema();

-- Optional: confirm you can create in your dev schema
create schema if not exists dev.analytics_jkim;

-- Optional: inspect the warehouse / cluster via system views if available
-- select * from system.query.history limit 10;
