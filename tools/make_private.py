#!/usr/bin/env python3
"""Generates /tyros-private/ and /en/tyros-private/."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pagegen import shell,write
def ul(items): return '<ul>\n'+'\n'.join('<li>%s</li>'%i for i in items)+'\n</ul>'
P={
'fr':dict(url='/tyros-private/',home='/',req='/demande/',
 title='Tyros Private : rencontres exécutives sur mandat | Tyros Group',
 desc="Tyros conçoit et organise, sur mandat, des rencontres exécutives confidentielles : introductions, déjeuners et dîners privés, tables rondes, accès à de nouveaux marchés.",
 eyebrow='Tyros Private',h1='Les bonnes conversations. Les bons décideurs. Le bon cadre.',
 lede="Tyros conçoit et organise des rencontres exécutives confidentielles pour les organisations souhaitant présenter une innovation, explorer un marché ou développer des relations stratégiques de haut niveau.",
 secs=[
 ('','Pour les organisations qui veulent rencontrer les bons décideurs',
  ["Une entreprise technologique, une FinTech, un investisseur, un prestataire de services ou un cabinet peut mandater Tyros pour concevoir et organiser des rencontres avec des décideurs ciblés : présenter une innovation, explorer une opportunité commerciale, développer un réseau.",
   "Nous ne vendons ni des repas ni un accès à des personnes. Nous apportons une expertise qui crée les conditions d'un dialogue stratégique avec des interlocuteurs pertinents. Vous n'avez pas besoin d'être membre pour nous mandater."],None),
 ('introductions','Private Executive Introductions',
  ["Identification, qualification et mise en relation confidentielle de dirigeants, d'investisseurs et de décideurs C-level."],
  ['Rencontres bilatérales','Introductions ciblées','Rendez-vous stratégiques']),
 ('events','Executive Private Events',
  ["Sur mandat, nous concevons et organisons des rencontres pour présenter une innovation, explorer une opportunité commerciale, développer un réseau ou échanger avec des décideurs sélectionnés."],
  ['Executive Private Lunches','Private Executive Dinners','Strategic Roundtables','Rencontres sectorielles sur invitation']),
 ('example',"Un exemple d'illustration",
  ["À titre d'illustration, et non comme référence : une entreprise technologique américaine souhaite développer son activité auprès des banques françaises. Elle mandate Tyros pour organiser un déjeuner privé réunissant un petit nombre de décideurs qualifiés autour d'une thématique sectorielle pertinente. L'objectif est de créer les conditions d'un dialogue stratégique et de lui permettre de présenter son expertise, sa technologie ou ses services dans un cadre privilégié."],None),
 ('market-access','Strategic Market Access',
  ["Pour les entreprises qui souhaitent accéder à de nouveaux marchés, notamment en France et au Royaume-Uni, ainsi qu'à l'international. Le périmètre géographique est défini avec vous pour chaque mandat."],
  ['Identification des interlocuteurs stratégiques','Qualification des opportunités','Introductions','Organisation de rencontres professionnelles']),
 ('method','Notre valeur ajoutée',
  ["Un mandat Tyros Private repose sur six étapes."],
  ['<strong>Cadrage stratégique</strong> : objectif, thématique et résultat attendu.','<strong>Qualification des interlocuteurs</strong> : définition du public cible.','<strong>Conception du format</strong> : déjeuner, dîner, table ronde ou rencontres individuelles.','<strong>Invitations</strong> : recherche des participants et invitations.','<strong>Organisation</strong> : lieu, déroulé et accueil.','<strong>Suivi</strong> : prolongement des échanges utiles.']),
 ('transparence','Transparence et cadre',
  [],
  ["L'identité du mandataire et la finalité de la rencontre sont communiquées aux invités.","Aucune participation individuelle n'est garantie ni vendue : chaque invité est libre de venir.","Chaque mandat est cadré sur mesure, dans la confidentialité."]),
 ('membership','Tyros Private et Membership',
  ["Tyros Private est une prestation sur mandat, distincte du Membership, qui est un abonnement continu. Les membres Enterprise peuvent être invités de façon sélective aux rencontres Tyros Private, sous réserve de pertinence, de disponibilité et de l'accord des organisateurs. Aucune invitation n'est automatique."],None)],
 b1='Organiser une rencontre privée',b2="Discuter d'un mandat stratégique",see='Voir aussi',
 seel=[('/for-boards-executives/','Conseils & dirigeants'),('/executive-search-banque-assurance/','Executive search banque & assurance'),('/insights/','Insights')],crumb='Tyros Private'),
'en':dict(url='/en/tyros-private/',home='/en/',req='/en/request/',
 title='Tyros Private: confidential executive encounters | Tyros Group',
 desc='Tyros designs and facilitates, on mandate, confidential executive encounters: introductions, private lunches and dinners, roundtables, access to new markets.',
 eyebrow='Tyros Private',h1='The right conversations. The right people. The right setting.',
 lede='We design and facilitate confidential executive encounters for organisations seeking to engage senior decision-makers, introduce innovative solutions, explore new markets and build strategic relationships.',
 secs=[
 ('','For organisations that want to meet the right decision-makers',
  ["A technology company, a FinTech, an investor, a service provider or a firm can mandate Tyros to design and run meetings with targeted decision-makers: to present an innovation, explore a commercial opportunity or build a network.",
   "We do not sell meals or access to people. We bring the expertise that creates the conditions for a strategic dialogue with relevant counterparts. You do not need to be a member to mandate us."],None),
 ('introductions','Private Executive Introductions',
  ['Identification, qualification and confidential introduction of executives, investors and C-level decision-makers.'],
  ['Bilateral meetings','Targeted introductions','Strategic appointments']),
 ('events','Executive Private Events',
  ['On mandate, we design and run meetings to present an innovation, explore a commercial opportunity, build a network or exchange with selected decision-makers.'],
  ['Executive Private Lunches','Private Executive Dinners','Strategic Roundtables','Invitation-only sector meetings']),
 ('example','An illustrative example',
  ['By way of illustration, not as a reference: a US technology company wants to grow its business with French banks. It mandates Tyros to organise a private lunch bringing together a small number of qualified decision-makers around a relevant sector theme. The aim is to create the conditions for a strategic dialogue and let the company present its expertise, technology or services in a privileged setting.'],None),
 ('market-access','Strategic Market Access',
  ['For companies seeking access to new markets, including France and the United Kingdom, and internationally. The geographic scope is defined with you for each mandate.'],
  ['Identifying strategic counterparts','Qualifying opportunities','Introductions','Organising professional meetings']),
 ('method','Our added value',
  ['A Tyros Private mandate rests on six steps.'],
  ['<strong>Strategic framing</strong>: objective, theme and expected outcome.','<strong>Qualifying counterparts</strong>: defining the target audience.','<strong>Designing the format</strong>: lunch, dinner, roundtable or one-to-one meetings.','<strong>Invitations</strong>: participant search and invitations.','<strong>Organisation</strong>: venue, running order and welcome.','<strong>Follow-up</strong>: carrying useful exchanges forward.']),
 ('transparency','Transparency and framework',
  [],
  ["The identity of the mandating party and the purpose of the meeting are disclosed to invited guests.","No individual attendance is guaranteed or sold: every guest is free to come.","Each mandate is scoped individually, in confidence."]),
 ('membership','Tyros Private and Membership',
  ['Tyros Private is a mandated service, separate from Membership, which is an ongoing subscription. Enterprise members may be invited selectively to Tyros Private meetings, subject to relevance, availability and the organisers\' agreement. No invitation is automatic.'],None)],
 b1='Commission a Private Executive Event',b2='Discuss a Strategic Mandate',see='See also',
 seel=[('/en/for-boards-executives/','Boards & Executives'),('/en/executive-search-banking-insurance/','Executive search for banking & insurance'),('/en/insights/','Insights')],crumb='Tyros Private'),
}
import json
for lang,c in P.items():
    body=[]
    for anc,h,paras,items in c['secs']:
        idattr=' id="%s"'%anc if anc else ''
        body.append('<h2%s>%s</h2>'%(idattr,h))
        for p in paras: body.append('<p>%s</p>'%p)
        if items: body.append(ul(items))
    q=lambda o:'%s?offer=%s&amp;from=%s'%(c['req'],o,c['url'])
    main=f'''<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">{c['eyebrow']}</div>
    <h1>{c['h1']}</h1>
    <p class="lede">{c['lede']}</p>
  </div>
</div>
<article class="page-body">
{chr(10).join(body)}
<div class="page-cta">
  <a href="{q('private-event')}" class="btn btn-primary">{c['b1']}</a>
  <a href="{q('private-mandate')}" class="btn btn-ghost">{c['b2']}</a>
</div>
</article>
<div class="see-also">
  <div class="see-also-inner">
    <h2>{c['see']}</h2>
    {chr(10).join('<a href="%s">%s</a>'%(u,t.replace('&','&amp;')) for u,t in c['seel'])}
  </div>
</div>'''
    h=shell(lang,c['url'],c['title'].replace('&','&amp;'),c['desc'],main)
    h=h.replace('"inLanguage": "%s"'%lang,'"inLanguage": "%s"'%lang)
    write(c['url'],h)
print('private pages written')
