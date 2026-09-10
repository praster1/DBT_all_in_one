# P17 · 설정 중앙화와 단일 소유자: 스키마가 바뀌어도 SQL은 유지하기

물리 스키마와 논리 모델을 분리하면 환경 변경의 범위를 줄일 수 있다. dbt는 custom schema를 처리할 때 기본적으로 target schema를 포함해 개발 환경을 분리한다. 원하는 이름이 다르게 생겼다고 접두어를 무조건 제거하면 개발자끼리 충돌할 수 있다. [S16](../references/README.md#s16)

![논리 이름에서 물리 relation으로](../assets/figures/routing.svg)

## 1. 네 계층의 이름은 한 곳에서 바꾼다

동봉 `lab/dbt/dbt_project.yml`에는 다음 변수가 있다.

```yaml
vars:
  raw_schema: l0_cus
  schema_l1: l1_cus
  schema_l2: l2_cus
  schema_l3: l3_cus
```

source YAML은 `raw_schema`를 읽고, 모델 폴더별 `+schema`는 해당 계층 변수를 읽는다. 이 로컬 프로젝트의 target schema가 `book_dev`이므로 L1의 실제 모델 스키마는 기본 동작상 `book_dev_l1_cus`가 된다. 입력은 bootstrap이 만든 `l0_cus`를 읽는다. 입력과 출력을 같은 이름 조립 규칙으로 다룬다고 가정하지 않는다.

## 2. 카탈로그와 스키마를 분리한다

Trino 환경을 설계할 때는 source의 catalog와 model의 catalog가 다를 수 있다. `catalog.schema.identifier` 세 부분을 따로 관리한다. 문자열 전체를 `split('.')`로 대충 나누는 방식은 quoting이나 특수 이름에서 위험할 수 있다. 어댑터가 제공하는 relation 표현과 식별자 정책을 확인한다.

이 책의 SQLite 기준 실행기는 물리 스키마 대신 `lab_l1_cus__모델명` 형태로 namespace를 표현한다. 실제 dbt schema 생성기를 실행한 결과가 아니다. `--prefix renamed`로 이름만 바꿔도 결과가 같은지를 별도 검사한다.

## 3. 기존 테이블만 허용하는 환경

실습용 dbt table 모델은 테이블을 만들고 다시 생성할 수 있다. 이미 DBA가 만든 테이블만 사용해야 하는 운영 환경에 그대로 적용하면 정책 위반이다. 모델의 materialization, 초기 relation 탐지, 권한, 임시 테이블, rename·drop·comment·grant 동작까지 확인해야 한다.

`allow_relation_creation=false` 같은 조직별 플래그는 **기본 dbt의 보편적 안전 스위치가 아니다**. 사용자 정의 코드가 그 값을 읽고 실제 DDL을 차단하는지 검증해야 한다. YAML에 값을 적기만 하면 안전해진다고 가르치지 않는다.

이 책은 회사의 기존 테이블을 수정하는 코드를 포함하지 않는다. 모든 로컬 생성·삭제는 교육용 데이터베이스 안에서만 이뤄진다. 실습용 bootstrap에는 운영 접속 정보를 넣지 않는다.

## 4. 물리 테이블마다 쓰기 소유자 하나

논리 모델 두 개가 같은 물리 테이블을 동시에 갱신하면 서로의 결과를 덮거나 중간 상태를 읽을 수 있다. 이름과 alias를 조합해 최종 relation 좌표를 만든 다음 중복 소유자를 검사한다. 외부 ETL도 같은 표를 쓰는지 확인해야 한다.

조회 권한과 쓰기 권한을 구별하고, 승인하지 않은 스키마에는 쓰지 못하도록 DB 계정 권한도 제한한다. 애플리케이션 수준의 검사만으로 모든 실수를 막으려 하지 않는다.

## 5. 로그 위치도 중앙화한다

로그 테이블의 catalog·schema·identifier, 파일 로그 디렉터리, 배치 ID는 환경 설정에서 관리한다. 주문 모델 SQL에 로그 위치를 반복 삽입하지 않는다. 로그 실패가 본 계산을 중단해야 하는지는 정책으로 정하되, 계산 성공과 로그 기록 실패를 둘 다 남길 수 있는 경로가 필요하다.

**연습:** `l1_cus`를 `silver_sales`로 바꾸려면 모든 SQL을 검색·치환해야 하는가?

**해설:** 논리 ref가 유지되고 물리 위치를 중앙 설정으로 결정했다면 폴더 설정·source/target 매핑을 바꾸는 것으로 범위를 줄일 수 있다. 다만 문서·권한·하류 소비자·외부 orchestration의 하드코딩도 함께 찾아야 한다. 이름 변경 자체가 데이터 이동이나 권한 변경을 수행하는 것은 아니다.
