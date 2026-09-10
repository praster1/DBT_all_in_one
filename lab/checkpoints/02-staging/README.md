# 체크포인트 02 · staging

전달 중복과 최신 업무 상태를 분리한다. first_orders는 교육을 마치고 제거한다.

데이터 P1, 모델 2개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 2
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
