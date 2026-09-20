#!/usr/bin/env python3
"""
Fill the case-study modals with UNMISTAKABLY-MARKED placeholder content so the
interaction can be tested before the real Figma exports arrive.

  python3 tools/demo.py           # install placeholders
  python3 tools/demo.py --clear   # remove them, back to {}

Every slice is stamped, so this can never be mistaken for finished work.
"""
import json, os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

ROOT = '/Users/ehabriaz/Desktop/uWebsite'
CASE = f'{ROOT}/assets/case'
SLUGS = {
    'lark': 'Lark Creatives', 'quiksnap': 'QuikSnap', 'zayriba': 'Zayriba',
    'aaron-rodricks': 'Aaron Rodricks', 'frame': 'Frame',
    'rend-stephan': 'Rend Stephan', 'animal-conservatory': 'Animal Conservatory',
    'keke': 'KEKE', 'cio1': 'CIO1',
}
W, H, SLICES = 2112, 1800, 3

def font(sz):
    for p in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf',
              '/System/Library/Fonts/Helvetica.ttc'):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except OSError: pass
    return ImageFont.load_default()

def clear():
    n = 0
    for slug in SLUGS:
        d = f'{CASE}/{slug}'
        if os.path.isdir(d): shutil.rmtree(d); n += 1
    json.dump({}, open(f'{ROOT}/js/cases.json', 'w'), indent=1)
    print(f'removed {n} placeholder case studies; js/cases.json -> {{}}')

def build():
    man = {}
    for slug, label in SLUGS.items():
        d = f'{CASE}/{slug}'
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d, exist_ok=True)
        for i in range(1, SLICES + 1):
            im = Image.new('RGB', (W, H), '#EDEDED')
            dr = ImageDraw.Draw(im)
            dr.rectangle([0, 0, W, 150], fill='#FF661C')
            dr.text((60, 48), 'PLACEHOLDER — NOT THE REAL CASE STUDY',
                    font=font(58), fill='white')
            dr.text((60, 320), label.upper(), font=font(150), fill='#111')
            dr.text((60, 520), f'slice {i} of {SLICES}', font=font(64), fill='#666')
            dr.text((60, 640), 'Export this frame from Figma at 2x into',
                    font=font(52), fill='#555')
            dr.text((60, 720), 'assets/case/_incoming/  then run tools/ingest.py',
                    font=font(52), fill='#555')
            for y in range(900, H, 190):                     # faint repeating stamp
                dr.text((60, y), 'PLACEHOLDER  ' * 6, font=font(54), fill='#DCDCDC')
            im.save(f'{d}/{i:02d}.webp', 'WEBP', quality=80, method=4)
        man[slug] = [f'assets/case/{slug}/{i:02d}.webp' for i in range(1, SLICES + 1)]
        print(f'  {slug:<22} {SLICES} placeholder slices')
    json.dump(man, open(f'{ROOT}/js/cases.json', 'w'), indent=1)
    print(f'\njs/cases.json -> {len(man)} case studies (ALL PLACEHOLDER)')
    print('remove with:  python3 tools/demo.py --clear')

if __name__ == '__main__':
    clear() if '--clear' in sys.argv else build()
