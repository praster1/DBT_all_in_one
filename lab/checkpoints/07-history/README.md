# 체크포인트 07 · history

새 이력 모델과 주문 당시 차원 조인을 추가한다. 이 체크포인트는 시간 학습을 위해 P3를 다시 본다.

데이터 P3, 모델 14개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 7
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
