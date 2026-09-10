# 참고 자료와 검증 경계

확장 원고의 외부 개념·제품 구문 확인일: **2026-09-10**. 문서의 `current`·`latest` 경로는 변경될 수 있다. 실행 환경의 버전은 별도로 잠가야 한다. 실제 회사의 저장소·고객 데이터·업무 SQL은 이 확장본에 복제하지 않았다.

<a id="s01"></a>

## S01 · Databricks — Medallion architecture

[Databricks — Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion)

확인 범위: 메달리온의 세 품질 구역. 최초 발명자를 단정하지 않는다.

<a id="s02"></a>

## S02 · dbt — How we structure our dbt projects

[dbt — How we structure our dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

확인 범위: staging, intermediate, marts는 권장 구조이지 강제 스키마 규격이 아니다.

<a id="s03"></a>

## S03 · Kimball Group — Enterprise DW Bus Architecture

[Kimball Group — Enterprise DW Bus Architecture](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/kimball-data-warehouse-bus-architecture/)

확인 범위: 업무 프로세스와 적합 차원의 전사 통합.

<a id="s04"></a>

## S04 · Nathan Marz — How to beat the CAP theorem

[Nathan Marz — How to beat the CAP theorem](https://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html)

확인 범위: 배치·저지연 경로 논의의 원문. 제목을 CAP 정리의 수학적 반박으로 해석하지 않는다.

<a id="s05"></a>

## S05 · Jay Kreps — Questioning the Lambda Architecture (2014-07-02)

[Jay Kreps — Questioning the Lambda Architecture (2014-07-02)](https://www.oreilly.com/radar/questioning-the-lambda-architecture/)

확인 범위: 중복 처리 로직 문제와 로그 재생 접근의 논의.

<a id="s06"></a>

## S06 · Microsoft — Big data architectures

[Microsoft — Big data architectures](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/big-data-architectures)

확인 범위: Lambda, Kappa, lakehouse의 구성과 적용 범위.

<a id="s07"></a>

## S07 · Zhamak Dehghani — Data Mesh Principles and Logical Architecture (2020-12-03)

[Zhamak Dehghani — Data Mesh Principles and Logical Architecture (2020-12-03)](https://martinfowler.com/articles/data-mesh-principles.html)

확인 범위: 도메인 소유권·제품·셀프서비스·연합 거버넌스.

<a id="s08"></a>

## S08 · IBM — What is a data fabric?

[IBM — What is a data fabric?](https://www.ibm.com/think/topics/data-fabric)

확인 범위: 공급업체 관점의 통합·메타데이터 설명. 보편 단일 표준으로 간주하지 않는다.

<a id="s09"></a>

## S09 · Rocha et al. — Kimball and Inmon architecture comparison (2026)

[Rocha et al. — Kimball and Inmon architecture comparison (2026)](https://arxiv.org/abs/2606.27571)

확인 범위: Hub-and-spoke와 bus 비교 연구. 실행 성능의 보편 우열을 증명하지 않는다.

<a id="s10"></a>

## S10 · AutomateDV — Hubs

[AutomateDV — Hubs](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_hubs/)

확인 범위: 업무 키·적재 시각·원천의 역할.

<a id="s11"></a>

## S11 · AutomateDV — Satellites

[AutomateDV — Satellites](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_satellites/)

확인 범위: 속성 이력과 유효시간·적재시간 구분.

<a id="s12"></a>

## S12 · Kimball Group — Dimensional modeling techniques

[Kimball Group — Dimensional modeling techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

확인 범위: 팩트·차원·SCD·bridge 기술의 분류.

<a id="s13"></a>

## S13 · dbt — Incremental models

[dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models)

확인 범위: is_incremental, unique_key, 필터와 재실행 조건.

<a id="s14"></a>

## S14 · dbt — Incremental strategy

[dbt — Incremental strategy](https://docs.getdbt.com/docs/build/incremental-strategy)

확인 범위: 전략별 어댑터 지원 확인이 필요하다.

<a id="s15"></a>

## S15 · dbt — Snapshots

[dbt — Snapshots](https://docs.getdbt.com/docs/build/snapshots)

확인 범위: 관측 시점 이력 기록. 원천 CDC 전체 역사를 자동 복원하지 않는다.

<a id="s16"></a>

## S16 · dbt — Custom schemas

[dbt — Custom schemas](https://docs.getdbt.com/docs/build/custom-schemas)

확인 범위: 기본 target schema 접두어와 개발자 격리.

<a id="s17"></a>

## S17 · dbt — Node selection syntax

[dbt — Node selection syntax](https://docs.getdbt.com/reference/node-selection/syntax)

확인 범위: 선택 구문과 그래프 연산자.

<a id="s18"></a>

## S18 · dbt — State comparison caveats

[dbt — State comparison caveats](https://docs.getdbt.com/reference/node-selection/state-comparison-caveats)

확인 범위: 상태 비교의 경계와 기준 manifest 보존.

<a id="s19"></a>

## S19 · dbt — Model contracts

[dbt — Model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts)

확인 범위: 구조 계약과 지원 조건.

<a id="s20"></a>

## S20 · dbt — Unit tests

[dbt — Unit tests](https://docs.getdbt.com/docs/build/unit-tests)

확인 범위: 고정 입력과 예상 결과에 대한 논리 검증.

<a id="s21"></a>

## S21 · Debezium — Outbox event router

[Debezium — Outbox event router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html)

확인 범위: outbox 이벤트 구조와 전달.

<a id="s22"></a>

## S22 · Martin Fowler — Event sourcing

[Martin Fowler — Event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)

확인 범위: 이벤트로 상태 변화를 표현하는 접근.

<a id="s23"></a>

## S23 · Microsoft — CQRS

[Microsoft — CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)

확인 범위: 쓰기·읽기 모델 책임 분리와 복잡성.

<a id="s24"></a>

## S24 · Trino — Concepts

[Trino — Concepts](https://trino.io/docs/current/overview/concepts.html)

확인 범위: 쿼리 엔진·카탈로그·스키마 개념.

<a id="s25"></a>

## S25 · Trino — Iceberg connector

[Trino — Iceberg connector](https://trino.io/docs/current/connector/iceberg.html)

확인 범위: 커넥터 기능과 운영 제약은 실제 버전에서 확인.

<a id="s26"></a>

## S26 · AutomateDV — Staging

[AutomateDV — Staging](https://automate-dv.readthedocs.io/en/latest/tutorial/tut_staging/)

확인 범위: Vault 입력 준비·해시·메타데이터.

<a id="s27"></a>

## S27 · Databricks — What is Medallion Architecture?

[Databricks — What is Medallion Architecture?](https://www.databricks.com/blog/what-is-medallion-architecture)

확인 범위: Bronze/Silver/Gold와 다른 모델링 방식의 조합.

## 코드 검증 수준

`lab/run_reference.py`는 Python 표준 라이브러리의 SQLite로 21개 모델의 SQL 논리를 실행한다. 이것은 dbt 자체의 파싱·매크로·materialization·어댑터·권한 검사가 아니다. `load_duckdb.py`와 `lab/dbt`는 독자의 로컬 dbt 실습용이며, 본 환경에서 통합 실행하지 못했다. 모든 그림은 직접 만든 개념도이며, 스크린샷은 동봉 기준 실행 결과를 표시한 로컬 교재 뷰어의 실제 브라우저 캡처다. 상용 플랫폼 화면으로 위장하지 않는다.

<a id="s28"></a>

## S28 · Anchor Modeling 공식 프로젝트

[Anchor Modeling](https://www.anchormodeling.com/)

확인일 2026-09-10. Anchor·Attribute·Tie·Knot와 시간 기반 모델링의 공식 프로젝트 자료. 교재 축소 SQL은 공식 생성기 결과나 완전 구현이 아니다.

<a id="s29"></a>

## S29 · dbt — Materializations

[dbt — Materializations](https://docs.getdbt.com/docs/build/materializations)

확인일: 2026-09-11. 확인 범위: view・table・ephemeral의 차이와 CTE로 결합되는 ephemeral의 동작.

<a id="s30"></a>

## S30 · dbt — About dbt artifacts

[dbt — About dbt artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts)

확인일: 2026-09-11. 확인 범위: manifest・run_results 등 산출물의 종류와 스키마 버전.

<a id="s31"></a>

## S31 · dbt — Defer

[dbt — Defer](https://docs.getdbt.com/reference/node-selection/defer)

확인일: 2026-09-11. 확인 범위: 상태 기준선과 다른 환경의 relation을 참조할 때의 조건.

<a id="s32"></a>

## S32 · Trino — SELECT / WITH clause

[Trino — SELECT / WITH clause](https://trino.io/docs/current/sql/select.html)

확인일: 2026-09-11. 확인 범위: WITH 정의가 사용 위치에 인라인되는 동작과 반복 참조의 경계.

<a id="s33"></a>

## S33 · dbt — Source freshness

[dbt — Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness)

확인일: 2026-09-11. 확인 범위: 원천 신선도 평가와 실행・설정의 범위.

<a id="s34"></a>

## S34 · dbt — Data tests

[dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests)

확인일: 2026-09-11. 확인 범위: 데이터에 대한 가정과 위반 행을 확인하는 테스트의 역할.

<a id="s35"></a>

## S35 · Martin Fowler — Strangler Fig

[Martin Fowler — Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html)

확인일: 2026-09-11. 확인 범위: 기존 시스템을 단계적으로 대체하는 이행 접근.
