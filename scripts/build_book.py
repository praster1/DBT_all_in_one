#!/usr/bin/env python3
"""Markdown + local figures + source files -> one offline HTML reader. No network access.
Run at any working directory: python scripts/build_book.py
"""
from __future__ import annotations
import base64,html,json,mimetypes,re,sys,unicodedata
from pathlib import Path
from urllib.parse import unquote,urlsplit
try:
    from markdown_it import MarkdownIt
except ImportError:
    raise SystemExit('Install book build dependency: python -m pip install -r requirements-book.txt')
ROOT=Path(__file__).resolve().parents[1]

def slug(s:str)->str:
    s=unicodedata.normalize('NFKC',s).lower()
    return re.sub(r'\s+','-',re.sub(r'[^\w\s-]','',s)).strip('-')

def main():
    book=json.loads((ROOT/'book.json').read_text(encoding='utf-8'))
    paths=[p for g in book['sections'] for p in g['files']]
    ids={p:f'd{i:03}' for i,p in enumerate(paths)}
    md=MarkdownIt('commonmark',{'html':True,'linkify':False}).enable('table')
    parsed={};titles={};anchors={};warnings=[];images=set()
    for path in paths:
        content=(ROOT/path).read_text(encoding='utf-8')
        tokens=md.parse(content);parsed[path]=tokens
        titles[path]=content.splitlines()[0].lstrip('# ')
        seen={}
        for i,t in enumerate(tokens):
            if t.type=='heading_open':
                text=tokens[i+1].content;key=slug(text);n=seen.get(key,0);seen[key]=n+1
                unique=key if not n else f'{key}-{n}'
                target=ids[path]+'--'+unique;t.attrSet('id',target);anchors[(path,unique)]=target
        def register_html(token):
            if token.type in ('html_block','html_inline'):
                def rename(m):
                    key=m.group(2);target=ids[path]+'--'+key;anchors[(path,key)]=target
                    return f'id={m.group(1)}{target}{m.group(1)}'
                token.content=re.sub(r"id=([\"'])([^\"']+)\1",rename,token.content)
            for child in token.children or []:register_html(child)
        for t in tokens:register_html(t)
    sources={}
    allowed={'.sql','.py','.yml','.yaml','.csv','.json','.md','.diff','.txt','.in','.dot','.sh','.ps1','.log','.jsonl','.ini','.toml'}
    for f in sorted(ROOT.rglob('*')):
        if f.name=='validate_project.py':continue
        if not f.is_file() or f.suffix not in allowed or any(x in f.parts for x in ('.venv','__pycache__','archive','docs','.local','target','dbt_packages')):continue
        rel=str(f.relative_to(ROOT))
        try:
            s=f.read_text(encoding='utf-8')
            if len(s)<350000:sources[rel]=s
        except (UnicodeError,OSError):pass
    def resolve(current:str,href:str):
        p=urlsplit(href)
        if p.scheme or p.netloc:return None,p.fragment
        f=(ROOT/current).parent/unquote(p.path) if p.path else ROOT/current
        f=f.resolve()
        try:rel=str(f.relative_to(ROOT))
        except ValueError:return '',p.fragment
        if f.is_dir():rel=str((f/'README.md').relative_to(ROOT))
        return rel,unquote(p.fragment)
    for path,tokens in parsed.items():
        def visit(token):
            if token.type=='link_open':
                href=token.attrGet('href') or '';dest,fragment=resolve(path,href)
                if dest is None:
                    token.attrSet('target','_blank');token.attrSet('rel','noopener noreferrer')
                elif dest in ids:
                    target=anchors.get((dest,fragment),ids[dest]) if fragment else ids[dest]
                    token.attrSet('href','#'+target)
                elif dest in sources:
                    token.attrSet('href','#'+ids[path]);token.attrSet('data-source',dest)
                elif (ROOT/dest).is_file():
                    # A raw non-text attachment remains a ZIP-relative file link.
                    token.attrSet('href',dest);token.attrSet('title','전체 ZIP에서 이 파일을 열 수 있습니다.')
                else:
                    warnings.append({'from':path,'href':href,'kind':'missing_local_link'})
            elif token.type=='image':
                href=token.attrGet('src') or '';dest,_=resolve(path,href)
                if dest and (ROOT/dest).is_file():
                    f=ROOT/dest;mime=mimetypes.guess_type(str(f))[0] or 'application/octet-stream'
                    token.attrSet('src',f'data:{mime};base64,'+base64.b64encode(f.read_bytes()).decode())
                    token.attrSet('loading','lazy');token.attrSet('data-original',dest);token.attrSet('tabindex','0')
                    images.add(dest)
                else:warnings.append({'from':path,'href':href,'kind':'missing_image'})
            for child in token.children or []:visit(child)
        for t in tokens:visit(t)
    sections=[];nav=[];index=0
    for group in book['sections']:
        nav.append('<details open><summary>'+html.escape(group['title'])+'</summary><div>')
        for path in group['files']:
            docid=ids[path];title=titles[path]
            nav.append(f'<a class="navitem" data-doc="{docid}" href="#{docid}">{html.escape(title)}</a>')
            prev=ids[paths[index-1]] if index else None;nextid=ids[paths[index+1]] if index+1<len(paths) else None
            pagers=('<a href="#'+prev+'">← 이전</a>' if prev else '<span></span>')+('<a href="#'+nextid+'">다음 →</a>' if nextid else '<span></span>')
            body=md.renderer.render(parsed[path],md.options,{})
            sections.append(f'<article id="{docid}" data-path="{html.escape(path)}" data-title="{html.escape(title)}" hidden><p class="eyebrow">{html.escape(group["title"])} · {index+1:02} / {len(paths)}</p>{body}<div class="pager">{pagers}</div><p class="sourcepath">원고: {html.escape(path)}</p></article>')
            index+=1
        nav.append('</div></details>')
    options=''.join('<option value="'+html.escape(p)+'">'+html.escape(p)+'</option>' for p in sources)
    source_json=json.dumps(sources,ensure_ascii=False).replace('<','\\u003c')
    css=r'''
:root{--ink:#1b3038;--muted:#5b6f78;--paper:#fff;--bg:#f2f5f6;--border:#dce5e8;--brand:#146674;--panel:#edf5f6;--code:#142e38;--base:17px;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:var(--base)/1.85 "Noto Sans CJK KR","Malgun Gothic","Apple SD Gothic Neo",sans-serif}body.dark{--ink:#dce8ec;--muted:#a5b9c3;--paper:#142831;--bg:#0d1c23;--border:#34505e;--brand:#7ed0d9;--panel:#1d3741;--code:#0b1b23;color-scheme:dark}a{color:var(--brand);text-underline-offset:3px}button,input,select{font:inherit}button{cursor:pointer;border:1px solid var(--border);border-radius:7px;padding:5px 11px;background:var(--paper);color:var(--ink)}button:hover{background:var(--panel)}.skip{position:absolute;left:-999px}.skip:focus{left:20px;top:8px;z-index:20;background:white;padding:8px}header{height:76px;position:fixed;inset:0 0 auto;background:#102f3b;color:#f3f8fa;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:0 25px;gap:16px;border-bottom:3px solid #3ea4af}header .brand{font:700 21px/1.3 sans-serif;letter-spacing:.4px}header small{display:block;color:#bfdbe2;font-size:12px;letter-spacing:1px;margin-top:5px}header .tools{display:flex;gap:6px;align-items:center;flex-shrink:0}header .tools button{white-space:nowrap}header>div:first-child{min-width:0}header button{font-size:13px;background:#1d4552;color:#f1f7f9;border-color:#476775}#menu{display:none}aside{position:fixed;left:0;top:76px;bottom:0;width:306px;overflow:auto;border-right:1px solid var(--border);background:var(--paper);padding:21px 17px 50px;z-index:9}.searchlabel{font-size:12px;color:var(--muted);display:block;margin-bottom:7px}#search{width:100%;border:1px solid var(--border);border-radius:8px;padding:10px 12px;background:var(--bg);color:var(--ink);font-size:14px}#searchstatus{font-size:12px;color:var(--muted);min-height:24px;margin:6px 0 12px}details{border-top:1px solid var(--border);padding:10px 0}summary{cursor:pointer;color:var(--muted);font-size:12px;font-weight:700;letter-spacing:.4px}.navitem{display:block;text-decoration:none;font-size:13px;line-height:1.6;padding:7px 10px;margin:3px 0;border-left:3px solid transparent;border-radius:0 6px 6px 0;color:var(--ink);word-break:keep-all}.navitem:hover{background:var(--panel)}.navitem.active{border-left-color:var(--brand);background:var(--panel);font-weight:700}main{margin:105px 32px 55px 338px;max-width:1070px}article{padding:44px 58px;background:var(--paper);border:1px solid var(--border);border-radius:13px;box-shadow:0 5px 22px #152e3507}[hidden]{display:none!important}.eyebrow{font-size:12px;color:var(--brand);font-weight:700;letter-spacing:.8px;margin:0 0 25px}article [id]{scroll-margin-top:100px}h1{font-size:34px;line-height:1.45;letter-spacing:-1px;margin:0 0 28px;word-break:keep-all}h2{font-size:25px;line-height:1.5;margin:45px 0 18px;padding-top:8px;border-bottom:1px solid var(--border);padding-bottom:12px;word-break:keep-all}h3{font-size:20px;margin:32px 0 14px}h4{font-size:18px}p{margin:16px 0}strong{font-weight:700}blockquote{margin:22px 0;padding:3px 22px;border-left:4px solid var(--brand);background:var(--panel);font-size:15px;color:var(--ink)}ul,ol{padding-left:25px}li{margin:7px 0}code{font-family:Consolas,"Liberation Mono",monospace;font-size:.88em;overflow-wrap:anywhere;background:var(--panel);padding:2px 5px;border-radius:4px}pre{position:relative;background:var(--code);color:#e9f4f8;border:1px solid #254652;border-radius:10px;padding:25px 21px 20px;overflow-x:auto;font:14px/1.75 Consolas,"Liberation Mono",monospace;margin:22px 0}pre code{padding:0;background:none;border:0;color:inherit;white-space:pre;overflow-wrap:normal;font:inherit}pre .copy{position:sticky;float:right;top:4px;right:5px;font-size:11px;line-height:1.5;color:#eaf4f7;background:#315563;border:0;margin:-16px -10px 0 0}.tablewrap{overflow-x:auto;margin:20px 0}table{border-collapse:collapse;font-size:14px;line-height:1.8;min-width:100%;margin:0}td,th{text-align:left;vertical-align:top;border-bottom:1px solid var(--border);padding:12px 14px;min-width:70px}th{background:var(--panel);white-space:normal}td{overflow-wrap:anywhere}table code{font-size:12px}img{display:block;max-width:100%;height:auto;background:white;border:1px solid var(--border);border-radius:9px;margin:24px auto;cursor:zoom-in}img:hover{outline:2px solid var(--brand)}hr{border:0;border-top:1px solid var(--border);margin:35px 0}.pager{display:flex;justify-content:space-between;border-top:1px solid var(--border);padding-top:22px;margin-top:44px}.pager a{text-decoration:none;font-size:15px}.sourcepath{font:11px/1.6 monospace;color:var(--muted);margin-top:28px}.bottomnote{font-size:12px;line-height:1.7;color:var(--muted);margin:23px 0}#progress{position:fixed;top:73px;left:0;height:3px;background:#8fddbd;z-index:11;width:0}dialog{border:1px solid var(--border);border-radius:12px;padding:23px;background:var(--paper);color:var(--ink);width:min(1180px,96vw);max-height:94vh}dialog::backdrop{background:#0c222dcc}.dialogbar{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-bottom:15px}#imagecanvas{max-height:75vh;overflow:auto;background:var(--bg);padding:10px}#imagecanvas img{max-width:none;margin:0 auto;cursor:default}#sourcecode{max-height:65vh;white-space:pre;overflow:auto}#sourcechoose{min-width:0;width:100%;background:var(--bg);color:var(--ink);border:1px solid var(--border);padding:8px;font-size:13px}#sourcetitle{font-size:15px;overflow-wrap:anywhere}#toast{position:fixed;bottom:24px;right:30px;border-radius:9px;background:#153e4c;color:white;padding:10px 16px;z-index:30;font-size:14px;display:none}.mobiletitle{display:none}
@media(min-width:1510px){main{margin-left:calc(306px + (100vw - 306px - 1070px)/2)}}
@media(max-width:1050px){aside{width:266px}main{margin-left:286px;margin-right:18px}article{padding:32px 30px}header .tools button{padding:5px 7px}}
@media(max-width:760px){#menu{display:inline-block}header{height:68px;padding:0 12px}header .brand{font-size:17px}header small{font-size:10px;letter-spacing:0;max-width:175px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}header .tools{gap:4px}.desktoponly{display:none}#progress{top:65px}aside{top:68px;width:min(320px,90vw);transform:translateX(-105%);box-shadow:10px 0 40px #142d3b22}body.menuopen aside{transform:translateX(0)}main{margin:86px 10px 28px;max-width:none}article{padding:25px 20px;border-radius:9px}h1{font-size:27px}h2{font-size:22px}body{--base:16px}pre{font-size:12px;padding:23px 15px 15px}td,th{padding:10px;font-size:13px}.eyebrow{font-size:11px}dialog{padding:14px}#sourcecode{font-size:11px}header .tools button{font-size:11px}img{margin:19px auto}}
@media print{header,aside,#progress,.pager,.sourcepath,.copy,.bottomnote,dialog,#toast{display:none!important}body{background:white;color:black;font-size:11pt}main{margin:0;max-width:none}article{border:0;border-radius:0;padding:0;box-shadow:none}body.printall article[hidden]{display:block!important}body.printall article{break-before:page}body.printall article:first-child{break-before:auto}h1{font-size:23pt}h2{font-size:17pt;break-after:avoid}h3{break-after:avoid}img{max-height:21cm;break-inside:avoid}pre{white-space:pre-wrap;overflow:visible;background:#f3f5f6!important;color:black!important;font-size:9pt}pre code{white-space:pre-wrap}table{font-size:9pt}.tablewrap{overflow:visible}td,th{font-size:9pt}a{color:#174758;text-decoration:none}.eyebrow{font-size:9pt}}
'''
    js=r'''
const articles=[...document.querySelectorAll('article')],links=[...document.querySelectorAll('.navitem')];
const sources=JSON.parse(document.getElementById('sources-data').textContent);
let current=articles[0].id;
function toast(text){const t=document.getElementById('toast');t.textContent=text;t.style.display='block';setTimeout(()=>t.style.display='none',1500)}
function route(){const hash=decodeURIComponent(location.hash.slice(1));let id=hash.split('--')[0];if(!document.getElementById(id)?.matches('article'))id=articles[0].id;current=id;articles.forEach(a=>a.hidden=a.id!==id);links.forEach(a=>a.classList.toggle('active',a.dataset.doc===id));document.title=document.getElementById(id).dataset.title+' · 마당마켓';document.body.classList.remove('menuopen');requestAnimationFrame(()=>{if(hash.includes('--'))document.getElementById(hash)?.scrollIntoView({block:'start'});else scrollTo({top:0,behavior:'instant'});progress()});try{localStorage.setItem('madang-last',location.hash)}catch(e){}}
function progress(){const max=document.documentElement.scrollHeight-innerHeight;document.getElementById('progress').style.width=(max>0?Math.min(100,scrollY/max*100):100)+'%'}
window.addEventListener('hashchange',route);window.addEventListener('scroll',progress,{passive:true});
document.getElementById('menu').onclick=()=>document.body.classList.toggle('menuopen');
let dark=false;try{dark=localStorage.getItem('madang-theme')==='dark'}catch(e){}document.body.classList.toggle('dark',dark);
document.getElementById('theme').onclick=()=>{document.body.classList.toggle('dark');try{localStorage.setItem('madang-theme',document.body.classList.contains('dark')?'dark':'light')}catch(e){}};
document.getElementById('print').onclick=()=>{document.body.classList.remove('printall');print()};
document.getElementById('printall').onclick=()=>{document.body.classList.add('printall');print()};window.addEventListener('afterprint',()=>document.body.classList.remove('printall'));
document.getElementById('search').addEventListener('input',e=>{const q=e.target.value.trim().toLocaleLowerCase();let n=0;links.forEach(a=>{const article=document.getElementById(a.dataset.doc);const yes=!q||article.textContent.toLocaleLowerCase().includes(q);a.hidden=!yes;if(yes)n++});document.querySelectorAll('aside details').forEach(d=>{d.hidden=![...d.querySelectorAll('a')].some(a=>!a.hidden);if(q)d.open=true});document.getElementById('searchstatus').textContent=q?n+'개 문서에서 찾았습니다. 목차를 눌러 이동하세요.':'본문까지 검색 · 그림은 클릭하여 확대'});
async function copyText(text){try{await navigator.clipboard.writeText(text)}catch(e){const box=document.createElement('textarea');box.value=text;document.body.append(box);box.select();document.execCommand('copy');box.remove()}toast('복사했습니다')}
document.querySelectorAll('article pre').forEach(pre=>{const b=document.createElement('button');b.className='copy';b.textContent='코드 복사';b.onclick=()=>copyText(pre.querySelector('code')?.textContent||pre.textContent);pre.prepend(b)});
document.querySelectorAll('article table').forEach(table=>{const wrap=document.createElement('div');wrap.className='tablewrap';table.before(wrap);wrap.append(table)});
const imagedialog=document.getElementById('imagedialog'),zoomimage=document.getElementById('zoomimage');let imagewidth=900;
function showImage(img){zoomimage.src=img.src;zoomimage.alt=img.alt;document.getElementById('imagetitle').textContent=img.alt||'그림 확대';imagewidth=Math.min(1080,innerWidth-90);zoomimage.style.width=imagewidth+'px';imagedialog.showModal()}
document.querySelectorAll('article img').forEach(img=>{img.onclick=()=>showImage(img);img.addEventListener('keydown',e=>{if(e.key==='Enter')showImage(img)})});document.getElementById('imageclose').onclick=()=>imagedialog.close();document.getElementById('zoomin').onclick=()=>{imagewidth=Math.min(4000,imagewidth*1.25);zoomimage.style.width=imagewidth+'px'};document.getElementById('zoomout').onclick=()=>{imagewidth=Math.max(250,imagewidth/1.25);zoomimage.style.width=imagewidth+'px'};
const sourcedialog=document.getElementById('sourcedialog'),select=document.getElementById('sourcechoose');
function source(p){if(!(p in sources))return;select.value=p;document.getElementById('sourcetitle').textContent=p;document.getElementById('sourcecode').textContent=sources[p];if(!sourcedialog.open)sourcedialog.showModal()}
select.onchange=()=>source(select.value);document.getElementById('sourceopen').onclick=()=>source('lab/dbt/dbt_project.yml');document.getElementById('sourceclose').onclick=()=>sourcedialog.close();document.getElementById('sourcecopy').onclick=()=>copyText(document.getElementById('sourcecode').textContent);document.querySelectorAll('[data-source]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();source(a.dataset.source)}));
route();
'''
    output='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="통계마당의 가상 상점 마당마켓으로 배우는 dbt와 데이터 아키텍처 설계 패턴"><title>'''+html.escape(book['title'])+'</title><style>'+css+'''</style></head><body><a class="skip" href="#content">본문으로 이동</a><header><div><span class="brand">DBT ALL IN ONE</span><small>통계마당 · 마당마켓 에디션 / DESIGN PATTERNS & PRACTICE</small></div><div class="tools"><button id="menu" aria-label="목차 열기">목차</button><button id="sourceopen">코드</button><button id="theme">화면 전환</button><button id="print" class="desktoponly">현재 장 인쇄</button><button id="printall" class="desktoponly">전체 인쇄</button></div></header><div id="progress"></div><aside aria-label="책 목차"><label class="searchlabel" for="search">목차 · 본문 검색</label><input id="search" type="search" placeholder="예: 카파, 5003, 멱등성"><div id="searchstatus">본문까지 검색 · 그림은 클릭하여 확대</div>'''+''.join(nav)+'''</aside><main id="content">'''+''.join(sections)+'''<p class="bottomnote">통계마당 · 마당마켓은 합성 교육 사례입니다. 실제 검증 범위는 보고서를 확인하세요. 외부 링크를 제외한 본문·그림·화면·소스 보기는 인터넷 연결이 필요하지 않습니다.</p></main><dialog id="imagedialog"><div class="dialogbar"><strong id="imagetitle"></strong><div><button id="zoomout">−</button> <button id="zoomin">+</button> <button id="imageclose">닫기</button></div></div><div id="imagecanvas"><img id="zoomimage" alt=""></div></dialog><dialog id="sourcedialog"><div class="dialogbar"><strong id="sourcetitle"></strong><div><button id="sourcecopy">복사</button> <button id="sourceclose">닫기</button></div></div><select id="sourcechoose" aria-label="소스 파일 선택">'''+options+'''</select><pre id="sourcecode"></pre></dialog><div id="toast" role="status"></div><script type="application/json" id="sources-data">'''+source_json+'</script><script>'+js+'</script></body></html>'
    out=ROOT/'DBT_all_in_one_Madang_Market.html';out.write_text(output,encoding='utf-8')
    (ROOT/'docs').mkdir(exist_ok=True);(ROOT/'docs/index.html').write_text(output,encoding='utf-8');(ROOT/'docs/.nojekyll').write_text('')
    report={'articles':len(paths),'unique_images_embedded':len(images),'source_files_embedded':len(sources),'html_bytes':out.stat().st_size,'warnings':warnings,'output':out.name}
    (ROOT/'reports/book-build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if any(x['kind']=='missing_image' for x in warnings):raise SystemExit('Missing embedded images')
if __name__=='__main__':main()
