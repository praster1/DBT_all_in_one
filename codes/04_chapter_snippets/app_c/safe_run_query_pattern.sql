{% set get_country_query %}
    select distinct country_code
    from {{ source('raw_retail', 'orders') }}
    where country_code is not null
    order by 1
{% endset %}

{% if execute and flags.WHICH not in ['compile', 'docs'] %}
    {% set rs = run_query(get_country_query) %}
    {% set country_list = rs.columns[0].values() %}
{% else %}
    {% set country_list = [] %}
{% endif %}

{% for country in country_list %}
select
    '{{ country }}' as country_code
{% if not loop.last %} union all {% endif %}
{% endfor %}