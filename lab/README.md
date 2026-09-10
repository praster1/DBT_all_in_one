# 마당마켓 실습 프로젝트

마당마켓(Madang Market)은 통계마당에서 이름을 딴 가상 상점이다. 실제 회사 거래·고객 자료가 아니다. 본편 숫자와 시간 흐름의 단일 기준은 이 폴더의 data와 expected다.

## 가장 빠른 실행: 외부 패키지 없음

저장소 루트에서 Python 3.10 이상으로 실행한다.

```bash
python lab/run_reference.py --phase 1
python lab/run_reference.py --verify --output reports/sql-reference-validation.json
python lab/run_stage.py --stage 1
python lab/run_stage.py --stage 11
python lab/run_comparisons.py --output reports/model-comparisons.json
```

기준 실행기는 SQLite이며 dbt 엔진이 아니다. 외부 DB에 연결하지 않고 메모리 안에서 소규모 합성 데이터를 실행한다. 숫자·중복·시간·정정·삭제·격리·영향 키를 확인하는 도구다.

## 코드와 데이터의 단계

checkpoints.json의 01~11은 코드 단계다. 각 폴더에 완전한 dbt 프로젝트 설정·해당 모델·필요한 테스트와 changes.diff가 있다. 첫 단계는 한 모델이고 최종 단계는 21개다. 데이터 P1~P5는 같은 CSV의 phase 값으로 누적된다. 코드 단계 07은 이력 학습을 위해 데이터 P3로 돌아간다.

## 선택 실습: 실제 dbt + DuckDB

아래는 독자 로컬 환경의 실행 절차다. 제공 환경에서는 설치를 완료하지 못했으므로 이 절차를 dbt 실행 통과 기록으로 보지 않는다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r lab/requirements-dbt.in
python lab/load_duckdb.py --phase 1
export BOOK_DB_PATH="$(pwd)/lab/.local/madang_market.duckdb"
dbt debug --project-dir lab/dbt --profiles-dir lab/dbt/profiles
dbt build --project-dir lab/dbt --profiles-dir lab/dbt/profiles
# 다음 입력 단계: 같은 파일을 다시 준비하고 같은 프로젝트를 실행
python lab/load_duckdb.py --phase 2
dbt build --project-dir lab/dbt --profiles-dir lab/dbt/profiles
```

PowerShell: `.venv\Scripts\Activate.ps1` 뒤 `$env:BOOK_DB_PATH = (Resolve-Path 'lab/.local/madang_market.duckdb').Path`로 절대 경로를 설정한다. 항상 저장소 루트에서 실행한다. 원천 로더는 lab/.local 밖의 경로를 거부한다.

단계별 실제 dbt 실행은 다음과 같다. 선택한 체크포인트의 기본 데이터 phase는 checkpoints.json에서 확인한다.

```bash
python lab/load_duckdb.py --phase 1
dbt build --project-dir lab/checkpoints/03-grain-and-quality --profiles-dir lab/dbt/profiles
```

기본 dbt 실습은 table materialization이며 스키마와 모델을 생성·교체할 수 있다. 운영의 기존 테이블 전용 정책과 다르다. production profile이나 실제 회사의 계정을 넣지 않는다. requirements-dbt.in은 잠금 파일이 아니며 성공한 설치의 버전을 freeze해 사용한다.

## 실행하지 않은 범위

SQLite 통과는 dbt parse/compile/build, 어댑터 MERGE, 클라우드 DDL, 동시성·성능·권한의 보증이 아니다. 실제 dbt artifacts는 이 전달본에서 생성하지 않았다. 비교용 Vault·Anchor는 원리를 설명하는 SQL 단편이며 완전한 방법론/생성기 구현이 아니다.

## 파일 찾기

models의 l1/l2/l3가 계산을 담당한다. data는 합성 원천이고 expected는 고정 fixture 예상 지표다. run_reference.py는 기준 SQL, run_stage.py는 장별 재현, run_comparisons.py는 모델링 대안 비교다. SQL tests는 실패 행을 반환하는 검사이며 정상 실행 시 0행을 기대한다.
