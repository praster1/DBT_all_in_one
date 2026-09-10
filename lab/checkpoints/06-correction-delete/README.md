# 체크포인트 06 · correction-delete

금액 정정·취소·삭제·품질 오류가 발생한 입력까지 재계산한다.

데이터 P4, 모델 11개.

```bash
# 저장소 루트에서
python lab/run_stage.py --stage 6
```

이 명령은 SQLite 기준 실행이다. dbt 엔진 실행은 루트 안내에 따라 별도로 수행한다. `changes.diff`는 직전 체크포인트와의 SQL 차이다.
