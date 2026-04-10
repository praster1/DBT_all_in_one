import polars as pl


def model(dbt, session):
    dbt.config(materialized="table")

    orders = dbt.ref("fct_orders")
    df = orders.pl()

    # 작은 실습용 예시: 상위 고객 10개만 추출
    result = (
        df.group_by("customer_id")
          .agg(pl.sum("gross_revenue").alias("customer_revenue"))
          .sort("customer_revenue", descending=True)
          .head(10)
    )

    return result
