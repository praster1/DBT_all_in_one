#!/usr/bin/env python3
"""선택 기능: 로컬 DuckDB 원천 준비. dbt 모델 실행은 별도 명령이다."""
import argparse,csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--phase',required=True,type=int,choices=range(1,6))
    p.add_argument('--path',type=Path,default=ROOT/'.local/madang_market.duckdb')
    p.add_argument('--raw-schema',default='l0_cus')
    a=p.parse_args(); path=a.path.resolve(); allowed=(ROOT/'.local').resolve()
    if not path.is_relative_to(allowed):raise ValueError('실습 보호: 데이터 파일은 lab/.local 안에만 만들 수 있습니다.')
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',a.raw_schema):raise ValueError('스키마 식별자 오류')
    try:import duckdb
    except ImportError:raise RuntimeError('선택 실습에는 duckdb가 필요합니다. requirements-dbt.in을 별도 가상환경에 설치하세요.')
    path.parent.mkdir(parents=True,exist_ok=True)
    schema=json.loads((ROOT/'schema.json').read_text())
    with duckdb.connect(str(path)) as con:
        con.execute('BEGIN TRANSACTION')
        try:
            con.execute(f'CREATE SCHEMA IF NOT EXISTS "{a.raw_schema}"')
            for name,columns in schema.items():
                fullname=f'"{a.raw_schema}"."{name}"'
                con.execute(f'DROP TABLE IF EXISTS {fullname}')
                con.execute(f'CREATE TABLE {fullname} ('+','.join(f'"{k}" {v}' for k,v in columns.items())+')')
                with (ROOT/'data'/f'{name}.csv').open(newline='',encoding='utf-8') as f:
                    rows=[[int(row[k]) if typ=='INTEGER' else row[k] for k,typ in columns.items()] for row in csv.DictReader(f) if int(row['phase'])<=a.phase]
                con.executemany(f'INSERT INTO {fullname} VALUES ({",".join("?" for _ in columns)})',rows)
            con.execute('COMMIT')
        except Exception:
            con.execute('ROLLBACK');raise
    print(f'원천 준비 완료. BOOK_DB_PATH={path}')
if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,OSError) as e:print(str(e),file=sys.stderr);sys.exit(1)
