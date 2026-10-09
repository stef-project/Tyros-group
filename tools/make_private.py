#!/usr/bin/env python3
"""Tyros Private: generates /tyros-private/ and /en/tyros-private/, and rewrites the Tyros Private block of both homes
(divisions card 04 + section #private). Idempotent. Run tools/sync.py afterwards."""
import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pagegen import shell,write
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
E=lambda x:x.replace('&','&amp;')
def ul(items): return '<ul>\n'+'\n'.join('<li>%s</li>'%i for i in items)+'\n</ul>'

P={
'fr':dict(url='/tyros-private/',home='/',req='/demande/',homefile='index.html',
 title='Tyros Private : accès exécutif et rencontres | Tyros Group',
 desc="Sur mandat, Tyros conçoit des rencontres privées avec des décideurs qualifiés : introductions, déjeuners, tables rondes, accès marché. Tous secteurs.",
 eyebrow='Tyros Private · Strategic Market Access',
 h1="L'accès ne se résume pas à un carnet d'adresses.",
 lede="Il consiste à savoir qui doit être autour de la table, et pourquoi. Dans le cadre de Strategic Market Access, une organisation peut mandater Tyros pour concevoir une rencontre privée sur mesure, ouvrir un dialogue stratégique et introduire une innovation, une technologie ou un nouveau service auprès de décideurs qualifiés.",
 secs=[
 ('mandat',"Un mandat, pas un événement",
  ["Tyros n'est ni une agence événementielle ni un annuaire de dirigeants. Vous nous confiez un objectif commercial ou stratégique ; nous réunissons les éléments qui permettent d'y répondre : connaissance du marché, définition de l'audience, accès aux décideurs, curation, animation et suivi.",
   "Le mandat est ponctuel et conçu sur mesure."],None),
 ('introduction','Private Executive Introduction',
  ["<strong>Une rencontre ciblée, avec l'interlocuteur pertinent.</strong> Lorsque l'objectif est clair et que le décideur est identifiable, Tyros le qualifie, présente votre organisation et prépare l'échange, en tête-à-tête ou en très petit comité. L'introduction est confidentielle et professionnelle : le décideur sait qui vous êtes et pourquoi vous souhaitez le rencontrer."],
  ["Découvrir un secteur ou une organisation","Éprouver une proposition de valeur auprès d'un utilisateur ou d'un acheteur potentiel","Établir une première connexion avec un écosystème","Rencontrer un futur partenaire ou investisseur"],'private-intro',"Échanger sur une introduction"),
 ('lunch','Executive Private Lunch',
  ["<strong>Un petit comité de décideurs, autour d'un sujet qui compte pour eux.</strong> Un déjeuner à huis clos, généralement de six à dix participants selon le mandat, centré sur une thématique sectorielle pertinente pour les invités. Le partenaire est identifié auprès des invités et la finalité de la rencontre est transparente. C'est un échange stratégique curaté, pas une démonstration commerciale : la conversation reste celle des participants.",
   "Une entreprise mandate Tyros pour concevoir une rencontre privée autour d'un objectif ou d'un enjeu stratégique et créer un dialogue avec une audience qualifiée autour d'une technologie, d'une innovation, d'un service ou d'une problématique de marché. Il s'agit d'une mission ponctuelle, qui comprend :"],
  ["le cadrage de la problématique et de l'audience visée","l'identification des profils","les invitations","la coordination de la rencontre","le suivi"],'private-lunch',"Échanger sur ce format"),
 ('roundtable','Strategic Executive Roundtable',
  ["<strong>Un groupe de dirigeants, une discussion de fond.</strong> Une table ronde, généralement de huit à douze participants selon le mandat, animée par Tyros sur un enjeu stratégique : intelligence artificielle et gouvernance de l'IA, DORA et résilience opérationnelle, cybersécurité, transformation bancaire ou assurantielle, paiements, conformité, nouveaux modèles de distribution, expansion internationale.",
   "La qualité de la discussion prime. Ce n'est ni un argumentaire commercial déguisé ni une conférence : la valeur du mandataire tient à la pertinence de la question posée et à la crédibilité de son point de vue."],
  None,'private-roundtable',"Échanger sur ce format"),
 ('market-entry','Market Entry Executive Programme',
  ["<strong>Un accompagnement sur plusieurs semaines pour avancer sur un marché.</strong> Le programme décline Strategic Market Access : entrer sur un nouveau marché, ou développer son activité commerciale sur un marché existant. Une organisation peut nous mandater pour introduire une nouvelle technologie, lancer un service, rencontrer des clients potentiels, nouer des partenariats stratégiques ou accélérer là où elle est déjà présente.",
   "Le programme combine cartographie du marché et des parties prenantes, qualification, introductions ciblées, un déjeuner ou une table ronde lorsque c'est pertinent, accompagnement et suivi. Marchés couverts : France, Royaume-Uni, Benelux, Suisse et Europe. Durée et périmètre sont définis pour chaque mandat."],
  ["Introduire une nouvelle technologie","Lancer un service","Rencontrer des clients potentiels","Développer des partenariats stratégiques","Accélérer sur un marché existant","S'implanter dans un nouveau pays"],'private-mandate',"Échanger sur un mandat privé"),
 ('methode','Une méthode, quatre formats',
  ["Les quatre prestations sont complémentaires et reposent sur le même fil en sept étapes. Leur ampleur varie : une introduction en mobilise le cœur, le Market Entry Programme les déroule toutes."],
  ["<strong>Comprendre l'objectif</strong> : ce que vous voulez faire avancer, et auprès de qui.","<strong>Cartographier</strong> les décideurs et les organisations pertinentes.","<strong>Identifier et approcher</strong> les profils, en précisant qui nous mandate.","<strong>Qualifier l'intérêt</strong> autour d'un sujet crédible pour eux.","<strong>Concevoir le format</strong> : introduction, déjeuner, table ronde ou programme.","<strong>Organiser et animer</strong> la rencontre.","<strong>Accompagner</strong> les mises en relation et le suivi."]),
 ('secteurs','Tous secteurs',
  ["Les services financiers sont notre terrain d'expérience le plus naturel : banques, assurances, gestion d'actifs, paiements. Le mandat s'adresse aussi à toute organisation B2B : technologie, intelligence artificielle, cybersécurité, santé, industrie, investissement, conseil.",
   "Nous évaluons la faisabilité et la pertinence de chaque mandat avant son acceptation."],None),
 ('exemples',"Des situations types",
  ["À titre d'illustration, et non comme références :"],
  ["une FinTech américaine qui souhaite aborder le marché bancaire français ;","un éditeur de cybersécurité qui cherche le dialogue avec des directions des risques et de l'informatique autour d'une nouvelle solution ;","un éditeur RegTech qui lance une offre de conformité ;","un investisseur qui explore un écosystème sectoriel ;","un prestataire technologique qui cherche le dialogue avec des assureurs ;","une entreprise qui prépare son arrivée sur un nouveau marché européen."]),
 ('transparence','Transparence et cadre',
  [],
  ["L'identité du mandataire et la finalité de la rencontre sont communiquées à chaque invité : aucun faux prétexte.","Aucune présence d'un dirigeant, aucun nombre de contacts et aucun contrat ne sont garantis ni vendus. Chaque invité est libre de venir.","Les coordonnées individuelles d'un invité ne sont transmises au mandataire qu'avec son accord préalable. Un retour anonymisé ou agrégé (synthèse des échanges, tendances) peut lui être restitué.","Les formats tiennent compte des politiques d'hospitalité et de conformité des organisations invitées.","Les données professionnelles des invités sont traitées comme indiqué dans la <a href=\"/confidentialite/\">politique de confidentialité</a>.","Les tarifs sont communiqués sur demande, après cadrage du mandat."]),
],
 cta='Échanger sur un mandat privé',cta2='Voir Tyros Intelligence',cta2u='/#intelligence',see='Voir aussi',
 seel=[('/for-boards-executives/','Conseils & dirigeants'),('/executive-search-banque-assurance/','Executive search banque & assurance'),('/insights/','Insights')],
 hp=dict(
  card=('Des rencontres privées, sur mandat.',"Ouvrez un dialogue stratégique autour d'une innovation, d'une technologie ou d'un service avec des interlocuteurs qualifiés, dans un cadre conçu sur mesure par Tyros."),
  eyebrow='Tyros Private',h2='Les bonnes conversations. Les bons décideurs. Le bon cadre.',
  p="Dans le cadre de Strategic Market Access, une organisation peut mandater Tyros pour concevoir une rencontre privée sur mesure, ouvrir un dialogue stratégique et introduire une innovation, une technologie ou un nouveau service auprès de décideurs qualifiés. Tous secteurs, des services financiers à la technologie, l'IA, la cybersécurité, la santé ou l'industrie.",
  rows=[('Private Executive Introduction','Une introduction ciblée et confidentielle.',"Une rencontre avec l'interlocuteur pertinent, qualifiée et préparée par Tyros.",'introduction'),
        ('Executive Private Lunch','Un déjeuner à huis clos, autour d\'un enjeu.','Un petit comité de décideurs réunis sur une thématique sectorielle, partenaire clairement identifié.','lunch'),
        ('Strategic Executive Roundtable','Une discussion de fond entre dirigeants.',"Un groupe de dirigeants autour d'un enjeu stratégique : IA, DORA, cybersécurité, transformation, expansion.",'roundtable'),
        ('Market Entry Executive Programme','Avancer sur un marché, de la cartographie au suivi.','Introduire une technologie, lancer un service, rencontrer des clients, nouer des partenariats : un accompagnement sur plusieurs semaines.','market-entry')],
  note="Une organisation peut nous mandater pour une mission ponctuelle. Le mandataire et la finalité de chaque rencontre sont annoncés aux invités, et la présence d'un dirigeant n'est jamais garantie.",
  b1='Échanger sur un mandat privé',b2='Découvrir Tyros Private')),
'en':dict(url='/en/tyros-private/',home='/en/',req='/en/request/',homefile='en/index.html',
 title='Tyros Private: executive access & encounters | Tyros Group',
 desc='On mandate, Tyros designs private meetings with qualified decision-makers: introductions, lunches, roundtables and market entry. All sectors.',
 eyebrow='Tyros Private · Strategic Market Access',
 h1='Access is not a contact list.',
 lede='It is knowing who should be in the room, and why. Through Strategic Market Access, an organisation can mandate Tyros to design a bespoke private meeting, open a strategic dialogue and introduce an innovation, a technology or a new service to qualified decision-makers.',
 secs=[
 ('mandate','A mandate, not an event',
  ['Tyros is neither an events agency nor a directory of executives. You give us a commercial or strategic objective; we bring together what it takes to meet it: market knowledge, audience design, access to decision-makers, curation, facilitation and follow-up.',
   'The mandate is one-off and bespoke.'],None),
 ('introduction','Private Executive Introduction',
  ['<strong>A targeted meeting with the right counterpart.</strong> When the objective is clear and the decision-maker can be identified, Tyros qualifies them, presents your organisation and prepares the conversation, one-to-one or in a very small group. The introduction is confidential and professional: the decision-maker knows who you are and why you wish to meet.'],
  ['Discover a sector or an organisation','Test a value proposition with a potential user or buyer','Make a first connection with an ecosystem','Meet a future partner or investor'],'private-intro','Discuss an introduction'),
 ('lunch','Executive Private Lunch',
  ['<strong>A small group of decision-makers around a subject that matters to them.</strong> A closed-door lunch, generally six to ten participants depending on the mandate, built around a sector theme relevant to the guests. The partner is identified to the guests and the purpose of the meeting is transparent. It is a curated strategic exchange, not a commercial demonstration: the conversation remains the participants\'.',
   'A company mandates Tyros to design a private meeting around a strategic objective or issue and create a dialogue with a qualified audience around a technology, an innovation, a service or a market question. It is a one-off assignment, which includes:'],
  ['framing the issue and the target audience','identifying the profiles','the invitations','coordinating the meeting','follow-up'],'private-lunch','Discuss this format'),
 ('roundtable','Strategic Executive Roundtable',
  ['<strong>A group of senior leaders, a discussion of substance.</strong> A roundtable, generally eight to twelve participants depending on the mandate, chaired by Tyros on a strategic issue: artificial intelligence and AI governance, DORA and operational resilience, cybersecurity, banking or insurance transformation, payments, compliance, new distribution models, international expansion.',
   'The quality of the discussion comes first. It is neither a disguised sales pitch nor a conference: the mandating party\'s value lies in the relevance of the question it raises and the credibility of its point of view.'],
  None,'private-roundtable','Discuss this format'),
 ('market-entry','Market Entry Executive Programme',
  ['<strong>A multi-week engagement to make progress in a market.</strong> The programme is the multi-week form of Strategic Market Access: entering a new market, or developing commercial activity in an existing one. An organisation can mandate us to introduce a new technology, launch a service, meet potential clients, build strategic partnerships or accelerate where it is already present.',
   'The programme combines market and stakeholder mapping, qualification, targeted introductions, a lunch or roundtable where relevant, accompaniment and follow-up. Markets covered: France, the United Kingdom, Benelux, Switzerland and Europe. Duration and scope are defined for each mandate.'],
  ['Introduce a new technology','Launch a service','Meet potential clients','Build strategic partnerships','Accelerate in an existing market','Enter a new country'],'private-mandate','Discuss a private mandate'),
 ('method','One method, four formats',
  ['The four services are complementary and rest on the same seven-step thread. Their scale varies: an introduction uses the core of it, the Market Entry Programme runs through every step.'],
  ['<strong>Understand the objective</strong>: what you want to move forward, and with whom.','<strong>Map</strong> the relevant decision-makers and organisations.','<strong>Identify and approach</strong> the profiles, stating who has mandated us.','<strong>Qualify interest</strong> around a topic that is credible for them.','<strong>Design the format</strong>: introduction, lunch, roundtable or programme.','<strong>Organise and facilitate</strong> the meeting.','<strong>Accompany</strong> the introductions and the follow-up.']),
 ('sectors','All sectors',
  ['Financial services are our most natural field of experience: banks, insurers, asset managers, payments. The mandate is also open to any B2B organisation: technology, artificial intelligence, cybersecurity, healthcare, industry, investment, advisory.',
   'We assess the feasibility and relevance of each mandate before accepting it.'],None),
 ('examples','Typical situations',
  ['By way of illustration, not as references:'],
  ['a US FinTech wishing to approach the French banking market;','a cybersecurity vendor seeking dialogue with risk and technology leaders around a new solution;','a RegTech launching a compliance offer;','an investor exploring a sector ecosystem;','a technology provider seeking dialogue with insurers;','a company preparing its arrival in a new European market.']),
 ('transparency','Transparency and framework',
  [],
  ['The identity of the mandating party and the purpose of the meeting are disclosed to every guest: no false pretext.','No executive\'s attendance, number of contacts or contract is guaranteed or sold. Every guest is free to come.','An individual guest\'s contact details are passed to the mandating party only with that guest\'s prior agreement. Anonymised or aggregated feedback (a summary of the discussion, emerging trends) may be provided to it.','Formats take into account the hospitality and compliance policies of the invited organisations.','Guests\' professional data is handled as set out in the <a href="/en/privacy-policy/">privacy policy</a>.','Fees are provided on request, once the mandate has been scoped.']),
],
 cta='Discuss a private mandate',cta2='See Tyros Intelligence',cta2u='/en/#intelligence',see='See also',
 seel=[('/en/for-boards-executives/','Boards & Executives'),('/en/executive-search-banking-insurance/','Executive search for banking & insurance'),('/en/insights/','Insights')],
 hp=dict(
  card=('Private meetings, on mandate.','Open a strategic dialogue around an innovation, a technology or a service with qualified counterparts, in a setting Tyros designs around you.'),
  eyebrow='Tyros Private',h2='The right conversations. The right people. The right setting.',
  p='Through Strategic Market Access, an organisation can mandate Tyros to design a bespoke private meeting, open a strategic dialogue and introduce an innovation, a technology or a new service to qualified decision-makers. All sectors, from financial services to technology, AI, cybersecurity, healthcare and industry.',
  rows=[('Private Executive Introduction','A targeted, confidential introduction.','A meeting with the right counterpart, qualified and prepared by Tyros.','introduction'),
        ('Executive Private Lunch','A closed-door lunch around one issue.','A small group of decision-makers on a sector theme, with the partner clearly identified.','lunch'),
        ('Strategic Executive Roundtable','A discussion of substance among senior leaders.','A group of senior leaders around a strategic issue: AI, DORA, cybersecurity, transformation, expansion.','roundtable'),
        ('Market Entry Executive Programme','Move forward in a market, from mapping to follow-up.','Introduce a technology, launch a service, meet clients, build partnerships: a multi-week engagement.','market-entry')],
  note="An organisation can mandate us for a one-off assignment. The mandating party and the purpose of every meeting are stated to guests, and no executive's attendance is ever guaranteed.",
  b1='Discuss a private mandate',b2='Discover Tyros Private')),
}
for lang,c in P.items():
    body=[]
    for sec in c['secs']:
        anc,h,paras,items=sec[:4]
        body.append('<h2 id="%s">%s</h2>'%(anc,h))
        for p in paras: body.append('<p>%s</p>'%p)
        if items: body.append(ul(items))
        if len(sec)>4:
            body.append('<p><a href="%s?offer=%s&amp;from=%s">%s</a></p>'%(c['req'],sec[4],c['url'],sec[5]))
    q=lambda o:'%s?offer=%s&amp;from=%s'%(c['req'],o,c['url'])
    main=f'''<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">{E(c['eyebrow'])}</div>
    <h1>{E(c['h1'])}</h1>
    <p class="lede">{E(c['lede'])}</p>
  </div>
</div>
<article class="page-body">
{chr(10).join(body)}
<div class="page-cta">
  <a href="{q('private-mandate')}" class="btn btn-primary">{E(c['cta'])}</a>
  <a href="{c['cta2u']}" class="btn btn-ghost">{E(c['cta2'])}</a>
</div>
</article>
<div class="see-also">
  <div class="see-also-inner">
    <h2>{c['see']}</h2>
    {chr(10).join('<a href="%s">%s</a>'%(u,E(t)) for u,t in c['seel'])}
  </div>
</div>'''
    write(c['url'],shell(lang,c['url'],E(c['title']),E(c['desc']),main))
    # ---- home
    hm=c['hp'];f=os.path.join(ROOT,c['homefile']);s=open(f,encoding='utf-8').read()
    qh=lambda o:'%s?offer=%s&amp;from=%s'%(c['req'],o,c['home'])
    a=s.index('id="private-access"');a=s.rfind('<a class="divi"',0,a);b=s.index('</a>',a)+4
    s=s[:a]+('<a class="divi" href="%s" id="private-access">\n        <div class="dnum">04</div>\n        <div><div class="dtag">Tyros Private</div><h3>%s</h3><p>%s</p></div>\n        <div class="darr">→</div>\n      </a>'%(c['url'],E(hm['card'][0]),E(hm['card'][1])))+s[b:]
    rows=''.join('      <a class="divi" href="%s#%s">\n        <div class="dnum">%02d</div>\n        <div><div class="dtag">%s</div><h3>%s</h3><p>%s</p></div>\n        <div class="darr">→</div>\n      </a>\n'%(c['url'],anc,i+1,E(t),E(h),E(d)) for i,(t,h,d,anc) in enumerate(hm['rows']))
    sec=('<!-- TYROS PRIVATE -->\n<section class="sec" id="private">\n  <div class="wrap">\n    <div class="sec-head">\n      <div class="eyebrow">%s</div>\n      <h2>%s</h2>\n      <p>%s</p>\n    </div>\n    <div class="divs">\n%s    </div>\n    <p class="private-note">%s</p>\n    <div class="private-cta">\n      <a href="%s" class="btn btn-primary">%s</a>\n      <a href="%s" class="btn btn-ghost">%s</a>\n    </div>\n  </div>\n</section>\n\n'%(hm['eyebrow'],E(hm['h2']),E(hm['p']),rows,E(hm['note']),qh('private-mandate'),E(hm['b1']),c['url'],E(hm['b2'])))
    a=s.index('<!-- TYROS PRIVATE -->');b=s.index('<!-- INSIGHTS -->')
    s=s[:a]+sec+s[b:]
    open(f,'w',encoding='utf-8').write(s)
print('private pages + home blocks written')
