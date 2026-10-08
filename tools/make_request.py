#!/usr/bin/env python3
"""Generates the request pages (/demande/ and /en/request/): four journeys, one component."""
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pagegen import shell,write
import forms
def page(lang):
    t=forms.T[lang]
    tabs=''.join('<a href="%s?type=%s" data-tab="%s">%s</a>'%('/demande/' if lang=='fr' else '/en/request/',k,k,l) for k,l in t['tabs'])
    secs=''
    for k in ('general','recruitment','consulting','academy','candidate'):
        secs+=f'<section class="req-sec" data-type="{k}" hidden>{forms.form(lang,k,k)}</section>\n'
    return f'''<div class="page-hero req-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">{t['eyebrow']}</div>
    <h1 id="req-h1">{t['h1']['general']}</h1>
    <p class="lede" id="req-lede">{t['lede']['general']}</p>
  </div>
</div>
<div class="req-wrap">
  <nav class="req-tabs" aria-label="{forms.E(t['switch'])}">{tabs}</nav>
  <p class="req-ctx" id="req-ctx" hidden>{t['ctx']} <strong></strong></p>
  <div class="req-panels">
{secs}  </div>
  {forms.success(lang)}
  <noscript><p class="req-noscript">{t['noscript']}</p></noscript>
</div>
<script type="application/json" id="req-config">{forms.config(lang)}</script>'''
ty=json.load(open('tools/types.json'))
for lang,url,title,desc in (('fr','/demande/','Demande | Tyros Group','Contact, recrutement, conseil, Tyros Academy : adressez votre demande à Tyros Group.'),
                            ('en','/en/request/','Request | Tyros Group','Contact, recruitment, consulting, Tyros Academy: send your request to Tyros Group.')):
    write(url,shell(lang,url,title,desc,page(lang),robots='noindex,follow',jsonld=False));ty[url]='page'
json.dump(ty,open('tools/types.json','w'),indent=1)
print('request pages written')
