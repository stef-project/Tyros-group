"""One contact form for the whole site (FR and EN). Subject is prefilled from the offer or programme that opened it."""
import json,html
E=lambda x:html.escape(x,quote=True)
# offer id -> (kind, FR label, EN label); kind decides the subject prefix
OFFERS={
 'cro':('recruitment','Chief Risk Officer','Chief Risk Officer'),
 'cco':('recruitment','Chief Compliance Officer','Chief Compliance Officer'),
 'banking-insurance':('recruitment','Executive search banque & assurance','Executive search for banking & insurance'),
 'actuarial':('recruitment','Executive search actuariat','Executive search for actuarial roles'),
 'executive-search':('recruitment','Tyros Executive Search','Tyros Executive Search'),
 'ai-act':('consulting',"AI Act & gouvernance de l'IA",'AI Act & AI governance'),
 'advisory':('consulting','Tyros Advisory','Tyros Advisory'),
 'compliance':('consulting','Conformité et avantage compétitif','Compliance as a competitive advantage'),
 'boards':('plain','Conseils & dirigeants','Boards & Executives'),
 'membership-essential':('plain','Membership Essential','Membership Essential'),
 'membership-professional':('plain','Membership Professional','Membership Professional'),
 'membership-enterprise':('plain','Membership Enterprise','Membership Enterprise'),
 'briefing':('plain',"Briefing d'intelligence confidentiel",'Confidential intelligence briefing'),
 'private-mandate':('plain','Tyros Private — Mandat d\'accès marché','Tyros Private — Market Entry Mandate'),
 'private-lunch':('plain','Tyros Private — Executive Private Lunch','Tyros Private — Executive Private Lunch'),
 'private-roundtable':('plain','Tyros Private — Strategic Roundtable','Tyros Private — Strategic Roundtable'),
 'private-intro':('plain','Tyros Private — Introduction stratégique','Tyros Private — Strategic Introduction'),
 'intel-market':('plain','Intelligence de marché et concurrentielle','Market & Competitive Intelligence'),
 'intel-mapping':('plain','Cartographie des talents et des dirigeants','Talent & Leadership Mapping'),
 'intel-comp':('plain','Benchmarks de rémunération','Compensation Benchmarks'),
 'intel-reg':('plain','Analyses sectorielles et réglementaires','Sector & Regulatory Analyses'),
 'dora-awareness':('academy','DORA Awareness','DORA Awareness'),
 'ai-literacy':('academy','AI Literacy & Responsible Use','AI Literacy & Responsible Use'),
 'manager-recruiter':('academy','Manager as Recruiter','Manager as Recruiter'),
 'specialist-talent':('academy','Hiring & Retaining Specialist Talent','Hiring & Retaining Specialist Talent'),
 'business-development':('academy','Business Development in Financial Services','Business Development in Financial Services'),
 'client-relationships':('academy','Strategic Client Relationships','Strategic Client Relationships'),
}
T={
'fr':dict(h1='Échange confidentiel.',lede='Dites-nous ce qui compte. Votre message arrive directement chez Tyros, qui vous répond personnellement sous 48 h ouvrées.',
 f=dict(name='Nom',email='Email',company='Entreprise (facultatif)',subject='Objet',message='Message'),
 default_subject='Échange confidentiel',
 prefix=dict(recruitment='Recrutement',consulting='Conseil',academy='Tyros Academy',programme='Demande de programme',session='Organisation d\'une session'),
 send='Envoyer',sending='Envoi en cours…',
 privacy='En envoyant ce formulaire, vous acceptez que Tyros Group traite votre demande pour y répondre.',privacy_link='Politique de confidentialité',privacy_url='/confidentialite/',
 err_required='Merci de renseigner ce champ.',err_email='Merci de saisir une adresse e-mail valide.',
 err_send='L\'envoi n\'a pas abouti. Merci de réessayer dans un instant ou d\'écrire à contact@tyros-group.com.',
 ok_h='Merci, votre demande est bien arrivée.',ok_p='Elle a bien été reçue par Tyros Group. Nous vous répondons personnellement sous 48 h ouvrées.',
 ok_back='Retour à l\'accueil',ok_home='/',
 noscript='Ce formulaire nécessite JavaScript. Vous pouvez aussi nous écrire à contact@tyros-group.com.'),
'en':dict(h1='A confidential conversation.',lede='Tell us what matters. Your message goes straight to Tyros, who will reply personally within 48 working hours.',
 f=dict(name='Name',email='Email',company='Company (optional)',subject='Subject',message='Message'),
 default_subject='Confidential discussion',
 prefix=dict(recruitment='Recruitment',consulting='Consulting',academy='Tyros Academy',programme='Programme request',session='Session request'),
 send='Send',sending='Sending…',
 privacy='By sending this form, you agree that Tyros Group will process your request in order to reply to it.',privacy_link='Privacy policy',privacy_url='/en/privacy-policy/',
 err_required='Please fill in this field.',err_email='Please enter a valid email address.',
 err_send='We could not send your request. Please try again in a moment or write to contact@tyros-group.com.',
 ok_h='Thank you, your request has arrived.',ok_p='It has been received by Tyros Group. We will reply personally within 48 working hours.',
 ok_back='Back to the home page',ok_home='/en/',
 noscript='This form needs JavaScript. You can also write to us at contact@tyros-group.com.'),
}
def _f(id_,label,kind='text',req=True,ac=None,extra=''):
    a=f' autocomplete="{ac}"' if ac else ''
    r=' required aria-required="true"' if req else ''
    return f'<div class="fld"><label for="{id_}">{E(label)}</label><input id="{id_}" name="{id_.split("__")[-1]}" type="{kind}"{r}{a}{extra}><span class="fld-err" role="alert"></span></div>'
def form(lang,uid):
    t=T[lang];f=t['f'];p=lambda n:'%s__%s'%(uid,n)
    rows=[_f(p('name'),f['name'],ac='name'),_f(p('email'),f['email'],'email',ac='email',extra=' inputmode="email"'),
          _f(p('company'),f['company'],req=False,ac='organization'),
          f'<div class="fld"><label for="{p("subject")}">{E(f["subject"])}</label><input id="{p("subject")}" name="subject" type="text" required aria-required="true" value="{E(t["default_subject"])}"><span class="fld-err" role="alert"></span></div>',
          f'<div class="fld fld-wide"><label for="{p("message")}">{E(f["message"])}</label><textarea id="{p("message")}" name="message" rows="5" required aria-required="true"></textarea><span class="fld-err" role="alert"></span></div>']
    priv='<p class="req-privacy">%s <a href="%s">%s</a>.</p>'%(E(t['privacy']),t['privacy_url'],E(t['privacy_link']))
    return f'''<form class="req-form" data-lang="{lang}" method="post" action="#" novalidate>
  <div class="req-grid">{"".join(rows)}</div>
  <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="offer" value=""><input type="hidden" name="intent" value=""><input type="hidden" name="lang" value="{lang}"><input type="hidden" name="page" value=""><input type="hidden" name="t0" value="">
  <p class="req-status" role="status" aria-live="polite"></p>
  <div class="req-actions"><button class="btn btn-primary req-send" type="submit" data-label="{E(t['send'])}" data-sending="{E(t['sending'])}">{E(t['send'])}</button>{priv}</div>
</form>'''
def success(lang):
    t=T[lang]
    return f'''<div class="req-ok" hidden tabindex="-1">
  <h2>{E(t['ok_h'])}</h2>
  <p class="ok-p">{E(t['ok_p'])}</p>
  <p><a class="btn btn-ghost" href="{t['ok_home']}">{E(t['ok_back'])}</a></p>
</div>'''
def config(lang):
    t=T[lang];li=1 if lang=='en' else 0
    offers={k:{'kind':v[0],'label':v[1+li]} for k,v in OFFERS.items()}
    return json.dumps({'offers':offers,'prefix':t['prefix'],'default_subject':t['default_subject'],'err_required':t['err_required'],'err_email':t['err_email'],'err_send':t['err_send']},ensure_ascii=False)
