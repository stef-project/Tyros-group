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
FR_P='''<h2>Données collectées : formulaire de contact</h2>
<p>Lorsque vous utilisez le formulaire de contact du site, nous collectons ce que vous saisissez : nom, adresse e-mail, entreprise (facultative), objet et message. Nous recevons aussi la langue, la page d'où vous écrivez, l'offre ou le programme concerné et la date de la demande, pour répondre correctement.</p>
<p><strong>Finalité :</strong> répondre à votre demande, y compris vous transmettre un programme sur demande. Le formulaire n'envoie aucun message automatique et n'enregistre aucune donnée dans une base ou un tableur.</p>
<p><strong>Destinataire :</strong> Tyros Group. Votre message arrive dans la messagerie de Tyros Group (Google Workspace). Aucune donnée n'est vendue ni cédée à des tiers.</p>
<p><strong>Durée de conservation :</strong> 24 mois après le dernier échange, puis suppression ou anonymisation, sauf relation contractuelle, obligation légale ou litige justifiant une conservation plus longue.</p>
<h2>Données collectées : sessions Tyros Academy</h2>
<p>Dans le cadre d'une session de sensibilisation commanditée par votre employeur, nous collectons via un questionnaire en ligne : nom, prénom, adresse email professionnelle, entreprise, et les réponses au questionnaire associé.</p>
<p><strong>Finalité :</strong> établir une attestation nominative de participation et un relevé documentaire transmis à l'entreprise commanditaire, à des fins de suivi de sa démarche de sensibilisation.</p>
<p><strong>Destinataires :</strong> Tyros Group et l'entreprise ayant commandité la session. Ces données ne sont pas transmises à d'autres tiers.</p>
<p><strong>Durée de conservation :</strong> 3 ans à compter de la session, correspondant aux besoins de justification du suivi de formation.</p>
<h2>Prestataires</h2>
<p><strong>Google</strong> (messagerie Google Workspace et Google Apps Script) reçoit et traite techniquement les messages envoyés par le formulaire, pour le compte de Tyros Group. <strong>GitHub</strong> (GitHub Pages) héberge le site et peut traiter des données techniques de connexion, comme l'adresse IP. <strong>Google Tag Manager</strong> n'est chargé qu'avec votre accord (voir ci-dessous). Ces prestataires peuvent traiter des données en dehors du Royaume-Uni et de l'Union européenne.</p>
<h2>Cookies et mesure d'audience</h2>
<p>Le site n'utilise aucun cookie nécessaire à un compte ou à un panier. Il enregistre seulement, dans votre navigateur, votre choix de consentement. Avec votre accord, Google Tag Manager est chargé et peut déposer des cookies de mesure d'audience. Vous pouvez refuser aussi simplement qu'accepter, et modifier votre choix à tout moment avec « Gérer les cookies » en bas de page.</p>
<h2>Vos droits (RGPD / UK GDPR)</h2>
<p>Accès, rectification, effacement, limitation et opposition sur l'ensemble de ces traitements. Contactez-nous via <a href="mailto:contact@tyros-group.com">contact@tyros-group.com</a> ; pour les données liées à une session Tyros Academy, vous pouvez également vous adresser à votre employeur.</p>'''
EN_P='''<h2>Data collected: contact form</h2>
<p>When you use the contact form on this site, we collect what you enter: name, email address, company (optional), subject and message. We also receive the language, the page you wrote from, the offer or programme concerned and the date of the request, so that we can reply properly.</p>
<p><strong>Purpose:</strong> to reply to your request, including sending you a programme on request. The form sends no automatic message and records no data in a database or spreadsheet.</p>
<p><strong>Recipient:</strong> Tyros Group. Your message arrives in the Tyros Group mailbox (Google Workspace). No data is sold or passed on to third parties.</p>
<p><strong>Retention:</strong> 24 months after the last exchange, then deletion or anonymisation, unless a contractual relationship, a legal obligation or a dispute justifies keeping it longer.</p>
<h2>Data collected: Tyros Academy sessions</h2>
<p>For an awareness session commissioned by your employer, we collect through an online questionnaire: first name, last name, work email address, company, and the answers to the related questionnaire.</p>
<p><strong>Purpose:</strong> to issue a named certificate of attendance and a documentary record sent to the commissioning company, in support of its awareness programme.</p>
<p><strong>Recipients:</strong> Tyros Group and the company that commissioned the session. This data is not passed on to any other third party.</p>
<p><strong>Retention:</strong> 3 years from the session, in line with the needs of training-record evidence.</p>
<h2>Service providers</h2>
<p><strong>Google</strong> (Google Workspace mail and Google Apps Script) receives and technically processes the messages sent through the form, on behalf of Tyros Group. <strong>GitHub</strong> (GitHub Pages) hosts the site and may process technical connection data, such as the IP address. <strong>Google Tag Manager</strong> is loaded only with your agreement (see below). These providers may process data outside the United Kingdom and the European Union.</p>
<h2>Cookies and audience measurement</h2>
<p>The site uses no cookie needed for an account or a basket. It only stores, in your browser, your consent choice. With your agreement, Google Tag Manager is loaded and may set audience-measurement cookies. You can refuse as easily as accept, and change your choice at any time with "Cookie settings" at the bottom of the page.</p>
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
