#!/usr/bin/env python3
"""Static audit: language integrity, link integrity, leftovers."""
import os,re,json,sys,urllib.parse
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
tw=json.load(open('tools/twins.json'));rev={v:k for k,v in tw.items()}
pages={}
for r,d,fs in os.walk('.'):
    if r.startswith(('./design-system','./.git','./tools','./assets','./fonts','./node_modules')): continue
    for x in fs:
        if x.endswith('.html'):
            f=os.path.join(r,x)[2:];u='/'+re.sub(r'index\.html$','',f);pages[u]=open(f,encoding='utf-8').read()
problems=[];stubs=[u for u,s in pages.items() if '<h1' not in s]
content={u:s for u,s in pages.items() if u not in stubs}
def exists(path):
    if path in pages: return True
    return os.path.exists(path.lstrip('/'))
ids={u:set(re.findall(r'\sid="([^"]+)"',s)) for u,s in pages.items()}
for u,s in content.items():
    lang=re.search(r'<html[^>]*lang="(\w+)"',s).group(1)
    exp='en' if u.startswith('/en/') else 'fr'
    if lang!=exp and u!='/404.html': problems.append((u,'html lang',lang))
    if 'data-en' in s: problems.append((u,'data-en left'))
    if 'theme-btn' in s or 'data-theme' in s.replace('data-theme-',''): problems.append((u,'theme switch left'))
    if 'Read in English' in s or 'Lire en français' in s: problems.append((u,'language shortcut left'))
    if 'tyros_lang' in s: problems.append((u,'lang storage left'))
    can=re.search(r'rel="canonical" href="https://tyros-group.com([^"]*)"',s)
    if not can or can.group(1)!=u: problems.append((u,'canonical',can and can.group(1)))
    # reciprocal hreflang
    alts=dict(re.findall(r'rel="alternate" hreflang="([\w-]+)" href="https://tyros-group.com([^"]*)"',s))
    twin=tw.get(u) or rev.get(u)
    if twin and u!='/404.html':
        if alts.get('fr')!=(u if exp=='fr' else twin) or alts.get('en')!=(twin if exp=='fr' else u): problems.append((u,'hreflang',alts))
        if twin not in pages: problems.append((u,'twin missing',twin))
    elif u not in('/404.html',) and not twin: problems.append((u,'no twin'))
    # lang switch links
    for l,href in re.findall(r'<a href="([^"]*)" lang="(?:fr|en)" hreflang="(fr|en)"',s):pass
    # links
    s_nolang=re.sub(r'<a [^>]*hreflang="[^"]*"[^>]*>','',s)
    for h in re.findall(r'href="([^"#?][^"]*|#[^"]*|[^"]*#[^"]*)"',s_nolang):
        if h.startswith(('http','mailto:','tel:','data:')): 
            if h.startswith('mailto:') and u not in('/','/en/','/confidentialite/','/en/privacy-policy/'): problems.append((u,'mailto',h[:60]))
            continue
        h=h.replace('&amp;','&');pth,_,frag=h.partition('#');pth=urllib.parse.urlsplit(pth).path
        if not pth: pth=u
        if exp=='en' and pth.startswith('/') and not pth.startswith(('/en/','/assets','/fonts')) and pth!='/404.html': problems.append((u,'EN page links to FR page',h))
        if pth.startswith('/') and not exists(pth): problems.append((u,'broken link',h)); continue
        if frag and pth in ids and frag not in ids[pth]: problems.append((u,'broken anchor',h))
    # assets
    for a in re.findall(r'(?:href|src)="(/assets/[^"?]+|/fonts/[^"?]+)',s):
        if not os.path.exists(a.lstrip('/')): problems.append((u,'missing asset',a))
print('pages',len(pages),'content',len(content),'stubs',len(stubs))
for p in problems: print(' ',*p)
print('PROBLEMS:',len(problems))
