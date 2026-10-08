#!/usr/bin/env python3
import json,os,datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
tw=json.load(open('tools/twins.json'));SITE='https://tyros-group.com'
today=datetime.date.today().isoformat()
skip={'/demande/'}
out=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
def entry(u,fr,en,pri):
    out.append(f'  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>{pri}</priority>'
      f'<xhtml:link rel="alternate" hreflang="fr" href="{SITE}{fr}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{fr}"/></url>')
for fr,en in tw.items():
    if fr in skip: continue
    pri='1.0' if fr=='/' else '0.3' if fr in('/mentions-legales/','/confidentialite/') else '0.8'
    if pri=='1.0': pass
    for u in (fr,en): entry(u,fr,en,pri)
out.append('</urlset>')
open('sitemap.xml','w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(out)-3,'urls')
