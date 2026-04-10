{% materialization insert_only, adapter='default' %}
    {%- set target_relation = this -%}
    {%- set compiled_sql = sql -%}

    {% call statement('main') %}
        create or replace table {{ target_relation }} as (
            {{ compiled_sql }}
        )
    {% endcall %}

    {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}