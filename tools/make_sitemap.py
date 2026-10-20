#!/usr/bin/env python3
"""Writes sitemap.xml. lastmod = date of the last SIGNIFICANT change of each URL: the last commit where the page's own content
(title, description, <main> markup) changed. Header/footer/stylesheet-version changes do not count. Uncommitted content changes count as today."""
import json,os,re,subprocess,datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
tw=json.load(open('tools/twins.json'));SITE='https://tyros-group.com'
today=datetime.date.today().isoformat()
skip={'/demande/'}
def path_of(u): return 'index.html' if u=='/' else u.strip('/')+'/index.html'
def norm(html):
    t=re.search(r'<title>(.*?)</title>',html,re.S);d=re.search(r'<meta name="description" content="([^"]*)"',html)
    m=re.search(r'<main[^>]*>(.*?)</main>',html,re.S)
    return re.sub(r'\s+',' ',((t.group(1) if t else '')+'|'+(d.group(1) if d else '')+'|'+(m.group(1) if m else html)))
def git(*a):
    r=subprocess.run(['git']+list(a),capture_output=True,text=True);return r.stdout if r.returncode==0 else None
if (git('rev-parse','--is-shallow-repository') or '').strip()=='true':
    raise SystemExit('shallow clone: git history is incomplete, so lastmod dates would be wrong. Fetch full history first (git fetch --unshallow). sitemap.xml left unchanged.')
cache={}
def lastmod(u):
    p=path_of(u)
    if p in cache: return cache[p]
    cur=norm(open(p,encoding='utf-8').read())
    log=[l.split(' ') for l in (git('log','--format=%H %cs','--',p) or '').strip().split('\n') if l]
    if not log: cache[p]=today;return today
    head=git('show','%s:%s'%(log[0][0],p))
    if head is None or norm(head)!=cur: cache[p]=today;return today
    date=log[0][1]
    for i,(h,d) in enumerate(log):
        older=git('show','%s:%s'%(log[i+1][0],p)) if i+1<len(log) else None
        if older is None or norm(older)!=cur:
            date=d;break
    cache[p]=date;return date
out=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
def entry(u,fr,en,pri):
    out.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{lastmod(u)}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority>'
      f'<xhtml:link rel="alternate" hreflang="fr" href="{SITE}{fr}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{fr}"/></url>')
for fr,en in tw.items():
    if fr in skip: continue
    pri='1.0' if fr=='/' else '0.3' if fr in('/mentions-legales/','/confidentialite/') else '0.8'
    for u in (fr,en): entry(u,fr,en,pri)
out.append('</urlset>')
open('sitemap.xml','w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(out)-3,'urls')
