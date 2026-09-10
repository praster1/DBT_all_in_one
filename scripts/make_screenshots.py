#!/usr/bin/env python3
"""실제 SQLite 검사 산출물을 로컬 HTML에 표시하고 Chromium으로 캡처한다.
상용 dbt UI나 dbt 실행 로그를 흉내내지 않는다. 먼저 SQL 기준 검사를 실행해야 한다.
"""
from pathlib import Path
import argparse,csv,html,json
ROOT=Path(__file__).resolve().parents[1]
def table(rows,columns=None):
 if not rows:return '<p class="empty">0행 — 해당 조건의 결과가 없습니다.</p>'
 cols=columns or list(rows[0]);return '<table><thead><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(row.get(c,'')))+'</td>' for c in cols)+'</tr>' for row in rows)+'</tbody></table>'
def code(text):return '<pre>'+html.escape(text)+'</pre>'
def main():
 p=argparse.ArgumentParser();p.add_argument('--chromium',default='/usr/bin/chromium');a=p.parse_args()
 from playwright.sync_api import sync_playwright
 report=json.loads((ROOT/'reports/sql-reference-validation.json').read_text())
 phases={x['phase']:x for x in report['phases']};screens=[]
 def add(slug,title,subtitle,body):screens.append((slug,title,subtitle,body))
 add('01-baseline','01 / 네 주문에서 출발하기','P1 · fct_orders · 주문 grain',table(phases[1]['orders'])+'<p class="callout">헤더 총액은 98.00. 인정 상태만 계산한 매출은 27.00입니다. 5003은 placed 상태입니다.</p>')
 raw=list(csv.DictReader((ROOT/'lab/data/order_changes.csv').open()))
 add('02-deduplication','02 / 같은 변경이 두 번 도착했습니다','P2 · 수신 행과 업무 변경의 차이',table([x for x in raw if x['order_id']=='5005'],['ingestion_id','change_id','order_id','amount_cents','source_seq'])+'<h2>최신 상태 결과</h2>'+table([x for x in phases[2]['orders'] if x['order_id']==5005]))
 add('03-grain','03 / SQL은 성공했지만 합계가 틀렸습니다','P1 · 실제 반례 쿼리의 계산 결과',code('select sum(o.amount_cents)\nfrom fct_orders o join fct_order_lines l\n  on o.order_id = l.order_id;')+table([{'계산':'헤더 grain에서 합산','cents':9800,'표시 금액':'98.00'},{'계산':'상세에 헤더 금액을 복제한 잘못된 합산','cents':16900,'표시 금액':'169.00'}])+'<p class="callout">같은 금액의 서로 다른 주문이 있을 수 있으므로 SUM(DISTINCT amount)로 덮지 않습니다.</p>')
 add('04-late-arrival','04 / 지난 날짜의 매출이 달라졌습니다','P2 · 주문 5005는 4월 1일 주문이지만 나중에 도착',table(phases[2]['daily_sales'])+'<h2>5005 현재 상태</h2>'+table([x for x in phases[2]['orders'] if x['order_id']==5005]))
 add('05-correction','05 / 같은 주문의 정정과 다른 주문의 취소','P2 → P3 · 5003 금액 정정 + 5002 취소',table([dict(phase=ph,**x) for ph in (2,3) for x in phases[ph]['orders'] if x['order_id'] in (5002,5003)])+'<p class="callout">118.00 + 4.00 − 15.00 = 107.00. 오래된 5003 v1 재전송은 현재 값을 되돌리지 않습니다.</p>')
 add('06-delete','06 / 삭제 이후 옛 주문을 되살리지 않기','P4 · 최신 tombstone 적용 후 정상 결과',table(phases[4]['orders'])+'<p class="callout">5004는 현재 투영에서 제외됩니다. 5006·5007은 삭제가 아니라 품질 격리입니다.</p>')
 add('07-history','07 / 오늘의 등급과 주문 당시의 등급','P3 · 고객 103의 유효시간 구간',table([x for x in phases[3]['customer_history'] if x['customer_id']==103])+code("order_time >= valid_from\nand (order_time < valid_to or valid_to is null)")+'<p class="callout">5003의 주문일은 4월 2일입니다. 현재 고객은 VIP여도 주문 당시 분류는 standard입니다.</p>')
 add('08-quarantine','08 / 사라진 행을 이유와 함께 남깁니다','P4 · quarantine_orders · 실제 기준 SQL 결과',table(phases[4]['quarantine'],['order_id','customer_id','amount_cents','quality_status'])+'<p class="callout">현재 6행 = 정상 4행 + 격리 2행. 계산 성공과 발행 승인은 별개입니다.</p>')
 add('09-repair','09 / 원천 정정 후 정상 경로로 돌아옵니다','P5 · 고객 104 도착 + 5007 금액 정정',table(phases[5]['orders'])+'<p class="callout">격리 0행. 인정 매출 130.00. 주문 5006은 주문 변경이 없어도 고객 도착 때문에 재계산됩니다.</p>')
 checks=[{'검사':x['name'],'결과':'PASS' if x['passed'] else 'FAIL'} for x in report['checks'] if 'incremental_' in x['name']]
 add('10-incremental','10 / 증분은 전체 계산과 같은 결과를 내는가','P1–P5 · 변경 키 교체와 같은 배치 재시도',table(checks)+'<p class="callout">소규모 SQLite 트랜잭션에서 검증했습니다. 분산 엔진의 동시성·어댑터 검증은 포함하지 않습니다.</p>')
 layers=json.loads((ROOT/'lab/model_layers.json').read_text())
 add('11-routing','11 / 논리 모델과 물리 이름을 구분합니다','기준 실행기의 이름 표현 · dbt schema 생성 결과가 아님',table([{'논리 모델':n,'계층':l,'SQLite 기준 relation':f'lab_{l}_cus__{n}'} for n,l in layers.items()][:10])+'<p class="callout">dbt 로컬 실습의 실제 개발 스키마는 기본 설정상 book_dev_l1_cus 등입니다.</p>')
 add('12-final','12 / 결과를 재현하고 검증 범위를 설명합니다','21개 모델 · 5단계 데이터 · 실제 검사 결과',table([{'단계':x['phase'],'현재 주문':x['metrics']['current_orders'],'정상':x['metrics']['valid_orders'],'격리':x['metrics']['quarantined'],'인정 매출':f"{x['metrics']['recognized_cents']/100:.2f}",'MRR':f"{x['metrics']['mrr_cents']/100:.2f}"} for x in report['phases']])+f'<p class="callout">SQLite 기준 검사 {report["passed"]}/{report["check_count"]} 통과. dbt 엔진·어댑터·클라우드 통합 실행은 미검증입니다.</p>')
 out=ROOT/'assets/screenshots';view=ROOT/'reports/viewer';view.mkdir(parents=True,exist_ok=True);out.mkdir(parents=True,exist_ok=True)
 css='''body{margin:0;background:#eaf0f4;color:#15323a;font:18px/1.6 "Noto Sans CJK KR","Malgun Gothic",sans-serif}header{background:#12363e;color:white;padding:24px 42px;display:flex;justify-content:space-between;align-items:center}header b{font-size:23px}header span{border:1px solid #729ca2;padding:5px 13px;border-radius:20px;font-size:14px}.panel{margin:26px 36px;background:white;border:1px solid #ccdce0;border-radius:16px;padding:30px 38px}h1{font-size:32px;margin:0 0 8px;letter-spacing:-1px}h2{font-size:23px;margin:26px 0 12px}.sub{color:#58717a;margin:0 0 26px}table{width:100%;border-collapse:collapse;font-size:17px}th{text-align:left;background:#edf5f7;font-weight:700}td,th{border-bottom:1px solid #dce7e9;padding:11px 12px}tbody tr:nth-child(even){background:#f7fafb}.callout{border-left:5px solid #2a818c;background:#eef7f8;padding:18px 22px;margin:28px 0 0}pre{font:17px/1.65 Consolas,monospace;background:#183a43;color:#f3fafb;padding:22px;border-radius:8px;white-space:pre-wrap}footer{margin:20px 42px 28px;color:#526d74;font-size:14px}a{color:inherit}.empty{padding:30px;background:#edf5f7}'''
 manifests=[]
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path=a.chromium,headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1500,'height':1100},device_scale_factor=1)
  for slug,title,subtitle,body in screens:
   doc='<!doctype html><html lang="ko"><meta charset="utf-8"><title>'+html.escape(title)+'</title><style>'+css+'</style><header><b>마당마켓 · MADANG MARKET / SQL 결과 뷰어</b><span>SQLite reference · 합성 데이터 · NOT dbt UI</span></header><main class="panel"><h1>'+title+'</h1><p class="sub">'+subtitle+'</p>'+body+'</main><footer>DBT All In One · Design Patterns Edition / 실제 기준 SQL 실행 산출물을 표시한 로컬 브라우저 화면 · source: reports/sql-reference-validation.json</footer></html>'
   file=view/f'{slug}.html';file.write_text(doc,encoding='utf-8');page.set_content(doc, wait_until='load');page.evaluate('document.fonts.ready');box=page.locator('footer').bounding_box();page.set_viewport_size({'width':1500,'height':int(box['y']+box['height']+30)});page.screenshot(path=str(out/f'{slug}.png'),full_page=True)
   manifests.append({'image':f'assets/screenshots/{slug}.png','title':title,'kind':'actual Chromium capture of local SQL-results viewer, not dbt UI','source':f'reports/viewer/{slug}.html','data':'reports/sql-reference-validation.json'})
  browser.close()
 (ROOT/'assets/screenshot-manifest.json').write_text(json.dumps(manifests,ensure_ascii=False,indent=2));print('captured',len(screens),'real local-viewer screens')
if __name__=='__main__':main()
