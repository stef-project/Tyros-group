#!/usr/bin/env python3
"""One-shot: routes every CTA to the journey it stands for, keeps the offer context in the URL,
and makes every internal link language-correct (EN pages never point at FR pages)."""
import os,re,json,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import sync
req=sync.req
twins=json.load(open('tools/twins.json'));rev={v:k for k,v in twins.items()}
KIND={ # FR url -> (kind, offer)
'/recrutement-chief-risk-officer/':('recruitment','cro'),'/recrutement-chief-compliance-officer/':('recruitment','cco'),
'/executive-search-banque-assurance/':('recruitment','banking-insurance'),'/executive-search-actuariat-assurance/':('recruitment','actuarial'),
'/ai-act-gouvernance-ia-finance/':('consulting','ai-act'),'/for-boards-executives/':('general','boards'),
'/dora-awareness/':('academy','dora-awareness'),'/formation-ia-banque-assurance/':('academy','ai-literacy'),
'/formation-manager-recrutement/':('academy','manager-recruiter'),'/formation-recrutement-talents-finance/':('academy','specialist-talent'),
'/formation-business-development-finance/':('academy','business-development'),'/formation-relation-client-b2b/':('academy','client-relationships'),
'/insights/ai-act-risk-compliance/':('consulting','ai-act'),'/insights/ai-act-article-4-ce-qui-change/':('academy','ai-literacy'),
'/insights/executive-search-vs-recrutement/':('recruitment','executive-search'),'/insights/conformite-avantage-competitif/':('consulting','compliance'),
}
TXT={'recruitment':('Demander une recherche','Request a search'),'consulting':('Demander un conseil','Request a consultation'),
     'general':('Échange confidentiel','Book a Discussion'),'academy':('Demander le programme','Request the programme')}
SESSION=('Organiser une session pour mon équipe','Arrange a session for my team')
def unesc(h): return h.replace('&amp;','&')
def localize_links(s,lang):
    """EN pages: FR page URLs and the FR home -> EN twins."""
    if lang!='en': return s
    def f(m):
        h=m.group(2)
        if h.startswith(('/assets','/fonts','/en/','/downloads')) or not h.startswith('/'): return m.group(0)
        base,hash_=(h.split('#')+[''])[:2] if '#' in h else (h,'')
        t=twins.get(base)
        if base=='/': t='/en/'
        if not t: return m.group(0)
        return m.group(1)+t+('#'+hash_ if hash_ else '')+'"'
    return re.sub(r'(href=")(/[^"]*)"',lambda m:f(m),s)
def process(f,url,lang):
    s=open(f,encoding='utf-8').read();o=s
    fr_url=url if lang=='fr' else rev.get(url)
    kind=KIND.get(fr_url)
    li=0 if lang=='fr' else 1
    if kind and url not in('/','/en/'):
        k,offer=kind
        src=url
        pat=re.compile(r'<a href="((?:/en)?/?#contact)"([^>]*)>(.*?)</a>',re.S)
        if k=='academy':
            # rebuild the page-cta block / byline CTA group
            prog=req(lang,'academy',offer,'programme',src);sess=req(lang,'academy',offer,'session',src)
            def cta(m):
                inner=m.group(2)
                home=sync.L[lang]['home']
                disc=re.search(r'<a href="[^"]*" class="btn btn-ghost">(Découvrir Tyros Academy[^<]*|Discover Tyros Academy[^<]*)</a>',inner)
                more='<a href="%s#academy" class="btn-text">%s</a>'%(home,disc.group(1)) if disc else ''
                return ('<div class="page-cta">\n  <a href="%s" class="btn btn-primary">%s</a>\n  <a href="%s" class="btn btn-ghost">%s</a>\n  %s\n</div>'
                        %(prog,TXT['academy'][li],sess,SESSION[li],more))
            s,n=re.subn(r'<div class="page-cta">(\s*)(.*?)\s*</div>',lambda m:cta(re.match(r'(.*)',m.group(0),re.S) and type('M',(),{'group':lambda self,i:m.group(2)})()),s,flags=re.S)
            s=re.sub(r'<a href="(?:/en)?/?#contact">([^<]*)</a>',lambda m:'<a href="%s">%s</a>'%(sess,m.group(1)),s)   # inline links
            # article CTA (insights): primary + ghost
            s=re.sub(r'(<div class="a-wrap cta">\s*)<a href="(?:/en)?/?#contact" class="btn btn-primary">[^<]*(?:<span class="ar">→</span>)?</a>',
                     lambda m:m.group(1)+'<a href="%s" class="btn btn-primary">%s <span class="ar">→</span></a>'%(sess if False else prog,TXT['academy'][li]),s)
        else:
            href=req(lang,k,offer,None,src)
            txt=TXT[k][li]
            s=re.sub(r'<a href="(?:/en)?/?#contact" class="btn btn-primary">[^<]*(?:<span class="ar">→</span>)?</a>',
                     lambda m:'<a href="%s" class="btn btn-primary">%s%s</a>'%(href,txt,' <span class="ar">→</span>' if 'span class="ar"' in m.group(0) else ''),s)
            s=re.sub(r'<a href="(?:/en)?/?#contact">([^<]*)</a>',lambda m:'<a href="%s">%s</a>'%(href,m.group(1)),s)
    s=localize_links(s,lang)
    if s!=o: open(f,'w',encoding='utf-8').write(s)
    return s!=o
n=0
for r,d,fs in os.walk('.'):
    if r.startswith(('./design-system','./.git','./tools','./assets','./node_modules')): continue
    for x in fs:
        if x!='index.html' and x!='404.html': continue
        f=os.path.join(r,x)[2:];u=sync.url_of(f)
        txt=open(f,encoding='utf-8').read()
        if '<!--@top-->' not in txt or u in('/','/en/'): continue
        lang=re.search(r'<html[^>]*lang="(\w+)"',txt).group(1)
        n+=process(f,u,lang)
print('routed',n,'pages')
