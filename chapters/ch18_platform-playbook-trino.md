# CHAPTER 18 · Platform Playbook · Trino

> 단일 저장소 대신 여러 catalog를 조합하는 분산 SQL 엔진을 dbt가 어떻게 다뤄야 하는지부터 생각하는 장.

> **핵심 개념 → 사례 → 운영 기준** 설명을 먼저 충분히 풀고, 이후 장에서 예제 케이스북과 플랫폼 플레이북으로 다시 가져간다.

Trino는 단일 저장소가 아니라 여러 catalog 위에서 SQL을 실행하고 조합하는 query engine에 가깝다. 그래서 dbt 관점에서 가장 먼저 물어야 할 질문은 “어디에서 읽고, 어디에 쓸 것인가”다. write 가능한 catalog와 schema를 정하고, materialization이 실제로 남는 위치를 명확히 해야 하며, connector가 보장하는 타입·권한·성능 특성을 source와 mart 설계에 함께 반영해야 한다.

또한 Trino는 federation이 쉬운 대신, 서로 다른 catalog를 가로지르는 join이 늘어날수록 latency와 cost가 커질 수 있다. 따라서 초반에는 “모든 원천을 한 번에 묶어 보자”보다 write-capable catalog를 중심으로 staging과 marts를 안정적으로 두는 편이 좋다.

## 18.1. 가장 먼저 확인할 profile / setup 예시

*Trino profile 예시*

```yaml
trino_lab:
  target: dev
  outputs:
    dev:
      type: trino
      method: none
      user: trino
      host: localhost
      port: 8080
      database: memory
```

*코드 · YAML*

| 예제 | day1 bootstrap 경로 | day2 변경 경로 |
| --- | --- | --- |
| Retail Orders | 03_platform_bootstrap/retail/trino/setup_day1.sql | 03_platform_bootstrap/retail/trino/apply_day2.sql |
| Event Stream | 03_platform_bootstrap/events/trino/setup_day1.sql | 03_platform_bootstrap/events/trino/apply_day2.sql |
| Subscription & Billing | 03_platform_bootstrap/subscription/trino/setup_day1.sql | 03_platform_bootstrap/subscription/trino/apply_day2.sql |

Trino에서는 catalog가 곧 저장소 경계다. 따라서 source를 어느 catalog에서 읽는지, materialization을 어느 catalog/schema에 남길지, connector가 쓰기를 지원하는지, 타입과 권한이 어떻게 다르게 보이는지를 먼저 잡아야 한다.

### 18.1.1. Trino에서 특히 조심할 점

- write가 필요한 dbt 모델은 write-capable connector 위에 materialize해야 한다.
- federation join은 편하지만, 플랫폼 단일 실행보다 cost와 latency가 커질 수 있다.
- profile의 database 값이 Trino catalog 이름이라는 점을 source schema 이름과 혼동하지 말아야 한다.
