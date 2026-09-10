select * from {{ ref('fct_orders') }} where amount_cents < 0 or recognized_cents < 0
