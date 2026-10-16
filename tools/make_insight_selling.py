#!/usr/bin/env python3
"""Insights article: selling to financial institutions (FR + EN). Idempotent. Builds both pages from the structure of an existing article,
registers the twin pair, adds the card to both Insights hubs. Run tools/sync.py and tools/make_sitemap.py afterwards."""
import os,re,json
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'));os.chdir(ROOT)
SITE='https://tyros-group.com'
A={
'fr':dict(skel='insights/conformite-avantage-competitif/index.html',url='/insights/vendre-aux-institutions-financieres/',hub='/insights/',home_name='Accueil',
 title='Vendre aux institutions financières | Tyros Group',
 desc="Une méthode commerciale donne un cadre, pas un résultat : circuit de décision, régulation, preuve dans les institutions financières.",
 h1='Vendre aux institutions financières&nbsp;: ce que les stratégies commerciales classiques ignorent',
 h1_plain='Vendre aux institutions financières : ce que les stratégies commerciales classiques ignorent',
 stand="Une banque ou un assureur n'achète pas comme une autre entreprise. Les approches qui fonctionnent ailleurs s'y heurtent à des processus de décision, des exigences de diligence et une culture de la preuve qui leur sont propres.",
 cat='Market',kind='Perspective',date='Octobre 2026',iso='2026-10-16',ctalabel='Échanger avec Tyros Group',allbtn='← Tous les Insights',more='À lire également',
 req='/demande/',
 body='''<p>Une méthode commerciale peut fournir un cadre. Elle ne produit pas les mêmes résultats d'une institution à l'autre, d'une géographie à l'autre, d'un marché à l'autre. Les entreprises technologiques, les cabinets de conseil et les investisseurs qui abordent une banque ou un assureur avec leur méthode habituelle (démonstration, période d'essai, volume de prospection) le découvrent vite : dans ce secteur, une décision d'achat mal préparée engage la responsabilité de l'institution devant son superviseur.</p>
<h2>Un intérêt n'est pas un contrat</h2>
<p>Prenons un exemple hypothétique. Une fintech propose une solution de paiement à une banque. Elle convainc la direction de l'innovation de l'intérêt du produit. Cet intérêt ne vaut pas validation : il reste à obtenir l'accord de la sécurité, de la gestion des risques, des achats et d'un sponsor qui porte le budget. Chacun juge la même solution à travers un risque différent.</p>
<h2>Un achat est un processus, non une décision</h2>
<p>L'implication des fonctions de contrôle et de support dépend de la matérialité de la prestation, du type de fournisseur et des procédures de l'institution. Pour un service important ou critique, le risque, la sécurité de l'information, la conformité, les achats et le juridique interviennent généralement. Pour une prestation marginale, le circuit est plus léger.</p>
<p>Une stratégie commerciale qui ne s'adresse qu'au sponsor métier laisse sans réponse les objections les plus sérieuses. Il faut cartographier le processus (qui valide, qui peut bloquer, dans quel ordre) avant de choisir l'interlocuteur à rencontrer, pas après.</p>
<h2>La réglementation structure les priorités commerciales</h2>
<p>Dans l'Union, DORA s'applique depuis le 17 janvier 2025 et place la maîtrise des prestataires tiers de technologies de l'information au centre des exigences de résilience. Au Royaume-Uni, le régime des prestataires tiers critiques est opérationnel depuis la désignation des premiers prestataires en juillet 2026, et de nouvelles obligations de déclaration des incidents opérationnels et de certains arrangements avec des tiers s'appliqueront à partir du 18 mars 2027. L'encadrement de l'intelligence artificielle relève d'un autre cadre.</p>
<p>Ces dispositifs ne sont pas interchangeables : leurs périmètres et leurs échéances diffèrent. Une offre qui répond à une obligation que l'institution a déjà identifiée trouve plus facilement un sponsor qu'une offre présentée comme une innovation de plus. Et le fournisseur lui-même doit anticiper ce qu'on lui demandera : contrôle, audit, réversibilité, sous-traitance.</p>
<div class="pull">Dans les services financiers, la bonne conversation précède la bonne offre.</div>
<h2>La preuve avant la promesse</h2>
<p>L'une des premières questions est presque toujours : « Qui d'autre l'utilise ? ». Pour un nouvel entrant, la réponse manque par définition. La preuve se construit donc autrement : un cadrage honnête de ce que l'offre fait et ne fait pas, une documentation prête pour la diligence, des échanges avec des pairs qui peuvent confirmer la pertinence du sujet. Les promesses de gains chiffrés, difficiles à vérifier, desservent la crédibilité plus qu'elles ne la servent.</p>
<h2>Un marché, des réalités différentes</h2>
<p>France, Royaume-Uni, Benelux, Suisse : les superviseurs, les calendriers, les langues et les habitudes d'achat diffèrent. Les mêmes mots (résilience, tiers critique, IA à haut risque) ne recouvrent ni les mêmes obligations ni les mêmes interlocuteurs d'un pays à l'autre.</p>
<h2>Ce que cela change pour la démarche commerciale</h2>
<ul>
<li>Partir de l'agenda de l'interlocuteur (réglementaire, risque, transformation) avant de décrire l'offre.</li>
<li>Cartographier le processus de décision et préparer une réponse pour chaque fonction concernée.</li>
<li>Préparer la diligence avant qu'elle ne soit demandée.</li>
<li>Préférer quelques conversations de qualité à un volume d'approches.</li>
<li>Adapter la démarche marché par marché.</li>
</ul>
<p>Dans les services financiers, la performance commerciale ne repose pas sur la reproduction d'une méthode d'un marché à l'autre. Elle dépend de la capacité à comprendre les mécanismes de décision, les contraintes de chaque organisation et les conditions réelles d'accès au marché.</p>
<p>C'est cette lecture que Tyros Group place au cœur de son approche : conjuguer intelligence de marché, stratégie commerciale et connaissance des organisations pour transformer les ambitions de développement en opportunités concrètes. Les organisations qui préparent leur arrivée sur un marché peuvent s'appuyer sur <a href="/tyros-private/">Tyros Private</a>.</p>
<p><em>Ce texte propose une analyse générale. Il ne constitue ni un conseil juridique ni un conseil réglementaire.</em></p>''',
 related=[('/insights/executive-search-vs-recrutement/','Leadership · Avril 2026',"Les dirigeants clés ne se cherchent pas en surface"),('/insights/conformite-avantage-competitif/','Market · Février 2026','La conformité : de centre de coût à avantage compétitif')],
 hub_d='Octobre 2026 · Perspective'),
'en':dict(skel='en/insights/compliance-as-a-competitive-advantage/index.html',url='/en/insights/selling-to-financial-institutions/',hub='/en/insights/',home_name='Home',
 title='Selling to financial institutions | Tyros Group',
 desc='A commercial method provides a framework, not a result: decision circuits, regulation and proof in financial institutions.',
 h1='Selling to financial institutions: what conventional commercial strategies overlook',
 h1_plain='Selling to financial institutions: what conventional commercial strategies overlook',
 stand="A bank or an insurer does not buy like any other company. Approaches that work elsewhere run into decision processes, due-diligence requirements and a culture of proof that are specific to the sector.",
 cat='Market',kind='Perspective',date='October 2026',iso='2026-10-16',ctalabel='Talk to Tyros Group',allbtn='← All Insights',more='Related reading',
 req='/en/request/',
 body='''<p>A commercial method can provide a framework. It does not produce the same results from one institution to the next, one geography to the next, one market to the next. Technology companies, advisory firms and investors approaching a bank or an insurer with their usual method (demonstration, trial period, volume of outreach) soon find this out: in this sector, a poorly prepared purchasing decision engages the institution's responsibility before its supervisor.</p>
<h2>Interest is not a contract</h2>
<p>Take a hypothetical example. A fintech offers a payment solution to a bank. It convinces the innovation team of the product's value. That interest is not approval: agreement is still needed from security, risk management, procurement and a sponsor who carries the budget. Each judges the same solution through a different risk.</p>
<h2>Buying is a process, not a single decision</h2>
<p>How far control and support functions are involved depends on the materiality of the service, the type of supplier and the institution's procedures. For an important or critical service, risk, information security, compliance, procurement and legal are generally involved. For a marginal service, the circuit is lighter.</p>
<p>A commercial strategy that addresses only the business sponsor leaves the most serious objections unanswered. The process (who approves, who can block, in what order) has to be mapped before choosing whom to meet, not afterwards.</p>
<h2>Regulation shapes commercial priorities</h2>
<p>In the Union, DORA has applied since 17 January 2025 and puts the control of ICT third-party providers at the centre of resilience requirements. In the United Kingdom, the critical third parties regime became operational with the designation of the first providers in July 2026, and new rules on reporting operational incidents and certain third-party arrangements will apply from 18 March 2027. AI governance and regulatory requirements fall under a different framework.</p>
<p>These regimes are not interchangeable: their scope and timetables differ. An offer that answers an obligation the institution has already identified finds a sponsor more easily than one presented as one more innovation. And the supplier must anticipate what it will be asked: oversight, audit, exit, subcontracting.</p>
<div class="pull">In financial services, the right conversation comes before the right offer.</div>
<h2>Proof before promise</h2>
<p>One of the first questions is almost always: "Who else uses it?". For a new entrant, the answer is missing by definition. Proof has to be built differently: an honest framing of what the offer does and does not do, documentation ready for due diligence, exchanges with peers who can confirm the relevance of the subject. Promises of quantified gains, hard to verify, damage credibility more than they build it.</p>
<h2>One market, different realities</h2>
<p>France, the United Kingdom, Benelux, Switzerland: supervisors, calendars, languages and purchasing habits differ. The same words (resilience, critical third party, high-risk AI) cover neither the same obligations nor the same counterparts from one country to the next.</p>
<h2>What this changes for the commercial approach</h2>
<ul>
<li>Start from the counterpart's agenda (regulatory, risk, transformation) before describing the offer.</li>
<li>Map the decision process and prepare an answer for each function involved in the approval process.</li>
<li>Prepare due diligence before it is requested.</li>
<li>Prefer a few high-quality conversations to a volume of approaches.</li>
<li>Adapt the approach market by market.</li>
</ul>
<p>In financial services, commercial performance does not come from repeating one method from one market to the next. It depends on understanding how decisions are made, the constraints of each organisation and the real conditions of market access.</p>
<p>This is the reading Tyros Group puts at the heart of its approach: combining market intelligence, commercial strategy and knowledge of organisations to turn growth ambitions into concrete opportunities. Organisations preparing their arrival in a market can draw on <a href="/en/tyros-private/">Tyros Private</a>.</p>
<p><em>This text offers a general analysis. It is neither legal advice nor regulatory advice.</em></p>''',
 related=[('/en/insights/executive-search-vs-recrutement/','Leadership · April 2026','Key leaders are not found at the surface'),('/en/insights/compliance-as-a-competitive-advantage/','Market · February 2026','Compliance: from cost centre to competitive edge')],
 hub_d='October 2026 · Perspective')}
E=lambda x:x.replace('&','&amp;')
for lang,c in A.items():
    s=open(c['skel'],encoding='utf-8').read()
    def sub(pat,new,flags=0):
        global s
        s,n=re.subn(pat,lambda m:new,s,count=1,flags=flags);assert n==1,pat
    ti=E(c['title']);de=E(c['desc'])
    sub(r'<title>.*?</title>','<title>%s</title>'%ti)
    sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="%s">'%de)
    sub(r'<link rel="canonical" href="[^"]*">','<link rel="canonical" href="%s%s">'%(SITE,c['url']))
    sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="%s">'%E(c['h1_plain']))
    sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="%s">'%de)
    sub(r'<meta property="og:url" content="[^"]*">','<meta property="og:url" content="%s%s">'%(SITE,c['url']))
    sub(r'<meta property="article:published_time" content="[^"]*">','<meta property="article:published_time" content="%s">'%c['iso'])
    art={"@context":"https://schema.org","@type":"Article","headline":c['h1_plain'],"description":c['desc'],"datePublished":c['iso'],"inLanguage":lang,"articleSection":c['cat'],"author":{"@type":"Organization","name":"Tyros Group"},"publisher":{"@type":"Organization","name":"Tyros Group","url":SITE+"/"},"mainEntityOfPage":SITE+c['url'],"url":SITE+c['url'],"isPartOf":{"@type":"Blog","name":"Tyros Insights","url":SITE+c['hub']}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":c['home_name'],"item":SITE+('/' if lang=='fr' else '/en/')},{"@type":"ListItem","position":2,"name":"Insights","item":SITE+c['hub']},{"@type":"ListItem","position":3,"name":c['h1_plain'],"item":SITE+c['url']}]}
    blocks=re.findall(r'<script type="application/ld\+json">.*?</script>',s,re.S);assert len(blocks)==2
    s=s.replace(blocks[0],'<script type="application/ld+json">\n%s\n</script>'%json.dumps(art,ensure_ascii=False))
    s=s.replace(blocks[1],'<script type="application/ld+json">\n%s\n</script>'%json.dumps(bc,ensure_ascii=False))
    rel=''.join('<a class="a-card" href="%s"><div class="d">%s</div><h3>%s</h3></a>\n'%(u,E(d),E(t)) for u,d,t in c['related'])
    main=f'''<main id="main">
<div class="a-hero">
  <div class="a-wrap">
    <div class="a-meta"><span class="cat">{c['cat']}</span><span>·</span><span>{c['kind']}</span></div>
    <h1>{c['h1']}</h1>
    <p class="a-stand">{c['stand']}</p>
    <div class="a-byline"><span class="au">Tyros Group · Insights</span><span><span style="color:var(--grey-2)">{c['date']}</span> &nbsp;</span></div>
  </div>
</div>
<article class="a-body">
  <div class="a-wrap">
    {c['body']}
  </div>
</article>
<div class="a-foot">
  <div class="a-wrap cta">
    <a href="{c['req']}?type=general&amp;from={c['url']}" class="btn btn-primary">{c['ctalabel']} <span class="ar">→</span></a>
    <a href="{c['hub']}" class="btn btn-ghost">{c['allbtn']}</a>
  </div>
</div>
<div class="a-more">
  <div class="a-wrap">
    <h2>{c['more']}</h2>
    <div class="a-more-grid">
      {rel}    </div>
  </div>
</div>
</main>'''
    s=re.sub(r'<main id="main">.*?</main>',lambda m:main,s,count=1,flags=re.S)
    out=c['url'].strip('/')+'/index.html';os.makedirs(os.path.dirname(out),exist_ok=True)
    open(out,'w',encoding='utf-8').write(s)
    # hub card, first in the grid
    hp=c['hub'].strip('/')+'/index.html';h=open(hp,encoding='utf-8').read()
    if c['url'] not in h:
        rd='Lire →' if lang=='fr' else 'Read →'
        card=f'''<a class="hub-card" href="{c['url']}">
      <div class="top"><span class="cat">{c['cat']}</span></div>
      <div class="b"><div class="d">{c['hub_d']}</div><h2>{E(c['h1_plain'])}</h2><span class="rd">{rd}</span></div>
    </a>
'''
        k=h.index('<div class="hub-grid">')+len('<div class="hub-grid">\n')
        h=h[:k]+card+h[k:]
        open(hp,'w',encoding='utf-8').write(h)
# twins and types
tw=json.load(open('tools/twins.json'));tw[A['fr']['url']]=A['en']['url'];json.dump(tw,open('tools/twins.json','w'),ensure_ascii=False,indent=1)
ty=json.load(open('tools/types.json'));ty[A['fr']['url']]='article';ty[A['en']['url']]='article';json.dump(ty,open('tools/types.json','w'),ensure_ascii=False,indent=1)
print('insight pages written')
