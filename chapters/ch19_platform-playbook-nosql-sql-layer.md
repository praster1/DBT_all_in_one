# CHAPTER 19 · Platform Playbook · NoSQL + SQL Layer

> 문서형·검색형 원천을 SQL 계층 뒤에 두고 dbt를 변환 계층으로 쓰는 패턴을 Trino와 분리해서 다룬다.

이 장에서 말하는 NoSQL + SQL Layer는 문서형 또는 검색형 원천을 직접 dbt에 붙이기보다, SQL 계층을 앞세운 뒤 dbt는 그 SQL 레이어를 기준으로 source를 정의하는 운영 패턴을 뜻한다. MongoDB + Trino 조합은 그 대표적인 예일 뿐이고, 핵심은 자유로운 원천 스키마를 staging에서 얼마나 보수적으로 정리할 것인가에 있다.

문서형 원천은 키 누락, nested field 차이, 타입 흔들림이 관계형 원천보다 훨씬 흔하다. 따라서 source 선언부터 “무엇을 그대로 가져오고, 무엇을 flatten하며, 어떤 필드를 business key로 볼 것인가”를 더 명시적으로 정해야 한다.

## 19.1. NoSQL + SQL Layer 패턴을 읽는 법

NoSQL + SQL Layer 패턴은 raw JSON 문서를 직접 dbt로 가공한다기보다, Trino 같은 SQL 레이어를 통해 문서 컬렉션을 source처럼 읽고, 결과 marts는 write 가능한 SQL catalog에 남기는 구조로 이해하면 좋다. companion ZIP에는 MongoDB JSONL과 `mongoimport` 스크립트, 그리고 Trino 쪽 bootstrap 예시가 함께 들어 있다. 핵심은 스키마가 느슨한 raw를 그대로 믿지 말고, staging에서 타입과 필수 필드를 더 강하게 정리하는 데 있다.

*MongoDB + Trino day1 예시*

```bash
#!/usr/bin/env bash
set -euo pipefail
# Example: MongoDB import for retail day1
# Adjust MONGO_URI if needed.
MONGO_URI="${MONGO_URI:-mongodb://localhost:27017}"
mongoimport --uri "$MONGO_URI" --db raw_retail --collection __schema --drop --jsonArray --file /dev/null || true
mongoimport --uri "$MONGO_URI" --db raw_retail --collection customers --drop --file customers.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection products --drop --file products.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection order_items --drop --file order_items.jsonl
mongoimport --uri "$MONGO_URI" --db raw_retail --collection orders --drop --file orders_day1.jsonl
```

*코드 · BASH*

### 19.1.1. 세 예제를 NoSQL + SQL Layer 패턴에서 진행할 때의 기준

Retail Orders는 문서 컬렉션을 관계형처럼 정규화하는 연습에 좋고, Event Stream은 이벤트 문서를 session/DAU로 읽는 흐름을 보기 좋다. Subscription & Billing은 문서 저장소에서 상태 추적을 할 때 스키마 일관성이 얼마나 중요한지 보여 준다. 다만 NoSQL + SQL Layer 조합은 “가장 쉬운 운영형 선택”이 아니라, 저장소 다양성과 SQL 접근성을 맞바꾸는 구조라는 점을 기억해야 한다.

# APPENDICES

## 실행·참조·복습을 위한 부록

부록은 본문을 대체하지 않지만, 실습과 운영에서 자주 되돌아오는 참조 지점을 한데 모아 책 전체를 다시 쓰기 쉽게 만든다.
