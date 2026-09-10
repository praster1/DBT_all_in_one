# 체크포인트 04 · daily-mart

주문 결과를 일 grain으로 집계한다.

데이터 P1, 모델 11개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 4
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
