import json, collections
D = json.load(open('/Users/ehabriaz/Desktop/uWebsite/tools/figma-file.json'))
page = D['document']['children'][0]

def find(n, tid):
    if n['id'] == tid: return n
    for c in n.get('children', []) or []:
        r = find(c, tid)
        if r: return r

HOME = find(page, '2:28014')
HB = HOME['absoluteBoundingBox']; OX, OY = HB['x'], HB['y']

def rel(n):
    b = n['absoluteBoundingBox']
    return dict(x=round(b['x']-OX,1), y=round(b['y']-OY,1), w=round(b['width'],1), h=round(b['height'],1))

# direct children of homepage, sorted by y
kids = [c for c in HOME['children'] if c.get('absoluteBoundingBox')]
print("== HOMEPAGE DIRECT CHILDREN (id, name, rect) ==")
for c in sorted(kids, key=lambda c: c['absoluteBoundingBox']['y']):
    r = rel(c)
    lbl = c['name'][:38]
    if c['type'] == 'TEXT': lbl += ' | ' + c.get('characters','').strip().replace('\n',' ')[:26]
    print(f"  {c['id']:<10} [{c['type'][:6]:<6}] y={r['y']:>6.0f} x={r['x']:>5.0f} {r['w']:>6.0f}x{r['h']:<6.0f} {lbl}")
