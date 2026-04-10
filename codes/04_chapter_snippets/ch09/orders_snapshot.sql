{% snapshot orders_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='order_id',
    strategy='check',
    check_cols=['order_status', 'total_amount', 'updated_at']
  )
}}
select * from {{ ref('stg_orders') }}
{% endsnapshot %}
