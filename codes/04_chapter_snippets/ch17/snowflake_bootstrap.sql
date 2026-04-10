use role SYSADMIN;

create warehouse if not exists LOADING_XS
  warehouse_size = XSMALL
  auto_suspend = 60
  auto_resume = true
  initially_suspended = true;

create warehouse if not exists TRANSFORMING_XS
  warehouse_size = XSMALL
  auto_suspend = 60
  auto_resume = true
  initially_suspended = true;

create warehouse if not exists TRANSFORMING_L
  warehouse_size = LARGE
  auto_suspend = 120
  auto_resume = true
  initially_suspended = true;

create warehouse if not exists REPORTING_XS
  warehouse_size = XSMALL
  auto_suspend = 60
  auto_resume = true
  initially_suspended = true;

create database if not exists RAW;
create database if not exists ANALYTICS_DEV;
create database if not exists ANALYTICS;

create schema if not exists RAW.RETAIL;
create schema if not exists RAW.EVENTS;
create schema if not exists RAW.SUBSCRIPTION;

create schema if not exists ANALYTICS_DEV.STAGING;
create schema if not exists ANALYTICS_DEV.INTERMEDIATE;
create schema if not exists ANALYTICS_DEV.MART_CORE;

create schema if not exists ANALYTICS.MART_PUBLISHED;

create role if not exists TRANSFORMER;
create role if not exists DBT_PROD;
create role if not exists ANALYST_READONLY;

grant usage on warehouse TRANSFORMING_XS to role TRANSFORMER;
grant usage on warehouse TRANSFORMING_L to role DBT_PROD;
grant usage on warehouse REPORTING_XS to role ANALYST_READONLY;

grant usage on database ANALYTICS_DEV to role TRANSFORMER;
grant usage on database ANALYTICS to role DBT_PROD;
grant usage on database ANALYTICS to role ANALYST_READONLY;

grant usage on all schemas in database ANALYTICS to role ANALYST_READONLY;
grant select on future tables in schema ANALYTICS.MART_PUBLISHED to role ANALYST_READONLY;
grant select on future views in schema ANALYTICS.MART_PUBLISHED to role ANALYST_READONLY;
