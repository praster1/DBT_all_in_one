{{ config(
    pre_hook=before_begin(
        "insert into audit.run_log(model_name, status) values ('{{ this.name }}', 'RUNNING')"
    ),
    post_hook=after_commit(
        "analyze {{ this }}"
    )
) }}

select *
from {{ ref('dim_customers') }}
