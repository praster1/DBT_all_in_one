# 1) raw 상태 확인
dbt source freshness -s source:raw_billing

# 2) 현재 모델 빌드
dbt build -s subscription

# 3) day2 변경 반영 후 snapshot
dbt snapshot -s subscriptions_status_snapshot

# 4) versioned mart 재검증
dbt build -s +fct_mrr_v2

# 5) semantic layer를 쓰는 환경이라면 validate 추가
# dbt sl validate
