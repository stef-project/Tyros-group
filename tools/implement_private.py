#!/usr/bin/env python3
"""One-shot: Intelligence restructure, Tyros Private section, Membership note, Advisory link, international stat (FR and EN homes)."""
import re,os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import forms
L={
'fr':dict(file='index.html',req='/demande/',home='/',priv='/tyros-private/',adv='/ai-act-gouvernance-ia-finance/',
 d2_tag='Tyros Intelligence',
 d4=('Des rencontres exécutives, sur mandat.','Introductions, déjeuners et dîners privés, tables rondes : nous concevons et organisons des rencontres avec des décideurs ciblés, pour les organisations qui nous mandatent.'),
 intel_p="Une pratique de recherche, pas un blog. Nous transformons notre proximité avec le marché des dirigeants en intelligence d'aide à la décision. Le périmètre et les données disponibles sont définis pour chaque mandat.",
 intel=[('Intelligence de marché et concurrentielle','Comprendre votre marché.','Mouvements de dirigeants, structure du marché, dynamiques de recrutement et positionnement de vos concurrents, analysés fonction par fonction.','intel-market'),
        ('Cartographie des talents et des dirigeants','Savoir qui compte, et où.',"Cartographie confidentielle du leadership et des fonctions critiques d'un marché, avec les profils clés à connaître.",'intel-mapping'),
        ('Benchmarks de rémunération','Positionner vos rémunérations.','Références de rémunération des dirigeants par fonction, secteur et marché. Le périmètre géographique et les données disponibles sont précisés pour chaque mandat.','intel-comp'),
        ('Analyses sectorielles et réglementaires','Anticiper ce qui change.',"Ce que l'AI Act, DORA et l'évolution du secteur changent pour les organisations et leurs dirigeants.",'intel-reg')],
 cad='Sur mandat ou dans le cadre du Membership',
 pv=dict(eyebrow='Tyros Private',h2='Les bonnes conversations. Les bons décideurs. Le bon cadre.',
   p='Tyros conçoit et organise des rencontres exécutives confidentielles pour les organisations souhaitant présenter une innovation, explorer un marché ou développer des relations stratégiques de haut niveau.',
   rows=[('Private Executive Introductions','Des introductions ciblées et confidentielles.',"Identification, qualification et mise en relation de dirigeants, d'investisseurs et de décideurs C-level : rencontres bilatérales, introductions ciblées, rendez-vous stratégiques.",'introductions'),
         ('Executive Private Events','Votre rencontre, conçue et organisée par Tyros.','Sur mandat : déjeuners privés, dîners, tables rondes stratégiques et rencontres sectorielles sur invitation, pour présenter une innovation ou développer des relations commerciales stratégiques.','events'),
         ('Strategic Market Access','Aborder un nouveau marché avec les bons interlocuteurs.',"En France, au Royaume-Uni et à l'international : identification des interlocuteurs stratégiques, qualification des opportunités, introductions et rencontres professionnelles.",'market-access')],
   note="Une entreprise peut nous mandater sans être membre. L'organisateur et la finalité de chaque rencontre sont annoncés aux invités, et la participation d'un dirigeant n'est jamais garantie.",
   b1='Organiser une rencontre privée',b2="Discuter d'un mandat stratégique"),
 ent='Invitations sélectives aux rencontres Tyros Private',
 memnote="Le Membership est un abonnement, distinct des missions Tyros Private. Les invitations aux rencontres Tyros Private sont sélectives, sous réserve de pertinence, de disponibilité et d'accord des organisateurs : aucune invitation n'est automatique.",
 stat=('London','Siège, accompagnement de mandats internationaux')),
'en':dict(file='en/index.html',req='/en/request/',home='/en/',priv='/en/tyros-private/',adv='/en/ai-act-ai-governance-financial-services/',
 d2_tag='Tyros Intelligence',
 d4=('Executive encounters, on mandate.','Introductions, private lunches and dinners, roundtables: we design and run meetings with targeted decision-makers, for the organisations that commission us.'),
 intel_p="A research practice, not a blog. We turn our proximity to the leadership market into decision-grade intelligence. Scope and available data are defined for each mandate.",
 intel=[('Market & Competitive Intelligence','Understand your market.','Leadership moves, market structure, hiring dynamics and the positioning of your competitors, analysed function by function.','intel-market'),
        ('Talent & Leadership Mapping','Know who matters, and where.','Confidential mapping of leadership and critical functions across a market, with the key profiles to know.','intel-mapping'),
        ('Compensation Benchmarks','Position your pay.','Executive pay references by function, sector and market. Geographic scope and available data are specified for each mandate.','intel-comp'),
        ('Sector & Regulatory Analyses','Anticipate what is changing.','What the AI Act, DORA and sector evolution change for organisations and their leaders.','intel-reg')],
 cad='On mandate or through Membership',
 pv=dict(eyebrow='Tyros Private',h2='The right conversations. The right people. The right setting.',
   p='We design and facilitate confidential executive encounters for organisations seeking to engage senior decision-makers, introduce innovative solutions, explore new markets and build strategic relationships.',
   rows=[('Private Executive Introductions','Targeted, confidential introductions.','Identification, qualification and introduction of executives, investors and C-level decision-makers: bilateral meetings, targeted introductions and strategic appointments.','introductions'),
         ('Executive Private Events','Your meeting, designed and run by Tyros.','On mandate: private lunches, dinners, strategic roundtables and invitation-only sector meetings, to present an innovation or build strategic commercial relationships.','events'),
         ('Strategic Market Access','Enter a new market with the right counterparts.','In France, the United Kingdom and internationally: identifying strategic counterparts, qualifying opportunities, introductions and professional meetings.','market-access')],
   note="A company can commission us without being a member. The organiser and purpose of every meeting are stated to invited guests, and no executive's attendance is ever guaranteed.",
   b1='Commission a Private Executive Event',b2='Discuss a Strategic Mandate'),
 ent='Selective invitations to Tyros Private meetings',
 memnote="Membership is a subscription, separate from Tyros Private engagements. Invitations to Tyros Private meetings are selective, subject to relevance, availability and the organisers' agreement: no invitation is automatic.",
 stat=('London','Headquarters, supporting international mandates')),
}
E=lambda x:x.replace('&','&amp;')
for lang,c in L.items():
    s=open(c['file'],encoding='utf-8').read()
    q=lambda offer,frm=None:'%s?offer=%s&amp;from=%s'%(c['req'],offer,frm or c['home'])
    # --- divisions: cards 02 (no tags), 03 (link + no hash anchor), 04
    s,n=re.subn(r'\s*<ul class="dlist"><li>(?:Rapports de marché|Market reports)</li>.*?</ul>','',s,count=1,flags=re.S);assert n==1,'tags'
    s,n=re.subn(r'<a class="divi" href="#advisory" id="advisory">','<a class="divi" href="%s" id="advisory">'%c['adv'],s);assert n==1,'adv'
    a=s.index('<a class="divi" href="%s'%c['req'][:6]) if False else s.index('id="private-access"')
    a=s.rfind('<a class="divi"',0,a);b=s.index('</a>',a)+4
    s=s[:a]+('<a class="divi" href="%s" id="private-access">\n        <div class="dnum">04</div>\n        <div><div class="dtag">Tyros Private</div><h3>%s</h3><p>%s</p></div>\n        <div class="darr">→</div>\n      </a>'%(c['priv'],E(c['d4'][0]),E(c['d4'][1])))+s[b:]
    # --- intelligence section
    a=s.index('<section class="sec sec-2" id="intelligence">');b=s.index('<!-- MEMBERSHIP -->')
    eyebrow='Tyros Intelligence'
    h2=re.search(r'<h2[^>]*>(.*?)</h2>',s[a:b],re.S).group(1)
    bar=re.search(r'<div class="ihub-bar">.*?</div>\s*</div>\s*</section>',s[a:b],re.S).group(0)
    cards=''.join('      <a class="ihub-card" href="%s">\n        <div class="ihub-cat">%s</div>\n        <h3>%s</h3>\n        <p class="ihub-p">%s</p>\n        <span class="ihub-cad">%s</span>\n      </a>\n'%(q(o),E(cat),E(h),E(d),E(c['cad'])) for cat,h,d,o in c['intel'])
    intel=('<section class="sec sec-2" id="intelligence">\n  <div class="wrap">\n    <div class="intel">\n      <div>\n        <div class="eyebrow">%s</div>\n        <h2>%s</h2>\n        <p>%s</p>\n      </div>\n    </div>\n    <div class="ihub-grid">\n%s    </div>\n    %s\n'%(eyebrow,h2,E(c['intel_p']),cards,bar))
    pv=c['pv']
    rows=''.join('      <a class="divi" href="%s#%s">\n        <div class="dnum">%02d</div>\n        <div><div class="dtag">%s</div><h3>%s</h3><p>%s</p></div>\n        <div class="darr">→</div>\n      </a>\n'%(c['priv'],anc,i+1,E(t),E(h),E(d)) for i,(t,h,d,anc) in enumerate(pv['rows']))
    private=('<!-- TYROS PRIVATE -->\n<section class="sec" id="private">\n  <div class="wrap">\n    <div class="sec-head">\n      <div class="eyebrow">%s</div>\n      <h2>%s</h2>\n      <p>%s</p>\n    </div>\n    <div class="divs">\n%s    </div>\n    <p class="private-note">%s</p>\n    <div class="private-cta">\n      <a href="%s" class="btn btn-primary">%s</a>\n      <a href="%s" class="btn btn-ghost">%s</a>\n    </div>\n  </div>\n</section>\n\n'%(pv['eyebrow'],E(pv['h2']),E(pv['p']),rows,E(pv['note']),q('private-event'),E(pv['b1']),q('private-mandate'),E(pv['b2'])))
    s=s[:a]+intel+private+s[b:]
    # --- membership: enterprise line + note
    ent_old=re.search(r'<li><span class="ck">✓</span><span>(?:Événements &amp; forums privés|Private events &amp; forums)</span></li>',s);assert ent_old,'ent'
    s=s.replace(ent_old.group(0),'<li><span class="ck">✓</span><span>%s</span></li>'%E(c['ent']))
    i=s.index('<div class="mem-grid">');j=s.index('</section>',i)
    k=s.rfind('</div>',i,j);k=s.rfind('</div>',i,k)  # closing of mem-grid is the one before the wrap's closing
    grid_end=s.index('\n  </div>\n</section>',i)
    s=s[:grid_end]+'\n    <p class="mem-note">%s</p>'%E(c['memnote'])+s[grid_end:]
    # --- stat
    s,n=re.subn(r'<div class="stat"><div class="v" data-count="4">4</div><div class="l">[^<]*</div></div>','<div class="stat"><div class="v">%s</div><div class="l">%s</div></div>'%c['stat'],s);assert n==1,'stat'
    # --- JSON-LD areaServed
    s=re.sub(r',"areaServed":\[[^\]]*\]','',s)
    # --- config
    s=re.sub(r'(<script type="application/json" id="req-config">).*?(</script>)',lambda m:m.group(1)+forms.config(lang)+m.group(2),s,count=1,flags=re.S)
    open(c['file'],'w',encoding='utf-8').write(s)
    print(lang,'ok')
# numerals 07/08 -> 08/09
p='assets/tyros-bplus.css';t=open(p,encoding='utf-8').read()
t=t.replace('#academy::after{content:"07"','#academy::after{content:"08"').replace('.contact::after{content:"08"','.contact::after{content:"09"')
open(p,'w',encoding='utf-8').write(t)
open('assets/tyros-theme.css','a').write('''
/* home: Intelligence cards with description, Tyros Private block, membership note */
.ihub-p{margin:.1rem 0 0;font-size:.92rem;line-height:1.55;color:var(--ivory-soft);max-width:48ch;}
.private-note,.mem-note{margin:1.6rem 0 0;font-size:.92rem;line-height:1.6;color:var(--ivory-mute);max-width:70ch;border-left:2px solid var(--gold);padding-left:1rem;}
.mem-note{margin-top:2.2rem;}
.private-cta{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.8rem;}
''')
