# 체크포인트 11 · final

최종 모델·검증·문서·발행 설계를 정리한다.

데이터 P5, 모델 21개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 11
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
