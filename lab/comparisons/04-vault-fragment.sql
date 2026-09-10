-- 업무 키/관계/속성 분리의 교육용 단편. Data Vault 2.0 준수 구현이 아니다.
-- 해시 키, PIT, 다중 원천, 삭제/유효성 Satellite의 완전 설계는 별도다.
create table cmp_hub_customer as select distinct customer_id from {{ source('shop_raw','customer_changes') }};
create table cmp_hub_order as select distinct order_id from {{ ref('stg_order_changes') }};
create table cmp_link_customer_order as select distinct customer_id,order_id from {{ ref('stg_order_changes') }};
create table cmp_sat_order as
select change_id,order_id,status,amount_cents,source_seq,ingested_at,op
from {{ ref('stg_order_changes') }};
create view cmp_vault_latest as
select order_id,status,amount_cents from
(select *,row_number() over(partition by order_id order by source_seq desc,change_id desc) as r
 from cmp_sat_order) where r=1 and op<>'D';
-- 소비 결과에는 품질 허용 목록을 적용한다. 원천 Vault 보존과 소비 품질은 다르다.
create view cmp_vault_result as
select v.order_id,l.customer_id,c.segment,
case when v.status in ('paid','shipped','delivered') then v.amount_cents else 0 end as recognized_cents
from cmp_vault_latest v join cmp_link_customer_order l on v.order_id=l.order_id
join {{ ref('dim_customers') }} c on l.customer_id=c.customer_id
join {{ ref('int_orders_valid') }} q on v.order_id=q.order_id;
