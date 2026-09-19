#!/usr/bin/env python3
"""Pull every homepage asset out of Figma as rendered PNGs, then slice grids locally."""
import json, os, sys, time, urllib.request, urllib.parse

ROOT = '/Users/ehabriaz/Desktop/uWebsite'
KEY  = 'qNIx6bYZZ9ewdWayAdL57P'
TOK  = open(f'{ROOT}/.figtok').read().strip()
IMG  = f'{ROOT}/assets/img'
os.makedirs(IMG, exist_ok=True)

D = json.load(open(f'{ROOT}/tools/figma-file.json'))
page = D['document']['children'][0]

def find(n, t):
    if n['id'] == t: return n
    for c in n.get('children', []) or []:
        r = find(c, t)
        if r: return r

def api(path):
    req = urllib.request.Request(f'https://api.figma.com/v1/{path}',
                                 headers={'X-Figma-Token': TOK})
    return json.load(urllib.request.urlopen(req, timeout=300))

def render(ids, scale):
    """ids -> {id: url}; batched, retried."""
    out = {}
    B = 3
    for i in range(0, len(ids), B):
        chunk = ids[i:i+B]
        q = urllib.parse.quote(','.join(chunk))
        for attempt in range(6):
            try:
                r = api(f'images/{KEY}?ids={q}&format=png&scale={scale}')
                if r.get('err'): raise RuntimeError(r['err'])
                out.update({k: v for k, v in r['images'].items() if v})
                print(f'   rendered {i+len(chunk)}/{len(ids)} @{scale}x', flush=True)
                break
            except Exception as e:
                print(f'   retry {attempt+1} ({e})', flush=True)
                time.sleep(20 * (attempt + 1))
        else:
            print(f'   FAILED chunk {chunk}', flush=True)
    return out

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0: return 'cached'
    urllib.request.urlretrieve(url, dest)
    return f'{os.path.getsize(dest)//1024}KB'

# ---- single-node assets: (node id, filename, scale) -------------------------
SINGLES = [
    ('2:28036', 'hero-illustration', 3),
    ('2:28045', 'hero-rose',         4),
    ('2:28029', 'break-1',           2),
    ('2:28060', 'break-2',           2),
    ('2:28075', 'brand-lark',        3),
    ('2:28016', 'brand-quiksnap',    3),
    ('2:29486', 'brand-zayriba',     3),
    ('2:29438', 'anim-aliph',        2),
    ('2:29469', 'anim-reimagined-a', 3),
    ('2:29474', 'anim-reimagined-b', 3),
    ('2:29447', 'anim-bashir',       3),
    ('2:29480', 'anim-magnetic-a',   3),
    ('2:29483', 'anim-magnetic-b',   3),
    ('2:29424', 'cover-1',           4),
    ('2:29322', 'cover-2',           4),
    ('2:29431', 'cover-3',           4),
    ('2:29362', 'cover-4',           4),
    ('2:29539', 'grid-uiux',         2),   # sliced below
    ('2:28096', 'grid-social',       2),   # sliced below
]

if __name__ == '__main__':
    todo = [(i, n, s) for i, n, s in SINGLES
            if not os.path.exists(f'{IMG}/{n}.png')]
    if not todo:
        print('all renders cached')
        sys.exit(0)
    by_scale = {}
    for i, n, s in todo: by_scale.setdefault(s, []).append((i, n))
    for scale, items in sorted(by_scale.items()):
        print(f'-- rendering {len(items)} nodes @{scale}x')
        urls = render([i for i, _ in items], scale)
        for nid, name in items:
            u = urls.get(nid)
            if not u:
                print(f'   !! no url for {name} ({nid})'); continue
            print(f'   {name:<22} {download(u, f"{IMG}/{name}.png")}', flush=True)
