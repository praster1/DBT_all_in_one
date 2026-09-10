# J14 · 이름·소유권·권한을 코드 밖에서도 관리하기

상점 이름은 마당마켓이고 dbt 프로젝트 이름은 `madang_market`이다. 그러나 프로젝트 표시 이름, source 이름, 모델 이름, 스키마 이름은 각각 다른 식별자다. 이름 변경이 생겼다고 모든 논리 모델의 공개 이름을 한 번에 깨뜨릴 필요는 없다.

## 논리 계층과 물리 위치를 분리한다

`dbt_project.yml`의 raw_schema, schema_l1, schema_l2, schema_l3를 통해 물리 위치를 설정한다. SQL은 source/ref를 유지한다. 기본값은 l0_cus~l3_cus이고, 독자 로컬 개발 target은 book_dev다.

![논리 모델과 환경별 물리 위치 매핑](../assets/figures/routing.svg)

```yaml
name: madang_market
profile: madang_market
vars:
  raw_schema: l0_cus
  schema_l1: l1_cus
  schema_l2: l2_cus
  schema_l3: l3_cus
```

이 조각만 복사해 기존 프로젝트를 덮지 않는다. 완전한 파일은 `lab/dbt/dbt_project.yml`에 있다. 기본 dbt schema 생성 규칙은 target schema에 custom schema를 덧붙이므로 개발 모델은 예를 들어 `book_dev_l1_cus`에 배치된다. `+schema: l1_cus`라고 썼다고 반드시 그 이름만 생성되는 것은 아니다. [S16](../references/README.md#s16)

![논리 계층과 기준 실행기의 물리 이름 표현](../assets/screenshots/11-routing.png)

*실제 로컬 SQL 결과 뷰어의 Chromium 캡처. 합성 데이터이며 상용 dbt 화면이나 dbt 엔진 실행 증거가 아니다.*

## 운영 환경의 기존 테이블만 허용한다면

권한으로 신규 schema/table DDL을 제한하고, 사전 점검으로 존재 여부·컬럼·소유자를 확인해야 한다. 이 책의 table 실습을 그대로 실행하면 로컬 모델이 만들어진다. ‘생성 차단 var’를 임의로 선언하는 것만으로 dbt 표준 materialization이 모두 그 정책을 따르는 것은 아니다.

원천·계산·통합·로그의 책임을 나눈다. 컴포넌트는 값을 계산하고 통합 owner가 쓰기를 맡도록 설계할 수 있다. result_mode가 없는 전용 INSERT/UPDATE 입력은 명시적인 입력 메타데이터로 정규화하고, 표식 있는 입력과 혼합해도 연산이 분명해야 한다. 이는 [P18](../patterns/18-components-and-integration.md)의 별도 설계 예이며 기본 마당마켓 SQL이 구현한 운영 MERGE 프레임워크는 아니다.

## 변경 요청 한 장으로 점검하기

스키마 이름을 바꿀 때 source, model config, 외부 소비 SQL, 권한, 로그 relation, 문서, CI 환경을 함께 확인한다. 계층명만 대체했는데 selected graph 밖의 source 선언이 낡아 파싱이 실패할 수도 있다. 선택 실행은 전체 프로젝트 구문·참조 무결성을 자동으로 면제하는 의미가 아니다. [S17](../references/README.md#s17)

---

[이전 장](13-architecture-alternatives.md) · [다음 장](15-release.md) · [전체 안내](../README.md)
