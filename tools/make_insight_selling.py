#!/usr/bin/env python3
"""Insights article: selling to financial institutions (FR + EN). Idempotent. Builds both pages from the structure of an existing article,
registers the twin pair, adds the card to both Insights hubs. Run tools/sync.py and tools/make_sitemap.py afterwards."""
import os,re,json
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'));os.chdir(ROOT)
SITE='https://tyros-group.com'
A={
'fr':dict(skel='insights/conformite-avantage-competitif/index.html',url='/insights/vendre-aux-institutions-financieres/',hub='/insights/',home_name='Accueil',
 title='Vendre aux institutions financières | Tyros Group',
 desc="Circuit de décision, agenda réglementaire, culture de la preuve : ce que les stratégies commerciales classiques ignorent des institutions financières.",
 h1='Vendre aux institutions financières&nbsp;: ce que les stratégies commerciales classiques ignorent',
 h1_plain='Vendre aux institutions financières : ce que les stratégies commerciales classiques ignorent',
 stand="Une banque ou un assureur n'achète pas comme une autre entreprise. Les approches qui fonctionnent ailleurs s'y heurtent à des circuits de décision, des exigences de diligence et une culture de la preuve qui leur sont propres.",
 cat='Market',kind='Perspective',date='Octobre 2026',iso='2026-10-16',ctalabel='Échanger sur un mandat privé',allbtn='← Tous les Insights',more='À lire également',
 req='/demande/',
 body='''<p>Une entreprise technologique, un cabinet de conseil ou un investisseur qui aborde une banque ou un assureur avec sa méthode habituelle (démonstration, période d'essai, volume de prospection) découvre vite que le rythme n'est pas le sien. Ce n'est pas de la lenteur gratuite. Dans ce secteur, une décision d'achat mal préparée engage la responsabilité de l'institution devant son superviseur.</p>
<h2>Un achat n'est pas une décision, c'est un circuit</h2>
<p>Dans une institution financière, le sponsor métier n'achète pas seul. Le risque, la conformité, la sécurité de l'information, les achats, le juridique et parfois l'audit interne ont chacun leur mot à dire, et chacun regarde un risque différent. Une stratégie commerciale qui ne s'adresse qu'au sponsor laisse sans réponse les objections les plus sérieuses.</p>
<p>Il faut donc cartographier le circuit (qui valide, qui peut bloquer, dans quel ordre) avant de choisir l'interlocuteur à rencontrer, et pas après.</p>
<h2>La réglementation fixe l'agenda</h2>
<p>Les priorités suivent souvent le calendrier réglementaire : résilience opérationnelle et maîtrise des prestataires tiers de technologies de l'information avec DORA dans l'Union, exigences comparables au Royaume-Uni, encadrement de l'intelligence artificielle. Une offre présentée comme une réponse à une obligation déjà identifiée en interne trouve plus facilement un sponsor qu'une offre présentée comme une innovation de plus.</p>
<p>La réglementation impose aussi des exigences au fournisseur : contrôle, audit, réversibilité, sous-traitance. Elles se préparent dans la proposition, pas une fois la discussion engagée.</p>
<div class="pull">Dans les services financiers, la bonne conversation précède la bonne offre.</div>
<h2>La preuve avant la promesse</h2>
<p>L'une des premières questions est presque toujours : « Qui d'autre l'utilise ? ». Pour un nouvel entrant, la réponse manque par définition. La preuve se construit donc autrement : un cadrage honnête de ce que l'offre fait et ne fait pas, une documentation prête pour la diligence, des échanges avec des pairs qui peuvent confirmer la pertinence du sujet.</p>
<p>Les promesses de gains chiffrés, difficiles à vérifier, desservent la crédibilité plus qu'elles ne la servent.</p>
<h2>Le même marché n'est jamais le même marché</h2>
<p>France, Royaume-Uni, Benelux, Suisse : les superviseurs, les calendriers, les langues et les habitudes d'achat diffèrent. Les mêmes mots (résilience, tiers critique, IA à haut risque) ne recouvrent ni les mêmes obligations ni les mêmes interlocuteurs d'un pays à l'autre. Une approche conçue pour un marché se transpose rarement telle quelle.</p>
<h2>Ce que cela change pour la démarche commerciale</h2>
<ul>
<li>Partir de l'agenda de l'interlocuteur (réglementaire, risque, transformation) avant de décrire l'offre.</li>
<li>Cartographier le circuit de décision et préparer une réponse pour chaque fonction qui valide.</li>
<li>Préparer la diligence avant qu'elle ne soit demandée.</li>
<li>Préférer quelques conversations de qualité à un volume d'approches.</li>
<li>Adapter la démarche marché par marché.</li>
</ul>
<p>C'est le terrain de <a href="/tyros-private/">Tyros Private</a> : identifier qui doit être autour de la table, et pourquoi, puis créer les conditions d'un dialogue, sans promesse de résultat.</p>
<p><em>Ce texte propose une analyse générale. Il ne constitue ni un conseil juridique ni un conseil réglementaire.</em></p>''',
 related=[('/insights/executive-search-vs-recrutement/','Leadership · Avril 2026',"Les dirigeants clés ne se cherchent pas en surface"),('/insights/conformite-avantage-competitif/','Market · Février 2026','La conformité : de centre de coût à avantage compétitif')],
 hub_d='Octobre 2026 · Perspective'),
'en':dict(skel='en/insights/compliance-as-a-competitive-advantage/index.html',url='/en/insights/selling-to-financial-institutions/',hub='/en/insights/',home_name='Home',
 title='Selling to financial institutions | Tyros Group',
 desc='Decision circuits, regulatory agenda, a culture of proof: what conventional commercial strategies overlook about financial institutions.',
 h1='Selling to financial institutions: what conventional commercial strategies overlook',
 h1_plain='Selling to financial institutions: what conventional commercial strategies overlook',
 stand="A bank or an insurer does not buy like any other company. Approaches that work elsewhere run into decision circuits, due-diligence requirements and a culture of proof that are specific to the sector.",
 cat='Market',kind='Perspective',date='October 2026',iso='2026-10-16',ctalabel='Discuss a private mandate',allbtn='← All Insights',more='Related reading',
 req='/en/request/',
 body='''<p>A technology company, an advisory firm or an investor approaching a bank or an insurer with its usual method (demonstration, trial period, volume of outreach) soon finds that the pace is not its own. It is not slowness for its own sake. In this sector, a poorly prepared purchasing decision engages the institution's responsibility before its supervisor.</p>
<h2>A purchase is not a decision, it is a circuit</h2>
<p>In a financial institution, the business sponsor does not buy alone. Risk, compliance, information security, procurement, legal and sometimes internal audit each have their say, and each looks at a different risk. A commercial strategy that addresses only the sponsor leaves the most serious objections unanswered.</p>
<p>The circuit (who validates, who can block, in what order) has to be mapped before choosing whom to meet, not afterwards.</p>
<h2>Regulation sets the agenda</h2>
<p>Priorities often follow the regulatory calendar: operational resilience and control of ICT third-party providers under DORA in the Union, comparable requirements in the United Kingdom, the framing of artificial intelligence. An offer presented as a response to an obligation already identified internally finds a sponsor more easily than one presented as one more innovation.</p>
<p>Regulation also places requirements on the supplier: oversight, audit, exit, subcontracting. These belong in the proposal, not once the discussion is under way.</p>
<div class="pull">In financial services, the right conversation comes before the right offer.</div>
<h2>Proof before promise</h2>
<p>One of the first questions is almost always: "Who else uses it?". For a new entrant, the answer is missing by definition. Proof has to be built differently: an honest framing of what the offer does and does not do, documentation ready for due diligence, exchanges with peers who can confirm the relevance of the subject.</p>
<p>Promises of quantified gains, hard to verify, damage credibility more than they build it.</p>
<h2>The same market is never the same market</h2>
<p>France, the United Kingdom, Benelux, Switzerland: supervisors, calendars, languages and purchasing habits differ. The same words (resilience, critical third party, high-risk AI) cover neither the same obligations nor the same counterparts from one country to the next. An approach designed for one market is rarely transferable as it stands.</p>
<h2>What this changes for the commercial approach</h2>
<ul>
<li>Start from the counterpart's agenda (regulatory, risk, transformation) before describing the offer.</li>
<li>Map the decision circuit and prepare an answer for each function that validates.</li>
<li>Prepare due diligence before it is requested.</li>
<li>Prefer a few high-quality conversations to a volume of approaches.</li>
<li>Adapt the approach market by market.</li>
</ul>
<p>This is the ground of <a href="/en/tyros-private/">Tyros Private</a>: identifying who should be in the room, and why, then creating the conditions for a dialogue, with no promise of outcome.</p>
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
    <a href="{c['req']}?offer=private-mandate&amp;from={c['url']}" class="btn btn-primary">{c['ctalabel']} <span class="ar">→</span></a>
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
