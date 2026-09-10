# 체크포인트 09 · incremental-proof

동일 SQL의 전체 결과를 기준으로 별도 변경 키 갱신의 동등성을 검사한다.

데이터 P5, 모델 14개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 9
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
