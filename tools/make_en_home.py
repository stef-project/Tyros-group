#!/usr/bin/env python3
"""One-shot: builds /en/index.html from index.html by applying, statically, the English strings that the former
client-side toggle held in data-en. Then strips data-en from both files (single mechanism: one URL per language)."""
import re,html,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
def swap(s):
    out=[];pos=0
    tag=re.compile(r'<(\w+)\b[^>]*?\sdata-en="([^"]*)"[^>]*>')
    while True:
        m=tag.search(s,pos)
        if not m: out.append(s[pos:]);break
        name=m.group(1);start=m.end()
        # find matching close of same tag name
        depth=1;i=start;op=re.compile(r'<%s\b'%name);cl=re.compile(r'</%s\s*>'%name)
        while depth:
            mo=op.search(s,i);mc=cl.search(s,i)
            assert mc,('unclosed',name,m.group(0)[:80])
            if mo and mo.start()<mc.start(): depth+=1;i=mo.end()
            else: depth-=1;i=mc.end() if depth==0 else mc.end();end_inner=mc.start()
        en=html.unescape(m.group(2))
        en=re.sub(r'&(?!#?\w+;)','&amp;',en)
        opening=re.sub(r'\sdata-en="[^"]*"','',m.group(0))
        out.append(s[pos:m.start()]);out.append(opening+en+s[end_inner:i])
        pos=i
    return ''.join(out)
def strip(s): return re.sub(r'\sdata-en="[^"]*"','',s)
fr=open('index.html',encoding='utf-8').read()
en=swap(fr)
assert 'data-en' not in en.replace('data-en-','')
# meta
rep=[('<html lang="fr">','<html lang="en">'),
 ('<link rel="canonical" href="https://tyros-group.com/">','<link rel="canonical" href="https://tyros-group.com/en/">'),
 ('<meta property="og:url" content="https://tyros-group.com/">','<meta property="og:url" content="https://tyros-group.com/en/">'),
 ('<meta property="og:locale" content="fr_FR">','<meta property="og:locale" content="en_GB">'),
 ('<meta property="og:locale:alternate" content="en_GB">','<meta property="og:locale:alternate" content="fr_FR">'),
 ('og-tyros-group-fr.png','og-tyros-group-en.png'),
 ('content="Partenaire stratégique en leadership et intelligence pour les institutions financières : executive search, intelligence de marché et advisory."','content="A strategic leadership and intelligence partner for financial institutions: executive search, market intelligence and advisory."'),
 ('content="Tyros Group. Services financiers. Conseil, Recrutement, Executive Education."','content="Tyros Group. Financial services. Advisory, Recruitment, Executive Education."'),
 ('"url":"https://tyros-group.com/"','"url":"https://tyros-group.com/en/"')]
for a,b in rep:
    assert a in en,a
    en=en.replace(a,b)
os.makedirs('en',exist_ok=True)
open('en/index.html','w',encoding='utf-8').write(strip(en))
open('index.html','w',encoding='utf-8').write(strip(fr))
print('en home written; data-en stripped from FR home')
