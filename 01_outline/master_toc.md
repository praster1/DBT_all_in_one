# DBT All In One · Master TOC

## Part 구성

## PART I · 핵심 개념과 기본기

dbt를 데이터 스택의 어디에 놓아야 하는지, 세 가지 연속 예제를 어떤 관점으로 읽어야 하는지, 그리고 모델링과 품질의 기본을 어디까지 가져갈지부터 잡는다.

- **1.** [DBT의 전체 그림과 세 가지 연속 예제](../chapters/ch01_dbt의-전체-그림과-세-가지-연속-예제.md)
- **2.** [개발 환경, 프로젝트 구조, DBT 명령어와 Jinja, 첫 실행](../chapters/ch02_개발-환경-프로젝트-구조-dbt-명령어와-jinja-첫-실행.md)
- **3.** [source/ref, selectors, layered modeling, grain, materializations](../chapters/ch03_sourceref-selectors-layered-modeling-grain-materializations.md)
- **4.** [Tests, Seeds, Snapshots, Documentation, Macros, Packages](../chapters/ch04_tests-seeds-snapshots-documentation-macros-packages.md)

## PART II · 신뢰성·운영·확장

디버깅, 배포, 거버넌스, semantic layer, mesh, performance처럼 실제 운영에서 프로젝트를 오래 살리는 기능을 묶는다.

- **5.** [디버깅, artifacts, runbook, anti-patterns](../chapters/ch05_디버깅-artifacts-runbook-anti-patterns.md)
- **6.** [운영, CI/CD, state/defer/clone, vars/env/hooks, 업그레이드](../chapters/ch06_운영-cicd-statedeferclone-varsenvhooks-업그레이드.md)
- **7.** [Governance, Contracts, Versions, Grants, Quality Metadata](../chapters/ch07_governance-contracts-versions-grants-quality-metadata.md)
- **8.** [Semantic Layer, Python/UDF, Mesh, Performance, dbt platform, AI](../chapters/ch08_semantic-layer-pythonudf-mesh-performance-dbt-platform-ai.md)

## PART III · 예제 케이스북

세 가지 연속 예제를 각각 하나의 독립 사례로 따라가며, 앞에서 배운 개념이 실제 도메인에서 어떤 순서로 자라나는지 보여 준다.

- **9.** [Casebook I · Retail Orders](../chapters/ch09_casebook-i-retail-orders.md)
- **10.** [Casebook II · Event Stream](../chapters/ch10_casebook-ii-event-stream.md)
- **11.** [Casebook III · Subscription & Billing](../chapters/ch11_casebook-iii-subscription-billing.md)

## PART IV · 플랫폼 플레이북

플랫폼마다 달라지는 profile, raw bootstrap, materialization, 성능·비용·제약을 실제 실행 맥락으로 정리한다.

- **12.** [Platform Playbook · DuckDB](../chapters/ch12_platform-playbook-duckdb.md)
- **13.** [Platform Playbook · MySQL](../chapters/ch13_platform-playbook-mysql.md)
- **14.** [Platform Playbook · PostgreSQL](../chapters/ch14_platform-playbook-postgresql.md)
- **15.** [Platform Playbook · BigQuery](../chapters/ch15_platform-playbook-bigquery.md)
- **16.** [Platform Playbook · ClickHouse](../chapters/ch16_platform-playbook-clickhouse.md)
- **17.** [Platform Playbook · Snowflake](../chapters/ch17_platform-playbook-snowflake.md)
- **18.** [Platform Playbook · Trino](../chapters/ch18_platform-playbook-trino.md)
- **19.** [Platform Playbook · NoSQL + SQL Layer](../chapters/ch19_platform-playbook-nosql-sql-layer.md)

## Appendices

- [APPENDIX A · Companion Pack, Example Data, Bootstrap, Answer Keys](../chapters/app_a_companion-pack-example-data-bootstrap-answer-keys.md)
- [APPENDIX B · DBT 명령어 레퍼런스](../chapters/app_b_dbt-명령어-레퍼런스.md)
- [APPENDIX C · Jinja, Macro, Extensibility Reference](../chapters/app_c_jinja-macro-extensibility-reference.md)
- [APPENDIX D · Troubleshooting, Decision Guides, Glossary, Official Sources, Support Matrix](../chapters/app_d_troubleshooting-decision-guides-glossary-official-sources-support-matrix.md)
