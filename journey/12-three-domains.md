# J12 · 주문·웹 방문·구독을 하나의 상점에 연결하기

마당마켓은 상품 주문 외에 웹사이트 방문 이벤트와 정기 구독을 기록한다. 같은 고객을 가리키더라도 세 데이터의 한 행은 다르다. 주문 한 건, 이벤트 한 번, 현재 구독 한 건을 원시 상태로 한꺼번에 조인하면 지표가 증폭된다.

## 웹 이벤트: 이벤트 수와 활성 사용자 수

```sql
with ranked as (
 select *, row_number() over (partition by event_id order by ingestion_id desc) as delivery_rank
 from {{ source('shop_raw', 'events') }}
)
select event_id, customer_id, event_time, substr(event_time,1,10) as event_date, event_type
from ranked where delivery_rank = 1
```
```sql
select event_date, count(distinct customer_id) as active_users
from {{ ref('stg_events') }} group by event_date
```

이벤트의 재전송을 먼저 처리하고 날짜별 고유 사용자를 계산한다. 하루에 같은 사용자가 세 번 방문했다면 이벤트 수는 세 건이어도 DAU는 한 명이다. 여러 날짜의 DAU를 더한 값을 월간 고유 사용자라고 부르지 않는다. 일별 유일 집계는 월 전체의 유일 집계와 더해지는 성질이 다르다.

## 구독: 현재 MRR과 실제 현금 수납

```sql
-- 단일 통화·월간 요금만 있는 실습. MRR은 주문 매출과 합산하지 않는다.
select sum(case when status = 'active' then monthly_cents else 0 end) as mrr_cents
from {{ ref('stg_subscriptions_current') }}
```
```bash
# 저장소 루트에서 실행 — Python 표준 라이브러리 / SQLite 기준 실행
python lab/run_stage.py --stage 10
```

완전한 해당 단계 소스와 직전 단계 대비 `changes.diff`는 `lab/checkpoints/`에 있다. dbt 실행 명령과 검증 경계는 [실습 안내](../lab/README.md)를 참고한다.

MRR은 이 예제에서 active 구독의 월 금액 합이다. trial과 cancelled는 제외한다. 청구서 수납액, 주문 매출, 기간별 수익 인식과 같지 않다. 일할 계산·연간 선결제·할인·환불은 추가 계약이 필요하다.

## 공통 고객 차원을 통해 연결한다

고객 ID가 같다고 해서 이벤트 원시 행과 주문 팩트를 직접 연결할 필요는 없다. 목적에 맞는 고객·기간 grain으로 먼저 각각 요약한 뒤 함께 제공한다. 공통 고객·날짜의 정의는 버스 매트릭스에 적는다. [P03](../patterns/03-kimball-bus.md)

같은 상점이라는 설정은 지표를 무리하게 하나로 합치려는 핑계가 아니다. 한 고객의 주문 매출, 활성 여부, MRR을 나란히 보여줄 수 있지만 서로 다른 통계량을 한 합계로 더해서는 안 된다. 지표마다 기준시점과 포함 조건을 남긴다.

## 다음 요구를 예상한다

다른 서비스의 고객 ID와 연결하려면 identity resolution이 필요하다. 숫자가 같다고 동일 인물이라고 가정하지 않는다. 도메인 팀이 분리되면 공통 고객 모델의 공개 계약과 버전 변경을 협의해야 한다. 이때 허브앤스포크, 버스, 메시의 적용 질문이 실제로 생긴다.

---

[이전 장](11-incremental.md) · [다음 장](13-architecture-alternatives.md) · [전체 안내](../README.md)
