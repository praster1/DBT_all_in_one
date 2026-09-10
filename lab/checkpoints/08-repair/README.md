# 체크포인트 08 · repair

고객 도착·금액 정정으로 격리 행이 정상으로 재진입한다.

데이터 P5, 모델 14개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 8
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
