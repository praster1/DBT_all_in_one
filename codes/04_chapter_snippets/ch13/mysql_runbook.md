# MySQL runbook

1. 운영계와 같은 인스턴스인지 확인
2. dev schema 분리
3. 전체 rebuild 대신 --select 사용
4. snapshot 도입 전 timestamp/sql_mode 점검
5. Event Stream은 toy data로만 시작
6. 반복적인 lock/부하가 보이면 DW 이전 검토
