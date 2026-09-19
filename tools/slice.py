#!/usr/bin/env python3
"""Slice the rendered UI/UX and social grids into per-tile images using Figma coords."""
import json, os
from PIL import Image

ROOT='/Users/ehabriaz/Desktop/uWebsite'; IMG=f'{ROOT}/assets/img'
D=json.load(open(f'{ROOT}/tools/figma-file.json')); page=D['document']['children'][0]
def find(n,t):
    if n['id']==t: return n
    for c in n.get('children',[]) or []:
        r=find(c,t)
        if r: return r

# ---------- UI/UX : 3x3, art 347x238, cols 3/356/710, rows 0/332/664 --------
UIUX=[['squint-cognition','aaron-rodricks','frame'],
      ['rend-stephan','atoofy','animal-conservatory'],
      ['syncquik','keke','cio1']]
def slice_uiux():
    src=Image.open(f'{ROOT}/tools/renders/grid-uiux.png').convert('RGBA')
    node=find(page,'2:29539'); nb=node['absoluteBoundingBox']
    S=src.width/nb['width']
    cols=[3,356,710]; rows=[0,332,664]; W,H=347,238
    for ri,y in enumerate(rows):
        for ci,x in enumerate(cols):
            box=(round(x*S),round(y*S),round((x+W)*S),round((y+H)*S))
            src.crop(box).save(f'{IMG}/uiux-{UIUX[ri][ci]}.webp', 'WEBP', quality=84, method=6)
            print(f'  uiux-{UIUX[ri][ci]:<22} {box[2]-box[0]}x{box[3]-box[1]}')

# ---------- Social : derive every tile rect from the JSON -------------------
def slice_social():
    src=Image.open(f'{ROOT}/tools/renders/grid-social.png').convert('RGBA')
    node=find(page,'2:28096'); nb=node['absoluteBoundingBox']
    S=src.width/nb['width']; ox,oy=nb['x'],nb['y']
    tiles=[]
    for c in node['children']:
        b=c.get('absoluteBoundingBox')
        if not b or b['width']<300 or b['height']<300: continue
        tiles.append((round(b['y']-oy), round(b['x']-ox), round(b['width']), round(b['height'])))
    tiles.sort()
    print(f'  social tiles found: {len(tiles)}')
    man=[]
    for i,(y,x,w,h) in enumerate(tiles,1):
        box=(max(0,round(x*S)),max(0,round(y*S)),
             min(src.width,round((x+w)*S)),min(src.height,round((y+h)*S)))
        name=f'social-{i:02d}'
        src.crop(box).save(f'{IMG}/{name}.webp','WEBP',quality=84,method=6)
        man.append(dict(n=name,x=x,y=y,w=w,h=h))
    json.dump(man,open(f'{ROOT}/tools/social-tiles.json','w'),indent=1)
    print(f'  wrote {len(man)} social tiles; grid {nb["width"]:.0f}x{nb["height"]:.0f}')
    return man

if __name__=='__main__':
    if os.path.exists(f'{ROOT}/tools/renders/grid-uiux.png'):   print('UI/UX:');  slice_uiux()
    if os.path.exists(f'{ROOT}/tools/renders/grid-social.png'): print('SOCIAL:'); slice_social()
