-- 교육용 스타의 고객 차원과 주문 팩트. 로컬 SQLite 전용 비교 스크립트.
create table cmp_star_customer as select customer_id, segment from {{ ref('dim_customers') }};
create table cmp_star_order as select * from {{ ref('fct_orders') }};
create view cmp_star_result as
select f.order_id, f.customer_id, c.segment, f.recognized_cents
from cmp_star_order f join cmp_star_customer c on f.customer_id=c.customer_id;
