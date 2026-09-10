#!/usr/bin/env python3
"""Restore only the reviewed book source from a hash-checked local payload.

The importer runs solely on an isolated publication branch. It does not modify
main, download a manuscript, evaluate payload code, or copy credentials.
"""
from __future__ import annotations
import argparse,hashlib,json,lzma,subprocess
from pathlib import Path,PurePosixPath

BASE='15ce73ed7fc7099176f6f9ad56617d269c2e9299'
TREE='90a1e124c56ff0125f02fc677f5961fda7470a4d'
PACK=Path(__file__).resolve().parent

def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def run(*args:str)->bytes:return subprocess.check_output(['git',*args])

def safe(path:str)->PurePosixPath:
    p=PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or '\\' in path or not p.parts or p.parts[0] in {'.git','.github','.publication-payload'}:
        raise ValueError(f'Unsafe publication path: {path}')
    return p

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--root',required=True);args=parser.parse_args()
    manifest=json.loads((PACK/'manifest.json').read_text())
    if manifest['base_commit']!=BASE or manifest['base_tree']!=TREE:raise ValueError('Unexpected publication baseline')
    if run('rev-parse',f'{BASE}^{{tree}}').decode().strip()!=TREE:raise ValueError('Original tree mismatch')
    parts=[]
    for item in manifest['chunks']:
        name=safe(item['name']);part=(PACK/name).read_bytes()
        if item.get('byte_corrections'):
            # Repair a known, checksum-identified transcription error in transport.
            # Both the stored bytes and the fully repaired payload are verified.
            if digest(part)!=item['transport_sha256']:raise ValueError('Transport checksum mismatch')
            fixed=bytearray(part)
            for offset,before,after in item['byte_corrections']:
                if fixed[offset]!=before:raise ValueError('Unexpected correction byte')
                fixed[offset]=after
            part=bytes(fixed)
        if len(part)!=item['bytes'] or digest(part)!=item['sha256']:raise ValueError(f'Corrupt payload part: {name}')
        parts.append(part)
    packed=b''.join(parts)
    if digest(packed)!=manifest['payload_sha256']:raise ValueError('Payload checksum mismatch')
    raw=lzma.decompress(packed)
    if digest(raw)!=manifest['json_sha256']:raise ValueError('JSON checksum mismatch')
    payload=json.loads(raw)
    if payload['base_commit']!=BASE or payload['base_tree']!=TREE:raise ValueError('Inner baseline mismatch')
    if len(payload['entries'])!=manifest['files']:raise ValueError('File count mismatch')
    target=Path(args.root).resolve()
    if target.exists():raise ValueError('Target must be a new worktree')
    subprocess.run(['git','worktree','add','--detach',str(target),BASE],check=True)
    paths=set()
    for entry in payload['entries']:
        relative=safe(entry['p'])
        if str(relative) in paths:raise ValueError('Duplicate target path')
        paths.add(str(relative))
        if 't' in entry:data=entry['t'].encode('utf-8')
        else:
            source=safe(entry['s']);old=run('show',f'{BASE}:{source}')
            if digest(old)!=entry['b']:raise ValueError(f'Changed source baseline: {source}')
            lines=old.decode('utf-8').splitlines(keepends=True)
            for start,end,replacement in reversed(entry['o']):
                if not (0<=start<=end<=len(lines)):raise ValueError('Invalid source edit range')
                lines[start:end]=replacement.splitlines(keepends=True)
            data=''.join(lines).encode('utf-8')
        out=target/relative;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
    # The ZIP is a reproducible local reference for the existing validator, not
    # another committed binary deliverable. Original manuscripts remain intact.
    archive=target/'archive';archive.mkdir(exist_ok=True)
    subprocess.run(['git','archive','--format=zip','--prefix=DBT_all_in_one-main/',f'--output={archive / "original-upload.zip"}',BASE],check=True)
    # The link checker references its own report. Seed it before the first run;
    # successful validation immediately replaces this pending value.
    (target/'reports/markdown-validation.json').write_text('{"status":"pending"}\n')
    print(json.dumps({'restored_source_files':len(paths),'base_commit':BASE,'target':str(target)}))

if __name__=='__main__':main()
