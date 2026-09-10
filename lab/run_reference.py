#!/usr/bin/env python3
"""SQL 학습용 SQLite 기준 실행기. dbt 엔진·어댑터·권한 검증을 대체하지 않는다.
지원하는 템플릿은 리터럴 ref()/source()뿐이다. 나머지 Jinja는 즉시 거부한다.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, sqlite3, sys
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parent
LAYERS = json.loads((ROOT/'model_layers.json').read_text())
SCHEMA = json.loads((ROOT/'schema.json').read_text())
REF = re.compile(r"\{\{\s*ref\(\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*\)\s*\}\}")
SOURCE = re.compile(r"\{\{\s*source\(\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*,\s*['\"]([A-Za-z_][A-Za-z0-9_]*)['\"]\s*\)\s*\}\}")
class GraphError(ValueError): pass

def ident(value: str) -> str:
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', value):
        raise ValueError(f'허용되지 않는 식별자: {value!r}')
    return '"'+value+'"'

def load_models() -> dict[str,str]:
    return {name:(ROOT/'dbt/models'/layer/(name+'.sql')).read_text(encoding='utf-8') for name,layer in LAYERS.items()}

def graph_order(models: dict[str,str]) -> list[str]:
    # 선택 모델뿐 아니라 전체 선언 그래프의 잘못된 입력을 먼저 차단한다.
    for name,sql in models.items():
        for dep in REF.findall(sql):
            if dep not in models: raise GraphError(f'{name}: missing ref {dep}')
        for group,table in SOURCE.findall(sql):
            if group != 'shop_raw' or table not in SCHEMA:
                raise GraphError(f'{name}: missing source {group}.{table}')
        if '{{' in SOURCE.sub('',REF.sub('',sql)) or '{%' in sql:
            raise GraphError(f'{name}: 교육용 실행기에서 지원하지 않는 Jinja')
    done:set[str]=set(); visiting:set[str]=set(); order:list[str]=[]
    def visit(name:str)->None:
        if name in visiting: raise GraphError(f'cyclic dependency: {name}')
        if name in done:return
        visiting.add(name)
        for dep in REF.findall(models[name]):visit(dep)
        visiting.remove(name);done.add(name);order.append(name)
    for name in sorted(models):visit(name)
    return order

class ReferenceLab:
    def __init__(self, path:Path, prefix:str='lab', models:dict[str,str]|None=None, layers:dict[str,str]|None=None):
        ident(prefix)
        self.prefix=prefix
        self.conn=sqlite3.connect(path)
        self.conn.row_factory=sqlite3.Row
        self.layers=layers if layers is not None else LAYERS
        self.models=models if models is not None else load_models()
        self.order=graph_order(self.models)
    def name(self, logical:str)->str:
        if logical in self.layers: return f'{self.prefix}_{self.layers[logical]}_cus__{logical}'
        return f'{self.prefix}_l0_cus__{logical}'
    def q(self, logical:str)->str:return ident(self.name(logical))
    def sql(self, text:str)->str:
        text=REF.sub(lambda m:self.q(m.group(1)),text)
        return SOURCE.sub(lambda m:self.q(m.group(2)),text)
    def load(self, phase:int)->None:
        with self.conn:
            for table,columns in SCHEMA.items():
                self.conn.execute(f'DROP TABLE IF EXISTS {self.q(table)}')
                ddl=','.join(f'{ident(k)} {v}' for k,v in columns.items())
                self.conn.execute(f'CREATE TABLE {self.q(table)} ({ddl})')
                with (ROOT/'data'/f'{table}.csv').open(encoding='utf-8',newline='') as f:
                    rows=[]
                    for row in csv.DictReader(f):
                        if int(row['phase'])<=phase:
                            rows.append([int(row[k]) if typ=='INTEGER' and row[k]!='' else (row[k] or None) for k,typ in columns.items()])
                self.conn.executemany(f'INSERT INTO {self.q(table)} VALUES ({",".join("?" for _ in columns)})',rows)
    def build(self)->None:
        with self.conn:
            for name in self.order:
                self.conn.execute(f'DROP TABLE IF EXISTS {self.q(name)}')
                self.conn.execute(f'CREATE TABLE {self.q(name)} AS {self.sql(self.models[name])}')
    def rows(self,name:str)->list[dict[str,Any]]:
        return [dict(r) for r in self.conn.execute(f'SELECT * FROM {self.q(name)} ORDER BY 1')]
    def scalar(self,sql:str)->Any:return self.conn.execute(self.sql(sql)).fetchone()[0]
    def metrics(self)->dict[str,int]:
        return {
         'current_orders':self.scalar("select count(*) from {{ ref('stg_orders_current') }}"),
         'valid_orders':self.scalar("select count(*) from {{ ref('fct_orders') }}"),
         'quarantined':self.scalar("select count(*) from {{ ref('quarantine_orders') }}"),
         'recognized_cents':self.scalar("select sum(recognized_cents) from {{ ref('fct_orders') }}"),
         'mrr_cents':self.scalar("select mrr_cents from {{ ref('mart_current_mrr') }}"),
         'events':self.scalar("select count(*) from {{ ref('stg_events') }}"),
         'order5003_cents':self.scalar("select amount_cents from {{ ref('fct_orders') }} where order_id=5003")}
    def sync_changed_keys(self,phase:int)->None:
        # 주문 변경뿐 아니라 상세·고객 변경으로 영향받는 주문까지 재계산한다.
        impacted=set(r[0] for r in self.conn.execute(f'SELECT order_id FROM {self.q("order_changes")} WHERE phase=?',(phase,)))
        impacted.update(r[0] for r in self.conn.execute(f'SELECT order_id FROM {self.q("item_changes")} WHERE phase=?',(phase,)))
        impacted.update(r[0] for r in self.conn.execute(f'SELECT o.order_id FROM {self.q("stg_orders_current")} o JOIN {self.q("customer_changes")} c ON o.customer_id=c.customer_id WHERE c.phase=?',(phase,)))
        with self.conn:
            self.conn.execute(f'CREATE TABLE IF NOT EXISTS incremental_orders AS SELECT * FROM {self.q("fct_orders")} WHERE 1=0')
            for oid in sorted(impacted):
                self.conn.execute('DELETE FROM incremental_orders WHERE order_id=?',(oid,))
                # 완전 계산 fct_orders의 행을 복사하지 않고, 동일 변환식을 현재 통합 입력에서 재평가한다.
                candidate=self.sql(self.models['fct_orders'])
                self.conn.execute(f'INSERT INTO incremental_orders SELECT * FROM ({candidate}) AS candidate WHERE order_id=?',(oid,))
    def close(self)->None:self.conn.close()

def run_suite()->dict[str,Any]:
    expected=json.loads((ROOT/'expected/phases.json').read_text())
    lab=ReferenceLab(Path(':memory:'))
    checks=[]; snapshots=[]
    def check(name:str,actual:Any,want:Any)->None:
        ok=actual==want
        checks.append({'name':name,'passed':ok,'actual':actual,'expected':want})
        if not ok: raise AssertionError(f'{name}: expected {want!r}, got {actual!r}')
    for phase in range(1,6):
        lab.load(phase);lab.build()
        metrics=lab.metrics()
        for k,v in expected[str(phase)].items():check(f'P{phase}.{k}',metrics[k],v)
        check(f'P{phase}.partition_accounting',metrics['current_orders'],metrics['valid_orders']+metrics['quarantined'])
        for f in sorted((ROOT/'dbt/tests').glob('*.sql')):
            bad=lab.conn.execute(lab.sql(f.read_text())).fetchall()
            check(f'P{phase}.sqltest.{f.stem}',len(bad),0)
        check(f'P{phase}.unique_order',len({r['order_id'] for r in lab.rows('fct_orders')}),metrics['valid_orders'])
        check(f'P{phase}.mart_reconciliation',sum(r['recognized_cents'] for r in lab.rows('mart_daily_sales')),metrics['recognized_cents'])
        lab.sync_changed_keys(phase)
        actual=[dict(r) for r in lab.conn.execute('SELECT * FROM incremental_orders ORDER BY order_id')]
        check(f'P{phase}.incremental_equals_full',actual,lab.rows('fct_orders'))
        lab.sync_changed_keys(phase)
        repeated=[dict(r) for r in lab.conn.execute('SELECT * FROM incremental_orders ORDER BY order_id')]
        check(f'P{phase}.incremental_retry_idempotence',repeated,actual)
        baseline=lab.rows('fct_orders');lab.build()
        check(f'P{phase}.full_rebuild_idempotence',lab.rows('fct_orders'),baseline)
        if phase>=3:
            check(f'P{phase}.asof_segment5003',next(r['segment_at_order'] for r in lab.rows('fct_orders_asof_segment') if r['order_id']==5003),'standard')
        if phase>=4:
            check(f'P{phase}.tombstone_removed',any(r['order_id']==5004 for r in lab.rows('stg_orders_current')),False)
        snapshots.append({'phase':phase,'metrics':metrics,'orders':lab.rows('fct_orders'),
          'quarantine':lab.rows('quarantine_orders'),'daily_sales':lab.rows('mart_daily_sales'),
          'customer_history':lab.rows('dim_customer_history'),'events':lab.rows('stg_events')})
    # 실제 실행 결과를 비교하는 반례. 성공 로그를 손으로 만들어내지 않는다.
    lab.load(1);lab.build()
    gross=lab.scalar("select sum(amount_cents) from {{ ref('fct_orders') }}")
    fanout=lab.scalar("select sum(o.amount_cents) from {{ ref('fct_orders') }} o join {{ ref('fct_order_lines') }} l on o.order_id=l.order_id")
    check('counterexample.fanout_base',gross,9800);check('counterexample.fanout_wrong',fanout,16900)
    max_day=lab.scalar("select max(order_date) from {{ ref('fct_orders') }}")
    lab.load(2);lab.build()
    missed=lab.conn.execute(f'SELECT order_id FROM {lab.q("stg_orders_current")} WHERE order_id=5005 AND order_date > ?',(max_day,)).fetchall()
    check('counterexample.event_date_watermark_misses_5005',len(missed),0)
    for kind,extra in [('missing_source',"select * from {{ source('missing_group','missing_table') }}"),('missing_ref',"select * from {{ ref('not_declared') }}"),('cycle',"select * from {{ ref('bad') }}")]:
        failed=False
        try:graph_order({**load_models(),'bad':extra})
        except GraphError:failed=True
        check(f'graph_guard.{kind}',failed,True)
    other=ReferenceLab(Path(':memory:'),prefix='renamed')
    other.load(2);other.build();check('routing.namespace_invariance',other.rows('fct_orders'),lab.rows('fct_orders'));other.close()
    lab.close()
    return {'engine':'Python sqlite3 reference executor; NOT dbt','sqlite_version':sqlite3.sqlite_version,
      'scope':'21 literal ref/source SQL models, 5 cumulative phases; not dbt adapter/streaming/cloud validation',
      'check_count':len(checks),'passed':sum(x['passed'] for x in checks),'checks':checks,'phases':snapshots}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify',action='store_true');p.add_argument('--phase',type=int,choices=range(1,6),default=1)
    p.add_argument('--prefix',default='lab');p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.verify:
        result=run_suite(); text=json.dumps(result,ensure_ascii=False,indent=2)
        if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text+'\n',encoding='utf-8')
        print(f"REFERENCE SQL: {result['passed']}/{result['check_count']} checks passed (SQLite {sqlite3.sqlite_version}; NOT dbt)")
        for phase in result['phases']: print('phase',phase['phase'],json.dumps(phase['metrics'],ensure_ascii=False))
    else:
        lab=ReferenceLab(Path(':memory:'),a.prefix);lab.load(a.phase);lab.build()
        print('SQLite reference results — dbt engine NOT executed')
        result={'metrics':lab.metrics(),'orders':lab.rows('fct_orders'),'quarantine':lab.rows('quarantine_orders')}
        print(json.dumps(result,ensure_ascii=False,indent=2));lab.close()
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,sqlite3.Error,AssertionError,OSError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);raise SystemExit(1)
