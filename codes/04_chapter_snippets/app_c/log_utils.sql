{% macro log_model_start() %}
    {% set run_key = var('airflow_run_id', invocation_id) %}
    {% set run_info = "from_dt=" ~ var('from_dt', 'N/A') ~ ", to_dt=" ~ var('to_dt', 'N/A') %}
    {% set audit_relation = var('audit_log_relation', target.database ~ '.' ~ target.schema ~ '.dbt_log') %}

    {% set sql %}
        merge into {{ audit_relation }} as target
        using (
            select '{{ run_key }}' as run_key, '{{ this.name }}' as model_name
        ) as source
        on target.invocation_id = source.run_key
       and target.model_name = source.model_name
        when matched then update set
            status = 'RUNNING',
            start_dt = current_timestamp,
            end_dt = null,
            error_message = null,
            run_info = '{{ run_info }}'
        when not matched then insert (
            invocation_id, model_name, status, start_dt, run_info
        ) values (
            '{{ run_key }}', '{{ this.name }}', 'RUNNING', current_timestamp, '{{ run_info }}'
        )
    {% endset %}

    {% if execute and flags.WHICH in ['run', 'build', 'test', 'snapshot'] %}
        {% do run_query(sql) %}
    {% endif %}
{% endmacro %}

{% macro log_run_end() %}
    {% if execute and flags.WHICH in ['run', 'build', 'test', 'snapshot'] %}
        {% set run_key = var('airflow_run_id', invocation_id) %}
        {% set audit_relation = var('audit_log_relation', target.database ~ '.' ~ target.schema ~ '.dbt_log') %}

        {% for res in results %}
            {% set model_nm = res.node.alias if res.node.alias else res.node.name %}
            {% set status = res.status | upper %}
            {% set msg = (res.message | string | replace("'", "''"))[:500] if res.message else '' %}

            {% set merge_query %}
                update {{ audit_relation }}
                   set status = '{{ status }}',
                       error_message = '{{ msg }}',
                       end_dt = current_timestamp
                 where invocation_id = '{{ run_key }}'
                   and model_name = '{{ model_nm }}'
            {% endset %}

            {% do run_query(merge_query) %}
        {% endfor %}
    {% endif %}
{% endmacro %}