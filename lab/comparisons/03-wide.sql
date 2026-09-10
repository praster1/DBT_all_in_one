-- 소비 목적의 현재 고객 속성을 붙인 wide 모델. 주문 당시 속성과는 다르다.
create table cmp_wide_result as
select o.order_id,o.customer_id,c.segment,o.recognized_cents
from {{ ref('fct_orders') }} o
join {{ ref('dim_customers') }} c on o.customer_id=c.customer_id;
