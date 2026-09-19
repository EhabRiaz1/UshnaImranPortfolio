#!/usr/bin/env python3
"""
Render each case-study frame from Figma and slice it into lazy-loadable strips.
Writes assets/case/<slug>/NN.webp + js/cases.json (slug -> [paths]).

Run:  python3 tools/cases.py            # all pending
      python3 tools/cases.py lark       # one slug
Safe to re-run: existing slugs are skipped.
"""
import json, os, sys, time, urllib.request, urllib.parse
from PIL import Image

ROOT='/Users/ehabriaz/Desktop/uWebsite'
KEY='qNIx6bYZZ9ewdWayAdL57P'
TOK=open(f'{ROOT}/.figtok').read().strip()
OUT=f'{ROOT}/assets/case'
SLICE_H=2000          # px per strip in rendered pixels
SCALE=2               # 1050pt frame -> 2100px, crisp at the 1056px modal

# tile slug -> Figma node id
CASES={
 'lark':                '2:47',
 'quiksnap':            '2:17319',
 'zayriba':             '2:27801',
 'aaron-rodricks':      '2:4673',
 'frame':               '2:15474',
 'rend-stephan':        '2:16869',
 'animal-conservatory': '2:5259',
 'keke':                '2:5124',
 'cio1':                '2:5362',
}

def api(path):
    r=urllib.request.Request(f'https://api.figma.com/v1/{path}',headers={'X-Figma-Token':TOK})
    return json.load(urllib.request.urlopen(r,timeout=600))

def render(node, scale):
    q=urllib.parse.quote(node)
    for attempt in range(5):
        try:
            r=api(f'images/{KEY}?ids={q}&format=png&scale={scale}')
            if r.get('err'): raise RuntimeError(r['err'])
            u=r['images'].get(node)
            if u: return u
            raise RuntimeError('null url')
        except urllib.error.HTTPError as e:
            if e.code==429:
                ra=e.headers.get('retry-after','?')
                print(f'   RATE LIMITED (retry-after={ra}s) — aborting', flush=True)
                raise SystemExit(2)
            print(f'   retry {attempt+1}: {e}', flush=True); time.sleep(10*(attempt+1))
        except Exception as e:
            print(f'   retry {attempt+1}: {e}', flush=True); time.sleep(10*(attempt+1))
    return None

def do(slug, node):
    d=f'{OUT}/{slug}'
    if os.path.isdir(d) and os.listdir(d):
        print(f'{slug}: cached'); return
    print(f'{slug}: rendering {node} @{SCALE}x', flush=True)
    u=render(node,SCALE)
    if not u: print(f'{slug}: FAILED'); return
    os.makedirs(d,exist_ok=True)
    tmp=f'{d}/_full.png'
    urllib.request.urlretrieve(u,tmp)
    im=Image.open(tmp).convert('RGB')
    w,h=im.size; n=0
    for top in range(0,h,SLICE_H):
        n+=1
        im.crop((0,top,w,min(h,top+SLICE_H))).save(f'{d}/{n:02d}.webp','WEBP',quality=82,method=5)
    os.remove(tmp)
    print(f'{slug}: {w}x{h} -> {n} slices, {sum(os.path.getsize(f"{d}/{f}") for f in os.listdir(d))//1024}KB')

def manifest():
    m={}
    for slug in CASES:
        d=f'{OUT}/{slug}'
        if os.path.isdir(d):
            fs=sorted(f for f in os.listdir(d) if f.endswith('.webp'))
            if fs: m[slug]=[f'assets/case/{slug}/{f}' for f in fs]
    json.dump(m,open(f'{ROOT}/js/cases.json','w'),indent=1)
    print(f'js/cases.json: {len(m)}/{len(CASES)} case studies ready')

if __name__=='__main__':
    want=sys.argv[1:] or list(CASES)
    for slug in want:
        if slug not in CASES: print(f'unknown slug {slug}'); continue
        do(slug,CASES[slug])
        time.sleep(2)
    manifest()
