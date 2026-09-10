# 체크포인트 03 · grain-and-quality

고객·상세를 결합하고 품질을 판정한 뒤 주문과 상세 grain을 분리한다.

데이터 P1, 모델 10개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 3
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
