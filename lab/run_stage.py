#!/usr/bin/env python3
"""장별 완전한 SQL 체크포인트를 SQLite로 실행한다. dbt의 대체 구현이 아니다."""
import argparse,json
from pathlib import Path
import run_reference as rr
ROOT=Path(__file__).resolve().parent

def run(stage:int):
    meta=next(x for x in json.loads((ROOT/'checkpoints.json').read_text()) if x['stage']==stage)
    files=list((ROOT/meta['path']/'models').rglob('*.sql'))
    lab=rr.ReferenceLab(Path(':memory:'), models={p.stem:p.read_text() for p in files}, layers={p.stem:p.parent.name for p in files})
    lab.load(meta['phase']);lab.build()
    rows=lab.rows(meta['result_model']);lab.close()
    return {'stage':stage,'phase':meta['phase'],'model':meta['result_model'],'model_count':len(files),'engine':'SQLite reference, NOT dbt','rows':rows}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',type=int,choices=range(1,12),required=True)
    a=p.parse_args();print(json.dumps(run(a.stage),ensure_ascii=False,indent=2))
