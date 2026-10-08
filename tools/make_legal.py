#!/usr/bin/env python3
import os,json,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from pagegen import shell,write
def page(eyebrow,h1,lede,body):
    return f'''<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</div>
<article class="page-body legal-doc">
{body}
</article>'''
FR_N='''<h2>Éditeur</h2>
<p>Site édité par TYROS GROUP LTD, société enregistrée en Angleterre et au Pays de Galles sous le numéro 16513376, siège social 61 Kensington Church Street, London W8 4BA, Royaume-Uni.</p>
<h2>Hébergement</h2>
<p>Hébergé via GitHub Pages (GitHub Inc.).</p>
<h2>Propriété intellectuelle</h2>
<p>L'ensemble des contenus est la propriété exclusive de TYROS GROUP LTD. Toute reproduction est interdite sans autorisation écrite préalable.</p>'''
EN_N='''<h2>Publisher</h2>
<p>This site is published by TYROS GROUP LTD, a company registered in England and Wales under number 16513376, registered office 61 Kensington Church Street, London W8 4BA, United Kingdom.</p>
<h2>Hosting</h2>
<p>Hosted via GitHub Pages (GitHub Inc.).</p>
<h2>Intellectual property</h2>
<p>All content is the exclusive property of TYROS GROUP LTD. Reproduction is prohibited without prior written permission.</p>'''
FR_P='''<h2>Données collectées : formulaires de demande</h2>
<p>Lorsque vous utilisez un formulaire du site (contact, recrutement, conseil, Tyros Academy, demande de programme), nous collectons uniquement ce que vous saisissez : nom, entreprise, adresse e-mail et message, ainsi que, selon le formulaire, le poste ou profil recherché, la localisation, l'échéance, le sujet, le nombre approximatif de participants, le format souhaité et la période envisagée. Nous enregistrons aussi la langue, la page d'origine, l'offre ou le programme concerné et la date de la demande, afin de traiter correctement votre demande.</p>
<p><strong>Finalité :</strong> répondre à votre demande et, pour une demande de programme, vous transmettre le programme une fois votre demande examinée.</p>
<p><strong>Destinataires :</strong> Tyros Group. Les demandes sont enregistrées et transmises par des outils Google Workspace (messagerie et tableur) utilisés par Tyros Group. Aucune donnée n'est vendue ni cédée à des tiers.</p>
<!-- DÉCISION REQUISE (voir design-system/DECISIONS-CONFIDENTIALITE.md) : durée de conservation des demandes envoyées par formulaire. Aucune durée n'a été arrêtée. -->
<h2>Données collectées : sessions Tyros Academy</h2>
<p>Dans le cadre d'une session de sensibilisation commanditée par votre employeur, nous collectons via un questionnaire en ligne : nom, prénom, adresse email professionnelle, entreprise, et les réponses au questionnaire associé.</p>
<p><strong>Finalité :</strong> établir une attestation nominative de participation et un relevé documentaire transmis à l'entreprise commanditaire, à des fins de suivi de sa démarche de sensibilisation.</p>
<p><strong>Destinataires :</strong> Tyros Group et l'entreprise ayant commandité la session. Ces données ne sont pas transmises à d'autres tiers.</p>
<p><strong>Durée de conservation :</strong> 3 ans à compter de la session, correspondant aux besoins de justification du suivi de formation.</p>
<h2>Vos droits (RGPD / UK GDPR)</h2>
<p>Accès, rectification, effacement, limitation et opposition sur l'ensemble de ces traitements. Contactez-nous via <a href="mailto:contact@tyros-group.com">contact@tyros-group.com</a> ; pour les données liées à une session Tyros Academy, vous pouvez également vous adresser à votre employeur.</p>'''
EN_P='''<h2>Data collected: request forms</h2>
<p>When you use a form on this site (contact, recruitment, consulting, Tyros Academy, programme request), we collect only what you enter: name, company, email address and message, and, depending on the form, the role or profile sought, location, timing, topic, approximate number of participants, preferred format and intended period. We also record the language, the page you came from, the offer or programme concerned and the date of the request, so that we can handle it properly.</p>
<p><strong>Purpose:</strong> to answer your request and, for a programme request, to send you the programme once your request has been reviewed.</p>
<p><strong>Recipients:</strong> Tyros Group. Requests are recorded and forwarded using Google Workspace tools (email and spreadsheet) operated by Tyros Group. No data is sold or passed on to third parties.</p>
<!-- DECISION REQUIRED (see design-system/DECISIONS-CONFIDENTIALITE.md): retention period for requests sent through the forms. No period has been decided. -->
<h2>Data collected: Tyros Academy sessions</h2>
<p>For an awareness session commissioned by your employer, we collect through an online questionnaire: first name, last name, work email address, company, and the answers to the related questionnaire.</p>
<p><strong>Purpose:</strong> to issue a named certificate of attendance and a documentary record sent to the commissioning company, in support of its awareness programme.</p>
<p><strong>Recipients:</strong> Tyros Group and the company that commissioned the session. This data is not passed on to any other third party.</p>
<p><strong>Retention:</strong> 3 years from the session, in line with the needs of training-record evidence.</p>
<h2>Your rights (GDPR / UK GDPR)</h2>
<p>Access, rectification, erasure, restriction and objection for all of these processing activities. Contact us at <a href="mailto:contact@tyros-group.com">contact@tyros-group.com</a>; for data linked to a Tyros Academy session, you may also contact your employer.</p>'''
D=[
 ('fr','/mentions-legales/','Mentions légales | Tyros Group','Mentions légales de Tyros Group Ltd, société enregistrée en Angleterre et au Pays de Galles.',page('Légal','Mentions légales.','',FR_N)),
 ('en','/en/legal-notice/','Legal notice | Tyros Group','Legal notice of Tyros Group Ltd, a company registered in England and Wales.',page('Legal','Legal notice.','',EN_N)),
 ('fr','/confidentialite/','Politique de confidentialité | Tyros Group','Politique de confidentialité de Tyros Group : données collectées par les formulaires et les sessions Tyros Academy, finalités, durées et droits.',page('Légal','Politique de confidentialité.','La confidentialité est au cœur de notre relation avec les dirigeants et institutions que nous accompagnons.',FR_P)),
 ('en','/en/privacy-policy/','Privacy policy | Tyros Group','Tyros Group privacy policy: data collected through forms and Tyros Academy sessions, purposes, retention and your rights.',page('Legal','Privacy policy.','Confidentiality is at the heart of our relationship with the executives and institutions we support.',EN_P)),
]
ty=json.load(open('tools/types.json'))
for lang,url,t,d,main in D:
    write(url,shell(lang,url,t,d,main));ty[url]='page'
json.dump(ty,open('tools/types.json','w'),indent=1)
print('legal pages written')
