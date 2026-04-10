{% test required_fields(model, column_name, required_values) %}
with base as (
    select {{ column_name }} as field_name
    from {{ model }}
)
select *
from base
where field_name not in (
    {% for value in required_values %}
    '{{ value }}'{% if not loop.last %}, {% endif %}
    {% endfor %}
)
{% endtest %}