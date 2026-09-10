# 전체 목차 · 마당마켓 에디션

주 학습 경로는 J00~J16이며, P00~P25는 설계 대안을 비교하는 아틀라스다. 기존 dbt·플랫폼 원고는 참조편으로 연결했다.

## 시작하기

- [DBT All In One](../README.md)

## 마당마켓 연속 실습

- [J00 · 마당마켓: 한 개의 상점으로 처음부터 끝까지](../journey/00-madang-market.md)
- [J01 · 환경 준비: 실행 종류와 데이터 파일을 혼동하지 않기](../journey/01-setup.md)
- [J02 · 첫 주문 모델: 결과를 눈으로 읽는 습관](../journey/02-first-query.md)
- [J03 · 전달 중복과 업무 최신 상태를 두 단계로 분리하기](../journey/03-staging.md)
- [J04 · 테이블의 한 행: 조인으로 매출이 부풀어 오르는 순간](../journey/04-grain.md)
- [J05 · 메달리온을 실제 관리 규칙으로 바꾸기](../journey/05-layers.md)
- [J06 · 첫 매출 마트: 업무 정의를 코드와 테스트에 고정하기](../journey/06-marts.md)
- [J07 · 지난 날짜의 주문이 오늘 도착했다](../journey/07-late-data.md)
- [J08 · 정정·취소·삭제를 같은 처리로 뭉개지 않기](../journey/08-correction-delete.md)
- [J09 · 오늘의 고객과 주문 당시의 고객은 다르다](../journey/09-history.md)
- [J10 · 격리는 끝이 아니라 복구를 위한 대기 상태다](../journey/10-quarantine-repair.md)
- [J11 · 증분 최적화의 출발점은 전체 계산과의 동등성이다](../journey/11-incremental.md)
- [J12 · 주문·웹 방문·구독을 하나의 상점에 연결하기](../journey/12-three-domains.md)
- [J13 · 메달리온 말고 다른 설계를 선택해야 할 때](../journey/13-architecture-alternatives.md)
- [J14 · 이름·소유권·권한을 코드 밖에서도 관리하기](../journey/14-configuration.md)
- [J15 · 검증·발행·복구까지 포함한 최종 상점](../journey/15-release.md)
- [J16 · 종합 실습과 해설: 숫자와 설계를 함께 설명하기](../journey/16-workbook.md)

## 설계 패턴 아틀라스

- [P00 · 메달리온 말고 무엇이 있는가: 설계 패턴 전체 지도](../patterns/00-pattern-map.md)
- [P01 · 메달리온: 색깔이 아니라 품질과 책임을 나누는 방법](../patterns/01-medallion.md)
- [P02 · 허브앤스포크: 중앙 통합 저장소와 종속 데이터 마트](../patterns/02-hub-and-spoke.md)
- [P03 · Kimball 버스 아키텍처: 작게 납품하고 공통 차원으로 연결하기](../patterns/03-kimball-bus.md)
- [P04 · 람다 아키텍처: 빠른 잠정값과 다시 계산한 확정값](../patterns/04-lambda.md)
- [P05 · 카파 아키텍처: 하나의 처리 경로와 로그 재생](../patterns/05-kappa.md)
- [P06 · 웨어하우스·데이터 레이크·레이크하우스와 dbt의 위치](../patterns/06-lakehouse.md)
- [P07 · 데이터 메시: 폴더가 아니라 소유권과 계약의 설계](../patterns/07-data-mesh.md)
- [P08 · 데이터 패브릭과 연합 쿼리: 복제하지 않고 연결하면 끝나는가](../patterns/08-data-fabric-and-federation.md)
- [P09 · Data Vault: 업무 키·관계·속성 이력을 분리하는 통합 모델](../patterns/09-data-vault.md)
- [P10 · dbt 계층형 DAG: 원천의 언어를 업무의 언어로 바꾸기](../patterns/10-staging-and-dag.md)
- [P11 · 스타·스노플레이크·wide table: 읽기 편의와 의미 일관성의 균형](../patterns/11-star-snowflake-wide.md)
- [P12 · 팩트 패턴: 거래·주기 스냅샷·누적 스냅샷·무측정 사실](../patterns/12-fact-patterns.md)
- [P13 · SCD와 시점 설계: 현재, 그 당시, 그때 알고 있던 사실](../patterns/13-history-and-temporal.md)
- [P14 · CDC·Outbox·이벤트 소싱·CQRS: 비슷해 보이는 변경 패턴 구별하기](../patterns/14-cdc-outbox-event-sourcing.md)
- [P15 · 증분·재처리·멱등성: 새 행만 읽는 설계의 함정](../patterns/15-incremental-and-replay.md)
- [P16 · 품질 게이트·계약·격리: 실패를 숨기지 않고 발행을 통제하기](../patterns/16-quality-contract-quarantine.md)
- [P17 · 설정 중앙화와 단일 소유자: 스키마가 바뀌어도 SQL은 유지하기](../patterns/17-configuration-and-ownership.md)
- [P18 · 컴포넌트와 통합 모델: 계산을 나누고 쓰기는 한 곳으로](../patterns/18-components-and-integration.md)
- [P19 · CI/CD·Blue–Green·Strangler: 계산 성공에서 안전한 교체까지](../patterns/19-ci-cd-and-migration.md)
- [P20 · 관측·성능·복구: 어떤 층에서 실패했는지 알아내기](../patterns/20-observability-and-performance.md)
- [P21 · 보안과 외부 제공: 모델의 끝이 데이터 책임의 끝은 아니다](../patterns/21-security-and-serving.md)
- [P22 · 패턴 선택 사례: 같은 도구, 서로 다른 정답](../patterns/22-pattern-selection-case-studies.md)
- [P23 · 설계 리뷰 워크북과 안티패턴 사전](../patterns/23-design-review-workbook.md)
- [P24 · Anchor Modeling: 속성의 시간 변화를 더 작게 분리하기](../patterns/24-anchor-modeling.md)
- [P25 · 아키텍처 비교표: 메달리온 외의 대안을 한 장에서 찾기](../patterns/25-architecture-comparison-atlas.md)

## dbt 기초·플랫폼 참고

- [이 책을 읽는 방법](../chapters/reference-v3/00-introduction-and-reading-guide.md)
- [CHAPTER 01 · DBT의 전체 그림과 세 가지 연속 예제](../chapters/reference-v3/01-dbt-overview-and-three-example-tracks.md)
- [CHAPTER 02 · 개발 환경, 프로젝트 구조, DBT 명령어와 Jinja, 첫 실행](../chapters/reference-v3/02-development-environment-project-structure-commands-and-jinja.md)
- [CHAPTER 03 · source/ref, selectors, layered modeling, grain, materializations](../chapters/reference-v3/03-source-ref-selectors-layered-modeling-grain-and-materializations.md)
- [CHAPTER 04 · Tests, Seeds, Snapshots, Documentation, Macros, Packages](../chapters/reference-v3/04-tests-seeds-snapshots-documentation-macros-and-packages.md)
- [CHAPTER 05 · 디버깅, artifacts, runbook, anti-patterns](../chapters/reference-v3/05-debugging-artifacts-runbook-and-anti-patterns.md)
- [CHAPTER 06 · 운영, CI/CD, state/defer/clone, vars/env/hooks, 업그레이드](../chapters/reference-v3/06-operations-cicd-state-defer-clone-vars-env-hooks-and-upgrades.md)
- [CHAPTER 07 · Governance, Contracts, Versions, Grants, Quality Metadata](../chapters/reference-v3/07-governance-contracts-versions-grants-quality-and-metadata.md)
- [CHAPTER 08 · Semantic Layer, Python/UDF, Mesh, Performance, dbt platform, AI](../chapters/reference-v3/08-semantic-layer-python-udf-mesh-performance-platform-and-ai.md)
- [CHAPTER 09 · Casebook I · Retail Orders](../chapters/reference-v3/09-casebook-retail-orders.md)
- [CHAPTER 10 · Casebook II · Event Stream](../chapters/reference-v3/10-casebook-event-stream.md)
- [CHAPTER 11 · Casebook III · Subscription & Billing](../chapters/reference-v3/11-casebook-subscription-billing.md)
- [CHAPTER 12 · Platform Playbook · DuckDB](../chapters/reference-v3/12-platform-playbook-duckdb.md)
- [CHAPTER 13 · Platform Playbook · MySQL](../chapters/reference-v3/13-platform-playbook-mysql.md)
- [CHAPTER 14 · Platform Playbook · PostgreSQL](../chapters/reference-v3/14-platform-playbook-postgresql.md)
- [CHAPTER 15 · Platform Playbook · BigQuery](../chapters/reference-v3/15-platform-playbook-bigquery.md)
- [CHAPTER 16 · Platform Playbook · ClickHouse](../chapters/reference-v3/16-platform-playbook-clickhouse.md)
- [CHAPTER 17 · Platform Playbook · Snowflake](../chapters/reference-v3/17-platform-playbook-snowflake.md)
- [CHAPTER 18 · Platform Playbook · Trino](../chapters/reference-v3/18-platform-playbook-trino.md)
- [CHAPTER 19 · Platform Playbook · NoSQL + SQL Layer](../chapters/reference-v3/19-platform-playbook-nosql-sql-layer.md)
- [CHAPTER 20 · Platform Playbook · Databricks](../chapters/reference-v3/20-platform-playbook-databricks.md)

## 명령·문제해결 부록

- [APPENDIX A · Companion Pack, Example Data, Bootstrap, Answer Keys](../chapters/reference-v3/appendix-a-companion-pack-bootstrap-and-answer-keys.md)
- [APPENDIX B · DBT 명령어 레퍼런스](../chapters/reference-v3/appendix-b-dbt-command-reference.md)
- [APPENDIX C · Jinja, Macro, Extensibility Reference](../chapters/reference-v3/appendix-c-jinja-macro-and-extensibility-reference.md)
- [APPENDIX D · Troubleshooting, Decision Guides, Glossary, Official Sources, Support Matrix](../chapters/reference-v3/appendix-d-troubleshooting-decision-guides-glossary-and-support-matrix.md)

## 설계·운영 문서

- [마당마켓 설계·운영 문서 묶음](../governance/README.md)
- [ADR-001 · 마당마켓의 기본 아키텍처](../governance/adr-001-architecture.md)
- [데이터 계약 · 마당마켓 기준선](../governance/data-contract.md)
- [마당마켓 버스 매트릭스](../governance/bus-matrix.md)
- [마당마켓 운영 runbook · 설계용](../governance/operations-runbook.md)
- [공개 모델 변경 정책 · 예시](../governance/change-policy.md)
- [실행·설계·플랫폼 적용의 구분](../governance/capability-matrix.md)

## 실습·출처·검증

- [마당마켓 실습 프로젝트](../lab/README.md)
- [참고 자료와 검증 경계](../references/README.md)
- [전달 검증 보고서](../reports/delivery-validation.md)
