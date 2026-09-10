-- 이미 관측한 원천의 업무 유효시간으로 구간을 만든 교육용 SCD2. dbt snapshot 실행이 아니다.
select customer_id, segment, effective_from as valid_from,
       lead(effective_from) over (partition by customer_id order by effective_from, source_seq) as valid_to
from {{ source('shop_raw', 'customer_changes') }}
