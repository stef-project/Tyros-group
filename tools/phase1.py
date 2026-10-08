#!/usr/bin/env python3
"""One-shot structural normalisation (run once on the pre-refactor tree).
Externalises the inline CSS per page type, replaces header/footer/legal/scripts by marker regions
that tools/sync.py fills, removes the dynamic translation layer and the decorative canvases."""
import re,os,json,hashlib,sys
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
os.chdir(ROOT)
inv=json.load(open('/tmp/inv.json'))
SKIP_STUB=lambda s:'<h1' not in s
types={}  # url -> type
css_out={}
def page_type(u,s):
    if u=='/': return 'home'
    if u in('/for-boards-executives/','/en/for-boards-executives/'): return 'boards'
    if '/insights/' in u: return 'article'
    return 'page'
parts_saved=False
for u,i in sorted(inv.items()):
    f=i['file'];s=open(f,encoding='utf-8').read()
    if SKIP_STUB(s) or u=='/404.html': continue
    t=page_type(u,s);types[u]=t
    # 1 css
    blocks=re.findall(r'<style>(.*?)</style>',s,re.S);css='\n'.join(b.strip('\n') for b in blocks)
    if t in css_out: assert css_out[t][0]==hashlib.md5(css.encode()).hexdigest(),(u,t,'css differs within type')
    else: css_out[t]=(hashlib.md5(css.encode()).hexdigest(),css)
    s=re.sub(r'<style>.*?</style>\s*','',s,flags=re.S)
    s=re.sub(r'<link rel="stylesheet" href="/assets/tyros-(?:ds|bplus)\.css[^"]*">\s*','',s)
    s=s.replace('</head>','<!--@css--><!--@/css-->\n</head>',1)
    # 2 save reusable svg parts once (from FR home)
    if u=='/' and not parts_saved:
        hd=re.search(r'<header class="site".*?</header>',s,re.S).group(0)
        svgs=re.findall(r'<svg.*?</svg>',hd,re.S)
        json.dump({'logo':svgs[0],'theme':svgs[1]+svgs[2],'toggle':svgs[3]},open('tools/parts.json','w'),ensure_ascii=False,indent=1)
        parts_saved=True
    # 3 top chrome: skip link .. before <main
    a=s.index('<a class="skip"');b=s.index('<main id="main">')
    s=s[:a]+'<!--@top--><!--@/top-->\n\n'+s[b:]
    # 4 bottom chrome: footer .. before first body <script>
    a=s.index('<footer class="site">');b=s.index('<script>',a)
    s=s[:a]+'<!--@bottom--><!--@/bottom-->\n'+s[b:]
    # 5 scripts: drop inline non-LD scripts after footer region
    head,body=s.split('<!--@bottom--><!--@/bottom-->',1)
    body=re.sub(r'<script>.*?</script>\s*','',body,flags=re.S)
    body=body.replace('</body>','<!--@scripts--><!--@/scripts-->\n</body>',1)
    s=head+'<!--@bottom--><!--@/bottom-->'+body
    # 6 decorative canvases
    s=re.sub(r'<div class="hero-bg"[^>]*><canvas id="hero-canvas"></canvas></div>\s*','',s)
    s=re.sub(r'<canvas class="ins-canvas"></canvas>','',s)
    open(f,'w',encoding='utf-8').write(s)
os.makedirs('assets/css',exist_ok=True)
for t,(h,css) in css_out.items(): open('assets/css/%s.css'%t,'w',encoding='utf-8').write(css+'\n')
json.dump(types,open('tools/types.json','w'),indent=1)
print({t:len(c[1]) for t,c in css_out.items()},len(types),'pages')
