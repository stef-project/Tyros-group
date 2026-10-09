#!/usr/bin/env python3
"""Fills the shared regions of every page from one template, per language.

Regions (written between marker comments, idempotent):
  <!--@css-->      theme bootstrap + stylesheet links (by page type)
  <!--@hreflang--> alternate links (from tools/twins.json)
  <!--@top-->      skip link, header, mobile menu
  <!--@bottom-->   footer
  <!--@scripts-->  shared script(s)

Language model: one URL per language. FR pages live at their FR URL, EN pages at their /en/ twin.
The FR/EN selector is a plain link to the twin page. There is no client-side translation.
"""
import os,re,json,hashlib,sys
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
os.chdir(ROOT)
parts=json.load(open('tools/parts.json'))
twins=json.load(open('tools/twins.json'))            # fr url -> en url
rev={v:k for k,v in twins.items()}
types=json.load(open('tools/types.json'))
SITE='https://tyros-group.com'

def ver():
    h=hashlib.md5()
    for f in sorted(os.listdir('assets/css'))+['tyros-ds.css','tyros-bplus.css','tyros-theme.css','tyros-inner.css','tyros-forms.css','site.js','request.js']:
        p=f if '/' in f else ('assets/css/'+f if f.endswith('.css') and f in os.listdir('assets/css') else 'assets/'+f)
        if os.path.exists(p): h.update(open(p,'rb').read())
    return h.hexdigest()[:8]
V=ver()

L={
 'fr':dict(skip='Aller au contenu',lang_label='Langue',theme='Changer le thème',menu='Menu',home='/',pre='',
   nav=[('À propos','#about'),('Divisions','#services'),('Industries','#industries'),('Dirigeants','/for-boards-executives/'),('Insights','#insights'),('Academy','#academy')],
   cta='Échange confidentiel',cta_m='Réserver un échange confidentiel',
   tag='Partenaire stratégique en leadership et intelligence pour les institutions financières. London.',
   f_div='Divisions',f_firm='Cabinet',f_legal='Légal',f_about='À propos',f_boards='Conseils &amp; dirigeants',f_contact='Contact',
   f_notice='Mentions légales',f_privacy='Confidentialité',f_reg='Société enregistrée en Angleterre &amp; Pays de Galles',
   cookies='Gérer les cookies',advisory='/ai-act-gouvernance-ia-finance/',notice='/mentions-legales/',privacy='/confidentialite/',request='/demande/'),
 'en':dict(skip='Skip to content',lang_label='Language',theme='Switch theme',menu='Menu',home='/en/',pre='/en',
   nav=[('About','#about'),('Services','#services'),('Industries','#industries'),('Boards','/for-boards-executives/'),('Insights','#insights'),('Academy','#academy')],
   cta='Book a Discussion',cta_m='Book a Confidential Discussion',
   tag='A strategic leadership &amp; intelligence partner for financial institutions. London.',
   f_div='Divisions',f_firm='Firm',f_legal='Legal',f_about='About',f_boards='Boards &amp; Executives',f_contact='Contact',
   f_notice='Legal notice',f_privacy='Privacy policy',f_reg='Company registered in England &amp; Wales',
   cookies='Cookie settings',advisory='/en/ai-act-ai-governance-financial-services/',notice='/en/legal-notice/',privacy='/en/privacy-policy/',request='/en/request/'),
}

def href(lang,h):
    """nav link target: '#x' -> home anchor of the language; '/p/' -> language page"""
    c=L[lang]
    if h.startswith('#'): return c['home']+h
    return c['pre']+h

def req(lang,type_='general',offer=None,intent=None,src=None):
    q=['type='+type_]
    if offer: q.append('offer='+offer)
    if intent: q.append('intent='+intent)
    if src and src not in('/','/en/'): q.append('from='+src)
    return L[lang]['request']+'?'+'&amp;'.join(q)

def header(lang,url):
    c=L[lang];twin=twins.get(url) if lang=='fr' else rev.get(url)
    fr_url=url if lang=='fr' else twin; en_url=twin if lang=='fr' else url
    nav=''.join('<a href="%s">%s</a>'%(href(lang,h),t) for t,h in c['nav'])
    lang_html=''
    if twin:
        on=lambda l:' class="on" aria-current="true"' if l==lang else ''
        lang_html=('<div class="lang" role="group" aria-label="%s"><a href="%s" lang="fr" hreflang="fr"%s>FR</a><span aria-hidden="true">·</span><a href="%s" lang="en" hreflang="en"%s>EN</a></div>'
                   %(c['lang_label'],fr_url,on('fr'),en_url,on('en')))
    cta=req(lang,'general',src=url)
    return f'''<a class="skip" href="#main">{c['skip']}</a>
<header class="site">
  <div class="hd">
    <a href="{c['home']}" class="logo" aria-label="Tyros Group">
      <span class="logo-top">TYR{parts['logo']}S</span>
      <span class="logo-sub">GROUP</span>
    </a>
    <nav class="main" aria-label="{'Navigation principale' if lang=='fr' else 'Main navigation'}">
      {nav}
    </nav>
    <div class="hd-tools">
      {lang_html}
      <a href="{cta}" class="btn btn-primary hd-cta">{c['cta']}</a>
      <button class="nav-toggle icon-btn" id="nav-toggle" type="button" aria-label="{c['menu']}" aria-expanded="false" aria-controls="mobile-nav">
        {parts['toggle']}
      </button>
    </div>
  </div>
</header>
<div class="mobile-nav" id="mobile-nav" hidden>
  {nav}
  {lang_html.replace('class="lang"','class="lang lang-m"') if lang_html else ''}
  <a href="{cta}" class="btn btn-primary">{c['cta_m']}</a>
</div>
'''

def footer(lang,url):
    c=L[lang];h=c['home']
    return f'''<footer class="site">
  <div class="wrap foot-grid">
    <div>
      <span class="logo" aria-label="Tyros Group"><span class="logo-top">TYR{parts['logo']}S</span><span class="logo-sub">GROUP</span></span>
      <p class="bl">{c['tag']}</p>
    </div>
    <div class="foot-col"><h3>{c['f_div']}</h3><a href="{h}#executive-search">Executive Search</a><a href="{h}#intelligence">Tyros Intelligence</a><a href="{c['advisory']}">Advisory</a><a href="{c['pre']}/tyros-private/">Tyros Private</a></div>
    <div class="foot-col"><h3>{c['f_firm']}</h3><a href="{h}#about">{c['f_about']}</a><a href="{c['pre']}/for-boards-executives/">{c['f_boards']}</a><a href="{h}#insights">Insights</a><a href="{req(lang,'general',src=url)}">{c['f_contact']}</a></div>
    <div class="foot-col"><h3>{c['f_legal']}</h3><a href="{c['notice']}">{c['f_notice']}</a><a href="{c['privacy']}">{c['f_privacy']}</a><a href="https://www.linkedin.com/company/119114061/" rel="noopener">LinkedIn</a><button type="button" class="linklike" id="cookie-settings">{c['cookies']}</button></div>
  </div>
  <div class="foot-bottom">
    <span>© 2026 Tyros Group Ltd, London</span>
    <span>{c['f_reg']}</span>
  </div>
</footer>
'''

THEME_BOOT="""<script>try{var t=localStorage.getItem('tyros_theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','light')}</script>"""

def css(typ,url):
    links=['/assets/css/%s.css'%typ,'/assets/tyros-ds.css','/assets/tyros-bplus.css','/assets/tyros-theme.css']
    if typ!='home': links.append('/assets/tyros-inner.css')
    links.append('/assets/tyros-forms.css')
    return '\n'.join('<link rel="stylesheet" href="%s?v=%s">'%(l,V) for l in links)

def hreflang(url,lang):
    fr=url if lang=='fr' else rev.get(url);en=twins.get(url) if lang=='fr' else url
    if not(fr and en): return ''
    return '\n'.join(['<link rel="alternate" hreflang="fr" href="%s%s">'%(SITE,fr),'<link rel="alternate" hreflang="en" href="%s%s">'%(SITE,en),'<link rel="alternate" hreflang="x-default" href="%s%s">'%(SITE,fr)])

def scripts(url,typ):
    s=['<script src="/assets/site.js?v=%s" defer></script>'%V]
    if url in('/demande/','/en/request/','/','/en/'): s.append('<script src="/assets/request.js?v=%s" defer></script>'%V)
    return '\n'.join(s)

def region(s,name,content):
    pat=re.compile(r'<!--@%s-->.*?<!--@/%s-->'%(name,name),re.S)
    assert pat.search(s),name
    return pat.sub(lambda m:'<!--@%s-->\n%s\n<!--@/%s-->'%(name,content,name),s,count=1)

def url_of(f):
    u='/'+f
    return re.sub(r'index\.html$','',u)

def run():
    n=0
    for r,d,fs in os.walk('.'):
        if r.startswith(('./design-system','./.git','./tools','./node_modules','./assets')):continue
        for x in fs:
            if not x.endswith('.html'):continue
            f=os.path.join(r,x)[2:];u=url_of(f);s=open(f,encoding='utf-8').read()
            if '<!--@top-->' not in s: continue
            lang=re.search(r'<html[^>]*lang="(\w+)"',s).group(1)
            typ=types.get(u,'page')
            s=region(s,'css',css(typ,u))
            s=s.replace('%2308090C','%23050E1D').replace('%23C4A469','%23CEA152')
            s=s.replace("connect-src 'self' https://www.googletagmanager.com","connect-src 'self' https://script.google.com https://script.googleusercontent.com https://www.googletagmanager.com") if 'script.google.com' not in s else s
            hl=hreflang(u,lang)
            # hreflang: drop previous static ones, then place after canonical
            s=re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?','',s)
            s=re.sub(r'<!--@hreflang-->.*?<!--@/hreflang-->\n?','',s,flags=re.S)
            if hl: s=s.replace('<link rel="canonical"','<!--@hreflang-->\n%s\n<!--@/hreflang-->\n<link rel="canonical"'%hl,1) if False else re.sub(r'(<link rel="canonical" href="[^"]*">)',lambda m:m.group(1)+'\n<!--@hreflang-->\n'+hl+'\n<!--@/hreflang-->',s,count=1)
            s=region(s,'top',header(lang,u))
            s=region(s,'bottom',footer(lang,u))
            s=region(s,'scripts',scripts(u,typ))
            open(f,'w',encoding='utf-8').write(s);n+=1
    print('synced',n,'pages, asset version',V)

if __name__=='__main__': run()
