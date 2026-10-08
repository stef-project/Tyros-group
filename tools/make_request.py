#!/usr/bin/env python3
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pagegen import shell,write
import forms
def page(lang):
    t=forms.T[lang]
    return f'''<div class="page-hero req-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">{'Contact'}</div>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
  </div>
</div>
<div class="req-wrap">
  <div class="req-panels">{forms.form(lang,'page')}</div>
  {forms.success(lang)}
  <noscript><p class="req-noscript">{t['noscript']}</p></noscript>
</div>
<script type="application/json" id="req-config">{forms.config(lang)}</script>'''
ty=json.load(open('tools/types.json'))
for lang,url,title,desc in (('fr','/demande/','Contact | Tyros Group','Écrire à Tyros Group : un seul formulaire, une réponse personnelle.'),('en','/en/request/','Contact | Tyros Group','Write to Tyros Group: one form, a personal reply.')):
    write(url,shell(lang,url,title,desc,page(lang),robots='noindex,follow',jsonld=False));ty[url]='page'
json.dump(ty,open('tools/types.json','w'),indent=1)
print('contact pages written')
