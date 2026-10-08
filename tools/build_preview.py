#!/usr/bin/env python3
"""Builds a self-contained, relative-path copy of the site in /tmp/prev for browsing inside an artifact.
Simulated sending only (banner shown). Query-string links become static variant pages."""
import os,re,json,shutil,hashlib,glob
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'));os.chdir(ROOT)
OUT='/tmp/prev';shutil.rmtree(OUT,ignore_errors=True);os.makedirs(OUT)
for d in ('assets','fonts'):
    shutil.copytree(d,OUT+'/'+d,ignore=shutil.ignore_patterns('og'))
for f in glob.glob(OUT+'/assets/**/*.css',recursive=True):
    depth=os.path.relpath(f,OUT).count('/');s=open(f,encoding='utf-8').read()
    open(f,'w',encoding='utf-8').write(s.replace("url('/fonts/","url('"+'../'*depth+"fonts/").replace('url("/fonts/','url("'+'../'*depth+'fonts/'))
MOCK="""<script>window.__ENDPOINT='https://mock.invalid/exec';(function(){var o=window.fetch;window.fetch=function(u,x){if(String(u).indexOf('mock.invalid')>-1){return new Promise(function(r){setTimeout(function(){r({json:function(){return Promise.resolve({ok:true,ref:'TY-APERCU-001'})}})},700)})}return o.apply(this,arguments)}})();</script>"""
BANNER='<div style="position:fixed;left:0;right:0;bottom:0;z-index:999;background:#CEA152;color:#050E1D;font:600 13px/1.4 system-ui,sans-serif;padding:8px 14px;text-align:center">Aperçu : les envois de formulaire sont simulés, rien n\'est transmis.</div>'
pages={}
for r,d,fs in os.walk('.'):
    if r.startswith(('./design-system','./.git','./tools','./assets','./fonts','./node_modules')):continue
    for x in fs:
        if x in('index.html','404.html'):
            f=os.path.join(r,x)[2:];pages[f]=open(f,encoding='utf-8').read()
variants={}
def rel(prefix,url):
    u=url
    if u.startswith('//') or not u.startswith('/'): return None
    path,_,frag=u.partition('#');q=''
    if '?' in path: path,q=path.split('?',1)
    if q.endswith('#'): q=q[:-1]
    path=path.replace('&amp;','&')
    if path.endswith('/') : target=path.lstrip('/')+'index.html'
    else: target=path.lstrip('/')
    if q and not target.endswith('index.html'): q=''
    if q:
        q=q.replace('&amp;','&');h=hashlib.md5(q.encode()).hexdigest()[:8];tdir=os.path.dirname(target)
        vf=(tdir+'/' if tdir else '')+'v_'+h+'.html';variants[vf]=(target,q);target=vf
    return prefix+target+('#'+frag if frag else '')
def convert(f,s,req=None):
    depth=f.count('/');prefix='../'*depth
    s=re.sub(r'(href|src)="(/[^"]*)"',lambda m:m.group(1)+'="'+(rel(prefix,m.group(2)) or m.group(2))+'"',s)
    s=re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->','',s,flags=re.S)
    s=re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->','',s,flags=re.S)
    s=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',s)
    inj=MOCK+(('<script>window.__REQ='+json.dumps(req)+';</script>') if req is not None else '')
    s=s.replace('<script src="'+prefix+'assets/request.js',inj+'<script src="'+prefix+'assets/request.js')
    if 'request.js' in s: s=s.replace('</body>',BANNER+'</body>')
    return s
for f,s in pages.items():
    os.makedirs(os.path.dirname(OUT+'/'+f) or OUT,exist_ok=True);open(OUT+'/'+f,'w',encoding='utf-8').write(convert(f,s))
for vf,(target,q) in variants.items():
    s=pages[target.replace('index.html','index.html')] if target in pages else None
    if s is None: continue
    os.makedirs(os.path.dirname(OUT+'/'+vf) or OUT,exist_ok=True);open(OUT+'/'+vf,'w',encoding='utf-8').write(convert(vf,s,q))
print(len(pages),'pages +',len(variants),'variants')
