#!/usr/bin/env python3
"""One-shot (already applied): Membership withdrawn as a public offer. Home section, nav, footer, form subjects, CSS removed;
Intelligence gets one discreet invitation sentence. Rerunning is a no-op on the homes (asserts guard)."""
import re,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
NOTE={'index.html':"Certains briefings et rencontres peuvent être proposés sur invitation à des clients et dirigeants de l'écosystème Tyros.",
      'en/index.html':"Selected briefings and private discussions may be offered by invitation to clients and senior members of the Tyros ecosystem."}
for f,note in NOTE.items():
    s=open(f,encoding='utf-8').read()
    a=s.index('<!-- MEMBERSHIP -->');b=s.index('<!-- INSIGHTS -->');s=s[:a]+s[b:]
    s=re.sub(r'<span class="ihub-cad">(Sur mandat ou dans le cadre du Membership|On mandate or through Membership)</span>',lambda m:'<span class="ihub-cad">%s</span>'%('Sur mandat' if f=='index.html' else 'On mandate'),s)
    k=s.index('    <div class="ihub-bar">')
    s=s[:k]+'    <p class="invite-note">%s</p>\n'%note+s[k:]
    s=s.replace('Une organisation peut nous mandater sans être membre. ','Une organisation peut nous mandater pour une mission ponctuelle. ')
    open(f,'w',encoding='utf-8').write(s)
def sub(p,pairs):
    t=open(p,encoding='utf-8').read()
    for a,b in pairs:
        assert a in t,(p,a[:40]);t=t.replace(a,b)
    open(p,'w',encoding='utf-8').write(t)
# CSS
for p in ('assets/css/home.css','assets/css/article.css','assets/css/boards.css','assets/css/page.css'):
    t=open(p,encoding='utf-8').read()
    t=re.sub(r'(?m)^\.mem[^\n]*\n|^:root\[lang="en"\] \.mem[^\n]*\n|^@media\(max-width:900px\)\{\.mem-grid[^\n]*\n','',t)
    t=re.sub(r'/\* membership \*/\n','',t);open(p,'w',encoding='utf-8').write(t)
t=open('assets/tyros-bplus.css',encoding='utf-8').read()
a=t.index('/* 7. MEMBERSHIP');b=t.index('/* 8. INSIGHTS');t=t[:a]+t[b:]
t=re.sub(r'(?m)^:root\[data-theme="dark"\] \.mem\.feat::before[^\n]*\n','',t)
t=t.replace('.tr-item,.ins,.cinfo,.mem,','.tr-item,.ins,.cinfo,').replace('.ins:hover,.mem:hover,','.ins:hover,')
t=t.replace('#academy::after{content:"08"','#academy::after{content:"07"').replace('.contact::after{content:"09"','.contact::after{content:"08"')
open('assets/tyros-bplus.css','w',encoding='utf-8').write(t)
t=open('assets/tyros-ds.css',encoding='utf-8').read()
t=re.sub(r'(?m)^(\[data-theme="dark"\] )?\.mem\.feat::before[^\n]*\n','',t)
t=t.replace(',.mem .tier','').replace('.mem:hover,','')
open('assets/tyros-ds.css','w',encoding='utf-8').write(t)
sub('assets/tyros-theme.css',[('.mem,.ind,.divi,.ins{','.ind,.divi,.ins{'),('.mem.feat{border-top-color:var(--gold);}\n',''),
 ('.private-note,.mem-note{','.private-note,.invite-note{'),('.mem-note{margin-top:2.2rem;}','.invite-note{margin-top:1.6rem;}'),('Tyros Private block, membership note','Tyros Private block, invitation note')])
# nav, footer, forms, tests
sub('tools/sync.py',[(",('Membership','#membership')",''),('<a href="{h}#membership">Membership</a>','')])
sub('tools/forms.py',[(" 'membership-essential':('plain','Membership Essential','Membership Essential'),\n",''),(" 'membership-professional':('plain','Membership Professional','Membership Professional'),\n",''),(" 'membership-enterprise':('plain','Membership Enterprise','Membership Enterprise'),\n",'')])
sub('tools/test_forms.js',[(" ['FR membership','/demande/?offer=membership-professional&from=/','Membership Professional',{offer:'membership-professional'}],\n",'')])
print('membership removed')
