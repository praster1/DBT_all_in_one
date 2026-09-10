#!/usr/bin/env python3
"""Check native Markdown file/image paths and local anchors (no HTTP requests)."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
from urllib.parse import unquote,urlsplit
from markdown_it import MarkdownIt
from build_markdown import slug

ROOT=Path(__file__).resolve().parents[1]
MD=MarkdownIt('commonmark',{'html':True}).enable('table')
SKIP={'.git','.venv','__pycache__','archive','target','dbt_packages','.publication-payload'}

def parse(path:Path):return MD.parse(path.read_text(encoding='utf-8'))

def anchors(tokens):
    result=set();seen={}
    for i,t in enumerate(tokens):
        if t.type=='heading_open':
            text=''.join(c.content for c in tokens[i+1].children or [] if c.type in ('text','code_inline'))
            base=slug(text);n=seen.get(base,0);seen[base]=n+1
            result.add(base+(f'-{n}' if n else ''))
        if t.type in ('html_block','html_inline'):
            result.update(re.findall(r'\b(?:id|name)=["\']([^"\']+)["\']',t.content))
        for child in t.children or []:
            if child.type=='html_inline':result.update(re.findall(r'\b(?:id|name)=["\']([^"\']+)["\']',child.content))
    return result

def urls(tokens):
    for t in tokens:
        if t.type in ('link_open','image'):
            value=t.attrGet('href' if t.type=='link_open' else 'src')
            if value:yield value,'image' if t.type=='image' else 'link'
        if t.type in ('html_inline','html_block'):
            for kind,value in re.findall(r'\b(href|src)=["\']([^"\']+)["\']',t.content):yield value,'image' if kind=='src' else 'link'
        yield from urls(t.children or [])

def main()->None:
    files=sorted(p for p in ROOT.rglob('*.md') if not any(part in SKIP for part in p.relative_to(ROOT).parts))
    parsed={p:parse(p) for p in files};by_anchor={p:anchors(t) for p,t in parsed.items()}
    errors=[];counts={'documents':len(files),'local_links':0,'image_links':0,'local_anchors':0,'external_links_skipped':0}
    for p,tokens in parsed.items():
        for value,kind in urls(tokens):
            u=urlsplit(value)
            if u.scheme in ('http','https','mailto','tel') or u.netloc:
                counts['external_links_skipped']+=1;continue
            if u.scheme or value.startswith('/'):
                errors.append({'file':p.relative_to(ROOT).as_posix(),'url':value,'error':'nonportable absolute/scheme URL'});continue
            q=(p.parent/unquote(u.path)).resolve() if u.path else p
            try:q.relative_to(ROOT)
            except ValueError:
                errors.append({'file':p.relative_to(ROOT).as_posix(),'url':value,'error':'outside repository'});continue
            counts['local_links']+=1
            if kind=='image':counts['image_links']+=1
            if not q.exists():
                errors.append({'file':p.relative_to(ROOT).as_posix(),'url':value,'error':'missing target'});continue
            if q.is_dir() and (q/'README.md').is_file():q=q/'README.md'
            if u.fragment and q.suffix=='.md':
                counts['local_anchors']+=1
                if q not in by_anchor:by_anchor[q]=anchors(parse(q))
                frag=unquote(u.fragment)
                if frag not in by_anchor[q]:errors.append({'file':p.relative_to(ROOT).as_posix(),'url':value,'error':'missing anchor'})
    preserved=json.loads((ROOT/'reports/original-preservation.json').read_text())
    for path,expected in preserved['original_manuscripts'].items():
        p=ROOT/path
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:errors.append({'file':path,'error':'original manuscript was changed'})
    counts['original_manuscripts_verified']=len(preserved['original_manuscripts'])
    result={'scope':'Local Markdown paths, explicit/heading anchors, image targets, original manuscript hashes; external URLs and remote GitHub rendering are not tested.',**counts,'error_count':len(errors),'errors':errors}
    out=ROOT/'reports/markdown-validation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
