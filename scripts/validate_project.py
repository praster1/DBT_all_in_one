#!/usr/bin/env python3
"""실제 SQL/체크포인트와 새 Python/YAML/자산을 검사한다. dbt 엔진 검사는 아니다."""
from __future__ import annotations
import ast,hashlib,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'lab'))
import run_reference,run_stage,run_comparisons

def main():
    sql=run_reference.run_suite();comp=run_comparisons.run()
    checkpoints=[run_stage.run(i) for i in range(1,12)]
    declared=json.loads((ROOT/'lab/checkpoints.json').read_text())
    for cp,meta in zip(checkpoints,declared):
        assert cp['phase']==meta['phase'] and cp['model_count']==len(meta['models']),meta['stage']
        assert cp['rows'],f"empty checkpoint {cp['stage']}"
    assert sum(row['recognized_cents'] for row in checkpoints[-1]['rows'])==13000
    pythons=list((ROOT/'lab').rglob('*.py'))+list((ROOT/'scripts').glob('*.py'))
    for p in pythons:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    try:import yaml
    except ImportError:raise SystemExit('Full static check requires PyYAML; SQL scripts themselves use only the standard library.')
    class UniqueLoader(yaml.SafeLoader):pass
    def mapping(loader,node,deep=False):
        result={}
        for k,v in node.value:
            key=loader.construct_object(k,deep=deep)
            if key in result:raise ValueError(f'duplicate YAML key {key}')
            result[key]=loader.construct_object(v,deep=deep)
        return result
    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,mapping)
    ymls=list((ROOT/'lab').rglob('*.yml'))+list((ROOT/'governance').glob('*.yml'))
    for p in ymls:
        data=yaml.load(p.read_text(encoding='utf-8'),Loader=UniqueLoader)
        if p.name=='dbt_project.yml':assert data['name']==data['profile']=='madang_market'
    svgs=list((ROOT/'assets/figures').glob('*.svg'))+list((ROOT/'chapters/images').glob('*.svg'))
    for p in svgs:ET.fromstring(p.read_bytes())
    manifest=json.loads((ROOT/'assets/screenshot-manifest.json').read_text())
    from PIL import Image
    for m in manifest:
        with Image.open(ROOT/m['image']) as im:
            im.verify()
    forbidden=['한빛마켓','한빛 마켓','Hanbit Market','hanbit_market','누리상점','NURI SHOP','nuri_shop']
    bad=[]
    for p in ROOT.rglob('*'):
        if not p.is_file() or 'archive' in p.parts or p.suffix not in {'.md','.py','.sql','.json','.yml','.svg','.dot','.html','.csv'} or p.name=='validate_project.py':continue
        s=p.read_text(encoding='utf-8')
        if any(x in s for x in forbidden):bad.append(str(p.relative_to(ROOT)))
    # Validation source code is deliberately excluded from the publication/source browser name scan.
    if bad:raise AssertionError('old market placeholders remain: '+', '.join(bad[:12]))
    versions={'python':sys.version.split()[0],'sqlite':run_reference.sqlite3.sqlite_version,'dbt':'NOT EXECUTED','duckdb':'NOT EXECUTED'}
    orig=ROOT/'archive/original-upload.zip'
    stats={'book_chapters':len(list((ROOT/'journey').glob('[0-9]*.md')))+len(list((ROOT/'patterns').glob('[0-9]*.md')))+len(list((ROOT/'chapters').glob('[0-9]*.md')))+len(list((ROOT/'chapters').glob('appendix-*.md'))),
      'journey_chapters':17,'pattern_chapters':26,'reference_chapters':25,'sql_models':len(run_reference.LAYERS),'data_phases':5,
      'sql_reference_checks':sql['check_count'],'sql_reference_passed':sql['passed'],'comparison_checks':comp['check_count'],'comparison_passed':comp['passed'],
      'checkpoints_executed':len(checkpoints),'python_files_parsed':len(pythons),'yaml_files_parsed':len(ymls),'svg_files_parsed':len(svgs),'new_concept_figures':len(list((ROOT/'assets/figures').glob('*.svg'))),'original_figures':len(list((ROOT/'chapters/images').glob('*.svg'))),'actual_viewer_screenshots':len(manifest),'old_brand_occurrences':0,
      'original_zip_sha256':hashlib.sha256(orig.read_bytes()).hexdigest(),'versions':versions}
    reports=ROOT/'reports';reports.mkdir(exist_ok=True)
    for n,data in [('sql-reference-validation.json',sql),('model-comparisons.json',comp),('checkpoint-results.json',checkpoints),('static-validation.json',stats)]:
        (reports/n).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
