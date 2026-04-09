-- source() : 프로젝트 바깥 입력
select * from {{ source('raw_retail', 'orders') }};

-- ref() : 프로젝트 안의 다른 모델
select * from {{ ref('stg_orders') }};

-- config() : 특정 모델 설정
{{ config(materialized='table', tags=['chapter02']) }}

select
  order_id,
  customer_id,
  order_date
from {{ ref('stg_orders') }};

-- var() : 실행 시점 변수 사용
select *
from {{ ref('fct_daily_sales') }}
where order_date >= '{{ var("start_date", "2026-04-01") }}';

-- env_var() : 비밀값 / 환경값 주입
-- profiles.yml 예시
-- password: "{{ env_var('DBT_ENV_SECRET_PG_PASSWORD') }}"

{% macro cents_to_currency(column_name) %}
  round({{ column_name }} / 100.0, 2)
{% endmacro %}

select
  order_id,
  {{ cents_to_currency('gross_revenue_cents') }} as gross_revenue
from {{ ref('fct_orders_raw') }};
