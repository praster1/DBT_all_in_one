# J04 · 테이블의 한 행: 조인으로 매출이 부풀어 오르는 순간

주문과 주문 상세를 결합하면 상품별 분석이 쉬워진다. 그러나 헤더의 주문 금액을 상세 수만큼 복제한 뒤 합산하면 SQL은 성공하면서 숫자는 틀린다. grain은 주석에 적는 장식이 아니라 조인과 집계의 계약이다.

## 먼저 두 모델의 단위를 선언한다

`fct_orders`는 정상 현재 주문 한 건, `fct_order_lines`는 정상 현재 주문의 상세 한 건이다. 주문 5003은 18.00과 11.00의 두 상세를 갖는다. 상세 금액 합은 29.00이지만 주문 금액 29.00을 두 상세에 붙여 더하면 58.00이 된다.

![동일 주문 헤더가 두 상세에 복제되는 반례](../assets/figures/fanout.svg)

```sql
-- 실패 반례: 헤더 금액이 상세 개수만큼 복제된다.
select sum(o.amount_cents)
from {{ ref('fct_orders') }} o
join {{ ref('fct_order_lines') }} l on o.order_id = l.order_id
```

![기준 SQL이 직접 계산한 98.00과 잘못된 169.00](../assets/screenshots/03-grain.png)

*실제 로컬 SQL 결과 뷰어의 Chromium 캡처. 합성 데이터이며 상용 dbt 화면이나 dbt 엔진 실행 증거가 아니다.*

P1 전체를 대상으로 실행하면 정상 헤더 합은 9800, 잘못된 합은 16900이다. `SUM(DISTINCT amount_cents)`로 덮으면 우연히 같은 금액의 다른 주문까지 하나로 합쳐질 수 있다. 중복 제거의 기준은 금액이 아니라 업무 키다.

## 상세를 먼저 주문 grain으로 집계한다

```sql
select order_id, sum(quantity * unit_price_cents) as line_amount_cents,
       count(*) as line_count
from {{ ref('stg_items_current') }} group by order_id
```

이 결과는 주문별 한 행이다. 이후 헤더와 1:1로 대사하고, 불일치한 주문은 숨기지 않고 격리한다. 상품 분석이 필요할 때는 상세 grain의 팩트를 유지한다. 분석 요구가 다르다고 모든 결과를 하나의 거대한 테이블로 합치지는 않는다.

```bash
# 저장소 루트에서 실행 — Python 표준 라이브러리 / SQLite 기준 실행
python lab/run_stage.py --stage 3
```

완전한 해당 단계 소스와 직전 단계 대비 `changes.diff`는 `lab/checkpoints/`에 있다. dbt 실행 명령과 검증 경계는 [실습 안내](../lab/README.md)를 참고한다.

## 연습과 해설

고객 하나에 주문 세 건, 이벤트 열 건이 있다. 둘을 고객 ID로 바로 연결하면 몇 행이 될 수 있는가? 같은 고객 안에서 3×10=30행이 될 수 있다. 주문 지표와 이벤트 지표를 각각 필요한 고객·기간 grain으로 집계한 뒤 연결해야 한다. 같은 문제는 J12의 구독 지표에서도 다시 나타난다.

---

[이전 장](03-staging.md) · [다음 장](05-layers.md) · [전체 안내](../README.md)
