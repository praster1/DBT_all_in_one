# P24 · Anchor Modeling: 속성의 시간 변화를 더 작게 분리하기

Anchor Modeling은 엔터티 식별, 속성, 관계 등을 나누어 데이터와 시간 변화를 표현하는 접근이다. 공식 프로젝트가 모델링 도구와 자료를 제공한다. 이 장은 마당마켓의 고객 등급을 통해 속성 이력 분리의 의미를 살펴본다. [S28](../references/README.md#s28)

![고객 식별자와 속성 이력의 분리](../assets/figures/anchor.svg)

## 1. 왜 이런 대안이 필요한가

고객의 주소는 자주 바뀌고 등급은 드물게 바뀌며, 특정 속성은 긴 기간 알 수 없을 수 있다. 모든 속성을 같은 넓은 SCD2 행으로 관리하면 한 속성의 변경이 전체 행 버전을 만든다. 속성을 별도로 시간 관리하면 무엇이 언제 바뀌었는지를 더 작은 단위로 표현할 수 있다.

그 대신 읽을 때 여러 속성과 시간 조건을 다시 조합해야 한다. 모델 생성·조회 보조·메타데이터 관리 없이 테이블만 잘게 나누면 복잡성만 늘 수 있다. 속성 분리가 언제 유리한지는 변경 빈도·조회 목적·엔진 특성에 따라 판단한다.

## 2. 네 구성 요소를 구별한다

Anchor는 엔터티의 안정적인 식별을, Attribute는 속성을, Tie는 관계를, Knot는 재사용되는 값 집합을 표현하는 구성으로 이해한다. 모든 모델에 네 요소를 무조건 만들어야 한다는 뜻은 아니다. 공식 생성기와 정식 방법론의 자세한 규칙은 원문 자료에서 확인한다. [S28](../references/README.md#s28)

마당마켓의 축소 실습은 고객 Anchor와 등급 Attribute만 만든다. Tie·Knot·모든 시점 질의·제약 생성까지 구현하지 않았으므로 이것을 완전한 Anchor Modeling 구현이라고 부르지 않는다.

## 3. 같은 고객 103을 표현한다

```sql
-- lab/comparisons/05-anchor-fragment.sql의 핵심
create table cmp_anchor_customer as
select distinct customer_id from {{ source('shop_raw','customer_changes') }};

create table cmp_attribute_segment as
select customer_id, effective_from as valid_from, segment
from {{ source('shop_raw','customer_changes') }};
```

고객 103의 식별자 행은 하나다. segment의 변화는 별도 테이블에서 유효시점별로 남는다. 고객의 현재 속성이 필요한 소비 모델과 주문 당시 속성이 필요한 소비 모델은 서로 다른 조회 조건을 사용한다. 같은 데이터 표현에서도 시간 질문은 사라지지 않는다.

## 4. Data Vault와 비교한다

둘 다 식별·관계·변경을 분리해 이해하도록 돕지만, 구성 단위와 방법론의 규칙을 같은 것으로 취급하지 않는다. Vault의 Hub·Link·Satellite를 이름만 Anchor·Tie·Attribute로 바꾸면 자동으로 Anchor Modeling이 되는 것은 아니다. [P09](09-data-vault.md)의 원천 추적과 이력 보존 목적을 함께 비교한다.

이 책의 두 비교 분기는 동일 고객·주문 fixture로 구조 차이를 보여주는 단편이다. 적재시각·다중 원천·해시 canonicalization·충돌·관계 유효성 등 운영 수준 문제를 모두 해결한 것으로 표시하지 않는다.

## 5. 실행하고 무엇을 확인할 것인가

```bash
python lab/run_comparisons.py --output reports/model-comparisons.json
```

P3·P4·P5에서 같은 정상 현재 주문 결과와 고객의 현재 등급이 나오는지 행 단위로 비교한다. 이 검사는 현재 상태 소비의 동등성을 보이며, 전체 시간 질의의 동등성이나 성능 우위를 증명하지 않는다. 주문 당시 등급 검사는 별도로 J09의 시간 구간 모델에서 수행한다.

## 6. 마당마켓의 채택 판단

기본 상점은 현재의 작은 고객 속성·간단한 이력 요구로 충분하므로 SCD2 구간 모델을 유지한다. 속성별 변경 주기·희소성·확장 요구가 커지고 자동화 도구를 운영할 수 있을 때 Anchor를 다시 비교한다. 채택하지 않는 이유까지 남겨야 패턴 사전이 실제 의사결정 도구가 된다.

**연습:** 고객 이메일만 바뀌었는데 고객의 모든 속성 이력을 복제해야 하는가? 선택한 모델이 무엇을 한 버전으로 취급하는지에 달려 있다. 행 단위 SCD2와 속성별 시간 관리는 서로 다른 변경 단위를 선택한 설계다.
