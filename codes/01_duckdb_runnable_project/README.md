# 🐥 01_duckdb_runnable_project

DuckDB 기반으로 `dbt` 핵심 흐름을 가장 빠르게 재현하는 실행형 프로젝트입니다.

## ⚡ 빠른 시작

1. Python 가상환경 생성
2. 의존성 설치
   ```bash
   pip install dbt-core dbt-duckdb duckdb
   ```
3. day1 데이터 로드
   ```bash
   bootstrap/load_duckdb.py --db lab.duckdb --variant day1
   ```
4. 아래 profile을 `~/.dbt/profiles.yml`에 저장

   ```yaml
   dbt_all_in_one_lab:
     target: dev
     outputs:
       dev:
         type: duckdb
         path: ./lab.duckdb
         threads: 4
   ```

5. 프로젝트 실행
   ```bash
   cd dbt_all_in_one_lab
   dbt debug
   dbt build --select retail
   dbt build --select events
   dbt build --select subscription
   ```

6. snapshot 실습(day2)
   ```bash
   bootstrap/load_duckdb.py --db lab.duckdb --variant day2
   dbt snapshot
   ```

## 🧭 프로젝트 트랙

- `models/retail/`
- `models/events/`
- `models/subscription/`

## 📌 참고

- `snapshots/`는 legacy SQL 방식 포함
- 책 본문 + `02_reference_patterns/`에서는 최신 YAML 기반 스냅샷 구성도 함께 안내
- `02_reference_patterns/semantic/`, `02_reference_patterns/functions/`는 참고용이며 지원 범위는 dbt 버전/엔진/어댑터에 따라 달라질 수 있음
