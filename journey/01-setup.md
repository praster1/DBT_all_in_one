# J01 · 환경 준비: 실행 종류와 데이터 파일을 혼동하지 않기

이번 장에서는 아무 패키지도 설치하지 않고 데이터 논리를 재현하는 경로와, 실제 dbt를 설치하는 경로를 분리한다. SQLite를 실행했다고 dbt를 실행한 것은 아니다. 화면이 비슷해 보여도 확인한 범위가 다르다.

## 경로 A: 기준 SQL을 먼저 실행한다

Python 3.10 이상을 준비하고 압축을 푼 저장소 루트에서 실행한다. 외부 네트워크, 계정, 데이터웨어하우스가 필요하지 않다. 실행기는 `ref()`와 `source()`의 리터럴 참조만 해석한다. 매크로·어댑터·materialization의 대체 구현이 아니므로 다른 dbt 코드를 무작정 넣지 않는다.

```bash
python lab/run_reference.py --phase 1
python lab/run_reference.py --verify --output reports/sql-reference-validation.json
python lab/run_stage.py --stage 1
```

첫 명령은 네 주문의 결과를 보여준다. 두 번째는 다섯 데이터 단계와 반례를 검증한다. 세 번째는 첫 장에서 필요한 모델 하나만 실행한다. 결과의 `engine`에 SQLite reference가 표시되는지 확인한다. 이것이 현재 책에 실린 실제 검사 경로다.

## 경로 B: 독자의 로컬 환경에서 dbt를 실행한다

아래 명령은 별도 가상환경에 설치하는 절차다. 제공 환경에서는 패키지 저장소의 이름 해석에 실패해 설치·dbt 실행을 확인하지 못했다. `requirements-dbt.in`은 허용 범위이며 검증된 잠금 파일이 아니다. 실제 설치가 성공한 환경에서는 `dbt --version`, Python 버전과 `pip freeze`를 함께 보관한다.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
python -m pip install -r lab/requirements-dbt.in
python lab/load_duckdb.py --phase 1
export BOOK_DB_PATH="$(pwd)/lab/.local/madang_market.duckdb"
dbt debug --project-dir lab/dbt --profiles-dir lab/dbt/profiles
dbt build --project-dir lab/dbt --profiles-dir lab/dbt/profiles
```

PowerShell에서는 `.venv\Scripts\Activate.ps1`로 활성화하고, `$env:BOOK_DB_PATH = (Resolve-Path 'lab/.local/madang_market.duckdb').Path`로 같은 파일을 지정한다. 가상환경 활성화가 정책으로 막힌 환경에서는 `.venv\Scripts\python.exe`와 `.venv\Scripts\dbt.exe`를 직접 사용한다. 운영체제 보안 정책을 임의로 낮추지 않는다.

## 작업 디렉터리를 고정하는 이유

상대 경로의 DuckDB 파일을 쓰면서 중간에 `cd`를 하면 다른 위치의 파일이 생성될 수 있다. 데이터가 사라진 것처럼 보일 때 모델 SQL보다 먼저 데이터 파일의 절대 경로를 확인한다. 이 책의 원천 로더는 `lab/.local/` 밖에 파일을 생성하지 않도록 제한했다. 테스트용 로더를 운영 데이터베이스에 연결하지 않는다.

프로젝트의 기본 materialization은 table이다. 로컬 실습에서는 모델·스키마가 생성될 수 있다. **운영에서 이미 존재하는 테이블만 쓰는 정책과 이 로컬 실습을 혼동하지 않는다.** 운영의 생성 차단은 권한과 별도 실행 정책으로 구현해야 하며 단순한 임의 var 하나로 dbt가 자동 차단해 주는 기능은 아니다.

## 확인 문제

SQLite 검사가 통과했지만 dbt에서 source를 찾지 못했다. 모순인가? 아니다. SQL 결과와 dbt 프로젝트 파싱·어댑터 실행은 다른 검증 계층이다. 실제 환경의 프로필·source 선언·프로젝트 경로를 확인하고, SQLite 결과를 그 문제의 해결 증거로 쓰지 않는다.

---

[이전 장](00-madang-market.md) · [다음 장](02-first-query.md) · [전체 안내](../README.md)
