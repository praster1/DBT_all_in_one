# J06 · 첫 매출 마트: 업무 정의를 코드와 테스트에 고정하기

담당자가 원하는 것은 주문 헤더 금액 총합이 아니라 ‘인정 매출’이다. 우선 어떤 상태를 포함할지 합의한다. 이 예제는 paid·shipped·delivered를 포함하고 placed·cancelled는 0으로 계산한다. 취소 주문 자체를 없애지 않으므로 주문 수와 매출을 독립적으로 설명할 수 있다.

## 주문별 인정 금액을 한 곳에서 정의한다

```sql
select order_id, customer_id, order_date, status, amount_cents,
       case when status in ('paid','shipped','delivered') then amount_cents else 0 end as recognized_cents
from {{ ref('int_orders_valid') }}
```

이 모델은 이미 품질을 통과한 입력만 읽는다. 고객이 없거나 상세 합계가 틀린 행은 다른 경로에 남아 있다. WHERE로 그 행을 버렸다는 사실을 감추지 않고 품질 요약에서 정상·격리 행을 대사한다.

## 일별 마트로 집계한다

```sql
select order_date, count(*) as order_count, sum(recognized_cents) as recognized_cents
from {{ ref('fct_orders') }} group by order_date
```
```bash
# 저장소 루트에서 실행 — Python 표준 라이브러리 / SQLite 기준 실행
python lab/run_stage.py --stage 4
```

완전한 해당 단계 소스와 직전 단계 대비 `changes.diff`는 `lab/checkpoints/`에 있다. dbt 실행 명령과 검증 경계는 [실습 안내](../lab/README.md)를 참고한다.

P1 인정 매출 27.00은 shipped 주문 5002의 15.00과 delivered 주문 5004의 12.00이다. 5001과 5003은 placed이므로 합계에 포함되지 않는다. 숫자를 바꾸기 전에 상태와 원천을 추적하는 습관을 만든다.

## 테스트를 세 층으로 나눈다

행 키의 유일성, 헤더와 상세 대사, 일별 마트와 주문 팩트의 합계 대사는 서로 다른 검사다. 하나가 통과했다고 나머지가 맞다는 보장은 없다. `schema.yml`의 generic tests와 `tests/order_line_reconciliation.sql`, 기준 실행기의 예상 지표를 함께 본다.

```bash
python lab/run_reference.py --verify --output reports/sql-reference-validation.json
```

테스트에 넣은 27.00은 이 작은 고정 fixture의 정답이다. 운영 매출을 매일 27.00과 비교하라는 뜻이 아니다. 운영에서는 원천 완전성, 전일 대비 변화, 허용 오차와 대사 기준을 업무에 맞게 정의한다.

## 문서도 결과의 일부다

설명에는 grain, 포함 상태, 통화 단위, 취소·환불 정책, 기준 시각을 적는다. 이 실습은 부분 환불·다중 통화·세금 계산을 구현하지 않는다. 이런 요구가 생기면 현재 금액 열 하나를 무리하게 확장하지 말고 별도 거래/환불 사실과 환산 시점의 설계를 검토한다. [P12](../patterns/12-fact-patterns.md)로 연결된다.

---

[이전 장](05-layers.md) · [다음 장](07-late-data.md) · [전체 안내](../README.md)
