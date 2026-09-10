# 체크포인트 10 · three-domains

웹 이벤트와 구독을 더하되 매출·활성 사용자·MRR의 단위를 섞지 않는다.

데이터 P5, 모델 21개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 10
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
