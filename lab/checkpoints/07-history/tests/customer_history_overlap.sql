select a.customer_id
from {{ ref('dim_customer_history') }} a
join {{ ref('dim_customer_history') }} b
 on a.customer_id = b.customer_id and a.valid_from < b.valid_from
where a.valid_to is null or a.valid_to > b.valid_from
