-- Anchor의 속성별 시간 분리를 보여 주는 단편. 완전한 생성기/6NF 검증은 아니다.
create table cmp_anchor_customer as select distinct customer_id from {{ source('shop_raw','customer_changes') }};
create table cmp_attribute_segment as
select customer_id,effective_from as valid_from,segment from {{ source('shop_raw','customer_changes') }};
create view cmp_anchor_current as
select customer_id,segment from
(select *,row_number() over(partition by customer_id order by valid_from desc) as r
 from cmp_attribute_segment) where r=1;
create view cmp_anchor_result as
select o.order_id,o.customer_id,c.segment,o.recognized_cents
from {{ ref('fct_orders') }} o join cmp_anchor_current c on o.customer_id=c.customer_id;
