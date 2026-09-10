# 체크포인트 05 · late-arrival

동일 코드를 유지하며 지연 도착·중복 재전송 입력을 적용한다.

데이터 P2, 모델 11개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 5
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
