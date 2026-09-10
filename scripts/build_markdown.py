#!/usr/bin/env python3
"""Build the complete Markdown manuscript from book.json without network access.

Chapter files remain canonical. Links into included chapters become explicit,
unique anchors; image/code links become repository-root-relative paths.
"""
from __future__ import annotations
import json,os,re,unicodedata
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
OUTPUT='DBT_all_in_one_v3_Madang_Market.md'

def slug(value:str)->str:
    """GitHub-style heading slug for the book's plain-text headings."""
    value=value.lower()
    value=''.join(c for c in value if c in '-_' or c.isspace() or unicodedata.category(c)[0] in 'LN')
    return re.sub(r'\s','-',value)

def key(path:str)->str:
    return 'book-'+re.sub(r'[^a-z0-9]+','-',path.lower()).strip('-')

def plain_heading(value:str)->str:
    from markdown_it import MarkdownIt
    tokens=MarkdownIt().parseInline(value)
    return ''.join(t.content for token in tokens for t in token.children or [] if t.type in ('text','code_inline','html_inline'))

def main()->None:
    book=json.loads((ROOT/'book.json').read_text(encoding='utf-8'))
    groups=book['sections']
    paths=[p for g in groups for p in g['files'] if p!='README.md']
    if len(paths)!=len(set(paths)):raise SystemExit('Duplicate paths in book.json')
    included=set(paths)
    def target(url:str,current:str)->str:
        parsed=urlsplit(url)
        if parsed.scheme or parsed.netloc or url.startswith('//'):return url
        resolved=current if not parsed.path else os.path.normpath(str(Path(current).parent/unquote(parsed.path))).replace('\\','/')
        if resolved in included:
            return '#'+key(resolved)+('--'+unquote(parsed.fragment) if parsed.fragment else '')
        if not parsed.path:return '#'+key(current)+('--'+unquote(parsed.fragment) if parsed.fragment else '')
        return resolved+('?' + parsed.query if parsed.query else '')+('#'+parsed.fragment if parsed.fragment else '')
    out=['# DBT All In One — 통계마당 · 마당마켓 에디션','',
         '> 장별 Markdown에서 자동 생성한 통합 원고다. 수정은 장별 원고에서 한다. 긴 파일의 웹 렌더링이 제한되면 [장별 전체 목차](01_outline/master_toc.md)를 이용한다.','',
         '[저장소 첫 화면](README.md) · [편집과 검증](CONTRIBUTING.md)','',
         '## 통합 목차','']
    for group in groups:
        selected=[p for p in group['files'] if p in included]
        if not selected:continue
        out += ['### '+group['title'],'']
        for p in selected:
            title=(ROOT/p).read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
            out.append(f'- [{title}](#{key(p)})')
        out.append('')
    for path in paths:
        out += ['---','',f'<a id="{key(path)}"></a>','',f'장별 원고: [{path}]({path})','']
        seen={};fence=None
        for line in (ROOT/path).read_text(encoding='utf-8').splitlines():
            mark=re.match(r'^\s*(`{3,}|~{3,})',line)
            if mark:
                m=mark.group(1)
                if fence is None:fence=m
                elif m[0]==fence[0] and len(m)>=len(fence):fence=None
                out.append(line);continue
            if fence:out.append(line);continue
            h=re.match(r'^(#{1,6})\s+(.+?)\s*#*$',line)
            if h:
                ident=slug(plain_heading(h[2]));n=seen.get(ident,0);seen[ident]=n+1
                if n:ident+=f'-{n}'
                out += [f'<a id="{key(path)}--{ident}"></a>','']
                line='#'*min(6,len(h[1])+1)+' '+h[2]
            # Keep image alt text and optional link titles intact.
            line=re.sub(r'(!?\[[^\]\n]*\]\()([^\s)]+)([^)]*\))',lambda m:m[1]+target(m[2],path)+m[3],line)
            line=re.sub(r'((?:src|href)=["\'])([^"\']+)(["\'])',lambda m:m[1]+target(m[2],path)+m[3],line)
            line=re.sub(r'(\bid=["\'])([^"\']+)(["\'])',lambda m:m[1]+key(path)+'--'+m[2]+m[3],line)
            line=re.sub(r'^(\s*\[[^\]]+\]:\s*)(\S+)',lambda m:m[1]+target(m[2],path),line)
            out.append(line)
        out.append('')
    result='\n'.join(out).rstrip()+'\n'
    (ROOT/OUTPUT).write_text(result,encoding='utf-8')
    print(json.dumps({'output':OUTPUT,'included_documents':len(paths),'utf8_bytes':len(result.encode())},ensure_ascii=False))

if __name__=='__main__':main()
