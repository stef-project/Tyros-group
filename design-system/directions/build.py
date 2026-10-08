#!/usr/bin/env python3
"""Builds the three draft home directions from the live index.html. Preview only, never published."""
import re,os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')+'/'
src=open(R+'index.html',encoding='utf-8').read()

def build(key,extra=None):
    t=src
    # 1. wrap sub + actions FIRST (before anything is inserted in the hero)
    hs=t.index('<section class="hero">'); he=t.index('</section>',hs)
    hero=t[hs:he]
    m=re.search(r'(<p class="sub"[^>]*>.*?</p>)\s*(<div class="hero-actions">.*?</div>)\s*(</div>\s*)$',hero,re.S)
    assert m,'hero structure'
    hero=hero[:m.start()]+'<div class="hero-side">'+m.group(1)+m.group(2)+'</div>\n  '+m.group(3)
    # 2. move the stats strip into the hero (after hero-inner)
    sm=re.search(r'<section class="stats reveal">\s*(<div class="wrap stats-grid">.*?</div>)\s*</section>',t,re.S)
    assert sm,'stats'
    hero=hero+'  <div class="hero-stats">'+sm.group(1)+'</div>\n'
    t=t[:hs]+hero+t[he:]
    t=t.replace(sm.group(0),'',1)
    # 3. stylesheets
    link='<link rel="stylesheet" href="/assets/tyros-ds.css?v=20261008">'
    assert link in t
    t=t.replace(link,link+'\n<link rel="stylesheet" href="/design-system/directions/tokens/tyros-tokens.css">\n<link rel="stylesheet" href="/design-system/directions/common.css">\n<link rel="stylesheet" href="/design-system/directions/%s/dir.css">'%key,1)
    if extra: t=extra(t)
    t=t.replace('<title>','<title>[Direction %s, draft] '%key,1)
    os.makedirs(R+'design-system/directions/'+key,exist_ok=True)
    open(R+'design-system/directions/%s/index.html'%key,'w',encoding='utf-8').write(t)

def extraC(t):
    t=t.replace('<span class="grad">Leadership</span><br>Shapes Markets.','<span class="l1">Leadership</span> <span class="l2">Shapes Markets<span class="dot">.</span></span>',1)
    rail='''<nav class="rail" aria-label="Sections"><a href="#about"><i>01</i><span>À propos</span></a><a href="#services"><i>02</i><span>Divisions</span></a><a href="#industries"><i>03</i><span>Industries</span></a><a href="#intelligence"><i>04</i><span>Intelligence</span></a><a href="#membership"><i>05</i><span>Membership</span></a><a href="#insights"><i>06</i><span>Insights</span></a><a href="#academy"><i>07</i><span>Academy</span></a><a href="#contact"><i>08</i><span>Contact</span></a></nav>
<script>(function(){var l=document.querySelectorAll('.rail a');if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){l.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-40% 0px -55% 0px'});[].forEach.call(l,function(a){var el=document.getElementById(a.getAttribute('href').slice(1));if(el)io.observe(el)})})();</script>
'''
    return t.replace('<main id="main">',rail+'<main id="main">',1)

def extraBplus(t):
    t=t.replace('<span class="grad">Leadership</span><br>Shapes Markets.','<span class="l1">Leadership</span> <span class="l2">Shapes Markets<span class="dot">.</span></span>',1)
    assert 'class="l1"' in t
    return t

for k,fn in (('A',None),('B',None),('C',extraC),('Bplus',extraBplus)): build(k,fn)
print('built A, B, C, Bplus')
