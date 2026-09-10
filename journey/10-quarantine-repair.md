# J10 · 격리는 끝이 아니라 복구를 위한 대기 상태다

P4의 주문 5006은 고객 104를 참조하지만 고객 데이터는 아직 도착하지 않았다. 주문 5007은 금액이 음수다. INNER JOIN으로 고객 없는 주문을 버리면 결과가 깔끔해 보이지만, 운영자는 무엇이 사라졌는지 알 수 없다.

## 이유를 계산하는 모델을 먼저 만든다

```sql
select o.*, c.segment, t.line_amount_cents,
 case when o.amount_cents is null or o.amount_cents < 0 then 'invalid_amount'
      when o.status is null or o.status not in ('placed','paid','shipped','delivered','cancelled') then 'invalid_status'
      when c.customer_id is null then 'missing_customer'
      when t.order_id is null then 'missing_items'
      when o.amount_cents <> t.line_amount_cents then 'header_line_mismatch'
      else 'accepted' end as quality_status
from {{ ref('stg_orders_current') }} o
left join {{ ref('stg_customers_current') }} c on o.customer_id = c.customer_id
left join {{ ref('int_order_totals') }} t on o.order_id = t.order_id
```

이 예제의 CASE는 우선순위에 따라 대표 오류 한 가지를 돌려준다. 하나의 행에 여러 오류가 있을 수 있는 운영 시스템이라면 오류 배열이나 별도 오류 상세 테이블을 검토한다. ‘대표 사유 한 개’와 ‘모든 오류 탐지’를 같다고 설명하지 않는다.

![P4 정상 4행과 격리 2행의 대사](../assets/screenshots/08-quarantine.png)

*실제 로컬 SQL 결과 뷰어의 Chromium 캡처. 합성 데이터이며 상용 dbt 화면이나 dbt 엔진 실행 증거가 아니다.*

현재 주문 6행 = 정상 4행 + 격리 2행이다. 이 분모는 최신 삭제 표식을 적용한 현재 투영이다. 원천 수신 행 수와 직접 비교하면 재전송·이력 행 때문에 맞지 않는다. 원천 완전성 대사와 현재 상태 대사를 분리한다.

## P5에서 되돌아오는 두 주문

고객 104가 도착하자 주문 5006은 주문 데이터 자체가 바뀌지 않았는데도 정상 상태가 된다. 주문 5007은 원천 금액이 10.00으로 정정되어 정상 경로로 돌아온다. 매출 95.00에 25.00과 10.00이 더해져 130.00이 된다.

```bash
# 저장소 루트에서 실행 — Python 표준 라이브러리 / SQLite 기준 실행
python lab/run_stage.py --stage 8
```

완전한 해당 단계 소스와 직전 단계 대비 `changes.diff`는 `lab/checkpoints/`에 있다. dbt 실행 명령과 검증 경계는 [실습 안내](../lab/README.md)를 참고한다.
![원천 정정과 고객 도착으로 격리 행이 정상 경로에 재진입한다](../assets/screenshots/09-repair.png)

*실제 로컬 SQL 결과 뷰어의 Chromium 캡처. 합성 데이터이며 상용 dbt 화면이나 dbt 엔진 실행 증거가 아니다.*

## 계산 성공과 발행 성공을 구별한다

모델 SQL이 성공했다고 모든 데이터를 공개해야 하는 것은 아니다. 이 책의 정책 예시는 격리 행이 있으면 발행 승인을 보류한다. 부분 공개가 허용되는 업무라면 누락 범위·영향 금액·공개 시각을 함께 표시해야 한다. 무조건 실패나 무조건 통과가 정답인 것은 아니고 정책을 명시해야 한다.

격리 테이블에도 민감정보가 들어갈 수 있다. 정상 마트에서 제외했다는 이유로 더 넓은 권한을 주지 않는다. 접근·보존·복구 소유자까지 함께 설계한다.

---

[이전 장](09-history.md) · [다음 장](11-incremental.md) · [전체 안내](../README.md)
