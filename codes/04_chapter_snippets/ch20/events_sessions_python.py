def model(dbt, session):
    dbt.config(
        materialized="incremental",
        submission_method="job_cluster",
        job_cluster_config={
            "spark_version": "15.3.x-scala2.12",
            "node_type_id": "Standard_DS3_v2",
            "autoscale": {"min_workers": 1, "max_workers": 4}
        },
        databricks_compute="WH_BI",
        query_tags={"casebook": "event_stream", "surface": "session_python"}
    )

    events = dbt.ref("stg_app_events")

    ordered = (
        events
        .select("user_id", "event_ts", "event_name")
        .orderBy("user_id", "event_ts")
    )

    # Extremely simplified sessionization starter
    # Replace with production logic as needed
    return ordered
