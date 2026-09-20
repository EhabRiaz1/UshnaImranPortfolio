#!/usr/bin/env python3
"""
Ingest case-study / cover images exported by hand from the Figma UI.

  1. In Figma select a frame  ->  Export  ->  PNG, 2x  ->  Export
  2. Drop the files in  assets/case/_incoming/
  3. python3 tools/ingest.py

Filenames are matched to slugs loosely, so Figma's own names work as-is
("Animal Conservatory.png", "Lark@2x.png", "CIO1.png", ...).
Tall frames are cut into <=2000px WebP strips so the modal lazy-loads.
"""
import json, os, re, sys, shutil
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = '/Users/ehabriaz/Desktop/uWebsite'
INBOX = f'{ROOT}/assets/case/_incoming'
CASE  = f'{ROOT}/assets/case'
IMG   = f'{ROOT}/assets/img'
SLICE_H = 2000
MAX_W   = 2112          # 2x the 1056px modal column

# slug -> the Figma frame names that should land on it
ALIASES = {
    'lark':                ['lark', 'larkcreatives'],
    'quiksnap':            ['quiksnap', 'quicksnap'],
    'zayriba':             ['zayriba'],
    'aaron-rodricks':      ['aaron', 'aaronrodricks', 'aaronrodericks'],
    'frame':               ['frame'],
    'rend-stephan':        ['rend', 'rendstephan'],
    'animal-conservatory': ['animalconservatory', 'animal'],
    'keke':                ['keke'],
    'cio1':                ['cio1', 'cio'],
}
COVERS = {'cover-1': ['cover1', 'cover-1', 'worldrhinoday'],
          'cover-2': ['cover2', 'cover-2', 'cover50'],
          'cover-3': ['cover3', 'cover-3'],
          'cover-4': ['cover4', 'cover-4', 'cover51']}

norm = lambda s: re.sub(r'[^a-z0-9]', '', os.path.splitext(s)[0].lower())

def match(fname, table):
    raw = norm(fname)
    # try the untouched name first: stripping digits would eat "cover50"
    for cand in (raw, re.sub(r'(@?[234]x|copy)$', '', raw),
                      re.sub(r'(@?[234]x|copy|\d{2,})$', '', raw)):
        best = None
        for slug, keys in table.items():
            for k in keys:
                if cand == k: return slug              # exact wins outright
                if cand.startswith(k) or k in cand:
                    if best is None or len(k) > best[1]: best = (slug, len(k))
        if best: return best[0]
    return None

def slice_case(slug, path):
    d = f'{CASE}/{slug}'
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d, exist_ok=True)
    im = Image.open(path).convert('RGB')
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    n = 0
    for top in range(0, im.height, SLICE_H):
        n += 1
        im.crop((0, top, im.width, min(im.height, top + SLICE_H))).save(
            f'{d}/{n:02d}.webp', 'WEBP', quality=84, method=5)
    kb = sum(os.path.getsize(f'{d}/{f}') for f in os.listdir(d)) // 1024
    print(f'  {slug:<22} {im.width}x{im.height} -> {n} slices, {kb}KB')

def manifest():
    m = {}
    for slug in ALIASES:
        d = f'{CASE}/{slug}'
        if os.path.isdir(d):
            fs = sorted(f for f in os.listdir(d) if f.endswith('.webp'))
            if fs: m[slug] = [f'assets/case/{slug}/{f}' for f in fs]
    json.dump(m, open(f'{ROOT}/js/cases.json', 'w'), indent=1)
    print(f'\njs/cases.json -> {len(m)}/{len(ALIASES)} case studies live')
    missing = [s for s in ALIASES if s not in m]
    if missing: print('  still missing: ' + ', '.join(missing))
    return m

if __name__ == '__main__':
    os.makedirs(INBOX, exist_ok=True)
    files = [f for f in sorted(os.listdir(INBOX))
             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if not files:
        print(f'Nothing in {INBOX}\n'
              f'Export frames from Figma as PNG @2x and drop them there.')
        manifest(); sys.exit(0)

    print(f'{len(files)} file(s) in _incoming:')
    unmatched = []
    for f in files:
        p = f'{INBOX}/{f}'
        slug = match(f, ALIASES)
        if slug:
            slice_case(slug, p); continue
        cov = match(f, COVERS)
        if cov:
            im = Image.open(p).convert('RGBA')
            im.save(f'{IMG}/{cov}.webp', 'WEBP', quality=88, method=6)
            print(f'  {cov:<22} cover -> assets/img/{cov}.webp')
            continue
        unmatched.append(f)

    if unmatched:
        print('\n  UNMATCHED (rename to one of the slugs below):')
        for f in unmatched: print(f'    {f}')
        print('    slugs: ' + ', '.join(list(ALIASES) + list(COVERS)))
    manifest()
