#!/usr/bin/env python3
"""Check the offline reader using Chromium; captures are our local reader, not dbt UI."""
from pathlib import Path
import json, re
from playwright.sync_api import sync_playwright
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--chromium',default='/usr/bin/chromium',help='Path to a locally installed Chromium executable')
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]
book=json.loads((ROOT/'book.json').read_text())
paths=[p for g in book['sections'] for p in g['files']]
ids={p:f'd{i:03}' for i,p in enumerate(paths)}
checks=[]
errors=[]
requests=[]
def check(name,condition,detail=None):
    checks.append({'name':name,'passed':bool(condition),'detail':detail})
    print('PASS' if condition else 'FAIL',name,detail,flush=True)
html=(ROOT/'DBT_all_in_one_Madang_Market.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.chromium,headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1500,'height':1000},device_scale_factor=1)
    page.set_default_timeout(5000)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda req:requests.append(req.url))
    page.set_content(html,wait_until='load')
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(200)
    check('79_reader_articles',page.locator('article').count()==79)
    check('root_article_visible',page.locator('article:not([hidden])').count()==1 and page.locator('#d000').is_visible())
    check('madang_brand', '통계마당' in page.locator('header').inner_text() and '마당마켓' in page.locator('header').inner_text())
    check('unique_ids',page.evaluate('''()=>{let a=[...document.querySelectorAll('[id]')].map(x=>x.id);return a.length===new Set(a).size}'''))
    missing=page.evaluate('''()=>[...document.querySelectorAll('a[href^="#"]')].map(x=>x.getAttribute('href').slice(1)).filter(x=>x&&!document.getElementById(decodeURIComponent(x)))''')
    check('internal_anchors_resolve',not missing,missing[:10])
    check('desktop_no_page_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.screenshot(path=str(ROOT/'reports/reader-desktop.png'))
    page.locator('#search').fill('카파')
    visible=page.locator('.navitem:not([hidden])').count()
    check('full_text_search',0<visible<79,{'matched_documents':visible})
    kappa=ids['patterns/05-kappa.md']
    page.locator(f'.navitem[data-doc="{kappa}"]').click()
    page.wait_for_timeout(150)
    check('search_result_navigation',page.locator(f'#{kappa}').is_visible() and page.locator('article:not([hidden])').count()==1)
    page.locator('#search').fill('')
    page.screenshot(path=str(ROOT/'reports/reader-pattern.png'))
    # Test all embedded images, including lazy-loaded images of inactive articles.
    imgres=page.evaluate('''async()=>{const sources=[...new Set([...document.querySelectorAll('article img')].map(x=>x.src))];return await Promise.all(sources.map(src=>new Promise(resolve=>{let x=new Image();x.onload=()=>resolve({ok:x.naturalWidth>0,width:x.naturalWidth});x.onerror=()=>resolve({ok:false});x.src=src})));}''')
    check('116_embedded_images_decode',len(imgres)==116 and all(x['ok'] for x in imgres),{'decoded':sum(x['ok'] for x in imgres),'total':len(imgres)})
    page.locator(f'#{kappa} img').first.click()
    check('figure_modal_opens',page.locator('#imagedialog').evaluate('(e)=>e.open'))
    w=page.locator('#zoomimage').evaluate('(e)=>e.style.width')
    page.locator('#zoomin').click()
    check('figure_zoom',float(page.locator('#zoomimage').evaluate('(e)=>e.style.width').removesuffix('px'))>float(w.removesuffix('px')))
    page.locator('#imageclose').click()
    check('figure_modal_closes',not page.locator('#imagedialog').evaluate('(e)=>e.open'))
    page.locator('#sourceopen').click()
    check('source_modal_opens',page.locator('#sourcedialog').evaluate('(e)=>e.open'))
    code=page.locator('#sourcecode').inner_text()
    check('source_brand',bool(re.search(r'name:\s*madang_market',code)) and bool(re.search(r'profile:\s*madang_market',code)))
    page.locator('#sourcechoose').select_option('lab/data/order_changes.csv')
    check('source_file_switch', '5003' in page.locator('#sourcecode').inner_text())
    page.screenshot(path=str(ROOT/'reports/reader-source.png'))
    page.locator('#sourceclose').click()
    page.locator('#theme').click()
    check('dark_theme',page.locator('body').evaluate('(e)=>e.classList.contains("dark")'))
    page.locator('#theme').click()
    # Source reference link route to S05.
    link=page.locator(f'#{kappa} a[href*="--s05"]').first
    link.click()
    page.wait_for_timeout(100)
    check('source_reference_anchor',page.locator(f'#{ids["references/README.md"]}').is_visible() and page.url.endswith('--s05'))
    # Small viewport, normal layout and menus.
    page.set_viewport_size({'width':390,'height':900})
    page.evaluate('location.hash="d000"')
    page.wait_for_timeout(150)
    check('mobile_no_page_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'),page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})'))
    page.screenshot(path=str(ROOT/'reports/reader-mobile.png'))
    page.locator('#menu').click()
    check('mobile_menu_opens',page.locator('body').evaluate('(e)=>e.classList.contains("menuopen")'))
    # Open section if closed before using nav
    target=ids['journey/04-grain.md']
    page.locator(f'.navitem[data-doc="{target}"]').evaluate('(e)=>e.closest("details").open=true')
    page.locator(f'.navitem[data-doc="{target}"]').click()
    page.wait_for_timeout(150)
    check('mobile_navigation',page.locator(f'#{target}').is_visible() and not page.locator('body').evaluate('(e)=>e.classList.contains("menuopen")'))
    check('mobile_chapter_no_page_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
    page.screenshot(path=str(ROOT/'reports/reader-mobile-chapter.png'))
    check('no_script_errors',not errors,errors)
    external=[r for r in requests if r.startswith(('http:','https:'))]
    check('no_external_network_requests',not external,external)
    browser_version=browser.version
    browser.close()
report={'load_method':'Identical self-contained HTML bytes loaded with Playwright page.set_content; file URL navigation is restricted in the build environment.','browser':'Chromium '+browser_version,'viewports':[{'width':1500,'height':1000},{'width':390,'height':900}],'checks':checks,'check_count':len(checks),'passed':sum(c['passed'] for c in checks),'page_errors':errors,'http_requests':external,'capture_files':['reader-desktop.png','reader-pattern.png','reader-source.png','reader-mobile.png','reader-mobile-chapter.png']}
(ROOT/'reports/reader-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':report['check_count'],'passed':report['passed'],'browser':report['browser']},ensure_ascii=False))
if report['passed']!=report['check_count']:raise SystemExit(1)
