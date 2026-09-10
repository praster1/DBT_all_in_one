#!/usr/bin/env python3
"""같은 합성 데이터의 모델링 구조를 SQLite에서 비교한다. 아키텍처 배포/성능 시험이 아니다."""
from __future__ import annotations
import argparse,json,sqlite3,sys
from pathlib import Path
from run_reference import ReferenceLab,ROOT

def run():
    checks=[]; outputs=[]
    def equal(name,actual,expected):
        passed=actual==expected
        checks.append(dict(name=name,actual=actual,expected=expected,passed=passed))
        if not passed:raise AssertionError(f"{name}: {actual!r} != {expected!r}")
    # 세 단계에서 정정·삭제·복구가 비교 모델에도 같은 결과를 주는지 확인한다.
    for phase in (3,4,5):
        lab=ReferenceLab(Path(':memory:'));lab.load(phase);lab.build()
        for path in sorted((ROOT/'comparisons').glob('*.sql')):
            lab.conn.executescript(lab.sql(path.read_text(encoding='utf-8')))
        baseline=[dict(x) for x in lab.conn.execute(f"SELECT o.order_id,o.customer_id,c.segment,o.recognized_cents FROM {lab.q('fct_orders')} o JOIN {lab.q('dim_customers')} c ON o.customer_id=c.customer_id ORDER BY o.order_id")]
        for branch in ('star','core','wide','vault','anchor'):
            rows=[dict(x) for x in lab.conn.execute(f'SELECT * FROM cmp_{branch}_result ORDER BY order_id')]
            equal(f'P{phase}.{branch}.row_equivalence',rows,baseline)
            equal(f'P{phase}.{branch}.unique_grain',len({x['order_id'] for x in rows}),len(rows))
        bus=[dict(x) for x in lab.conn.execute('SELECT * FROM cmp_bus_result ORDER BY customer_id')]
        equal(f'P{phase}.bus.sales_conservation',sum(x['sales_cents'] for x in bus),lab.metrics()['recognized_cents'])
        equal(f'P{phase}.bus.mrr_conservation',sum(x['mrr_cents'] for x in bus),lab.metrics()['mrr_cents'])
        outputs.append(dict(phase=phase,order_results=baseline,bus_customer_results=bus))
        lab.close()
    return dict(engine='SQLite reference; NOT dbt',scope='Five modeling fragments + bus aggregation; P3/P4/P5; not certified Vault/Anchor, production architectures, or benchmark',check_count=len(checks),passed=sum(x['passed'] for x in checks),checks=checks,outputs=outputs)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();result=run()
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"MODELING COMPARISONS: {result['passed']}/{result['check_count']} checks passed (SQLite; NOT dbt)")
if __name__=='__main__':
    try:main()
    except (AssertionError,ValueError,OSError,sqlite3.Error) as exc:print('ERROR:',exc,file=sys.stderr);sys.exit(1)
