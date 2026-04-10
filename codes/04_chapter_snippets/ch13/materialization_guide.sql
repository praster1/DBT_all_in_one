-- Retail Orders: 작은 mart table
{{ config(materialized='table') }}
select * from {{ ref('stg_orders') }};

-- Event Stream: toy data 범위만 incremental 검토
{{ config(materialized='incremental', unique_key='event_id') }}
select * from {{ ref('stg_events') }};

-- Subscription: snapshot은 작은 범위부터
-- snapshot 설정은 YAML 정의를 우선 사용
