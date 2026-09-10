-- 단순 정규화 코어: 상태별 인정 여부를 분리한다. 완전한 전사 3NF 모델은 아니다.
create table cmp_status(status text primary key, include_in_sales integer not null);
insert into cmp_status values ('placed',0),('paid',1),('shipped',1),('delivered',1),('cancelled',0);
create table cmp_core_order as
select order_id, customer_id, order_date, status, amount_cents from {{ ref('int_orders_valid') }};
create view cmp_core_result as
select o.order_id,o.customer_id,c.segment,o.amount_cents*s.include_in_sales as recognized_cents
from cmp_core_order o join cmp_status s on o.status=s.status
join {{ ref('dim_customers') }} c on o.customer_id=c.customer_id;
