-- Appendix A convenience snippet
-- 보다 완전한 운영형 예시는 codes/04_chapter_snippets/ch18/trino/ 아래를 함께 본다.

create table if not exists iceberg.sample_db.dbt_log (
    invocation_id  varchar,
    model_name     varchar,
    status         varchar,
    start_dt       timestamp(6) with time zone,
    end_dt         timestamp(6) with time zone,
    duration       varchar,
    error_message  varchar,
    run_info       varchar
);

-- 이 테이블은 Trino/Iceberg/Airflow 운영형 샘플에서
-- log_model_start / log_run_end 매크로의 타깃으로 사용한다.
-- platform-independent default가 아니라 Trino 사례집의 일부로 읽는 것이 좋다.
