"""Request forms: one component, four journeys (recruitment, consulting, academy, general), FR and EN.
Rendered statically into /demande/ and /en/request/, and (general only) into the home contact section."""
import json,html

PROGRAMMES=[ # id, name, FR page, EN page
 ('dora-awareness','DORA Awareness','/dora-awareness/','/en/dora-awareness/'),
 ('ai-literacy','AI Literacy & Responsible Use','/formation-ia-banque-assurance/','/en/ai-literacy-responsible-use-training/'),
 ('manager-recruiter','Manager as Recruiter','/formation-manager-recrutement/','/en/manager-recruitment-training/'),
 ('specialist-talent','Hiring & Retaining Specialist Talent','/formation-recrutement-talents-finance/','/en/financial-services-talent-recruitment-training/'),
 ('business-development','Business Development in Financial Services','/formation-business-development-finance/','/en/financial-services-business-development-training/'),
 ('client-relationships','Strategic Client Relationships','/formation-relation-client-b2b/','/en/strategic-client-relationships-training/'),
]
# offer id -> (type, FR label, EN label)
OFFERS={
 'cro':('recruitment','Recruter un Chief Risk Officer','Recruiting a Chief Risk Officer'),
 'cco':('recruitment','Recruter un Chief Compliance Officer','Recruiting a Chief Compliance Officer'),
 'banking-insurance':('recruitment','Executive search banque & assurance','Executive search for banking & insurance'),
 'actuarial':('recruitment','Executive search actuariat','Executive search for actuarial roles'),
 'executive-search':('recruitment','Tyros Executive Search','Tyros Executive Search'),
 'ai-act':('consulting','AI Act & gouvernance de l\'IA','AI Act & AI governance'),
 'advisory':('consulting','Tyros Advisory','Tyros Advisory'),
 'boards':('general','Conseils & dirigeants','Boards & Executives'),
 'compliance':('consulting','Conformité et avantage compétitif','Compliance as a competitive advantage'),
 'membership-essential':('general','Membership Essential','Membership Essential'),
 'membership-professional':('general','Membership Professional','Membership Professional'),
 'membership-enterprise':('general','Membership Enterprise','Membership Enterprise'),
 'briefing':('general','Briefing d\'intelligence confidentiel','Confidential intelligence briefing'),
 'private':('general','Tyros Private','Tyros Private'),
}
for pid,name,_,_ in PROGRAMMES: OFFERS[pid]=('academy',name,name)

T={
'fr':dict(
 tabs=[('general','Contact général'),('recruitment','Recrutement'),('consulting','Conseil'),('academy','Tyros Academy')],
 eyebrow='Demande',
 h1={'general':'Échange confidentiel.','recruitment':'Demande de recrutement.','consulting':'Demande de conseil.','academy':'Tyros Academy.','programme':'Demander le programme.','session':'Organiser une session.'},
 lede={'general':'Dites-nous ce qui compte. Réponse sous 48 h, en toute confidentialité.',
       'recruitment':'Décrivez le poste ou le profil recherché. Toute recherche est conduite en approche directe et sous stricte confidentialité.',
       'consulting':'Décrivez le sujet ou le besoin. Nous vous répondons avec une première lecture et les prochaines étapes.',
       'academy':'Indiquez le programme, le public et le format envisagés. Nous construisons la session avec vous.',
       'programme':'Indiquez le programme qui vous intéresse. Nous prenons connaissance de votre demande et revenons vers vous pour vous le transmettre.',
       'session':'Indiquez le programme, le public et le format envisagés. Nous construisons la session avec vous.'},
 f=dict(name='Nom',company='Entreprise',email='Email',message='Message',message_opt='Message (facultatif)',
        role='Poste ou profil recherché',location='Localisation',timing='Calendrier',
        topic='Sujet ou besoin',deadline='Échéance éventuelle',
        programme='Programme',participants='Nombre approximatif de participants',format='Format souhaité',period='Période envisagée'),
 timing=[('urgent','Urgent (moins d\'un mois)'),('1-3','1 à 3 mois'),('3-6','3 à 6 mois'),('open','À définir')],
 participants=[('<10','Moins de 10'),('10-25','10 à 25'),('25-50','25 à 50'),('50+','Plus de 50'),('tbd','À préciser')],
 formats=[('remote','À distance'),('in-person','En présentiel'),('discuss','À discuter')],
 choose='Choisir',multi=('multiple','Plusieurs programmes / à discuter'),
 send={'general':'Envoyer','recruitment':'Envoyer la demande','consulting':'Envoyer la demande','academy':'Envoyer la demande','programme':'Demander le programme','session':'Envoyer la demande'},
 sending='Envoi en cours…',
 privacy='En envoyant ce formulaire, vous acceptez que Tyros Group traite votre demande pour y répondre.',
 privacy_link='Politique de confidentialité',privacy_url='/confidentialite/',
 ctx='Votre demande concerne',orig='Page d\'origine',
 err_required='Merci de renseigner ce champ.',err_email='Merci de saisir une adresse e-mail valide.',
 err_send='L\'envoi n\'a pas abouti. Merci de réessayer dans un instant ou d\'écrire à contact@tyros-group.com.',
 ok_h='Merci, votre demande est bien envoyée.',
 ok_p='Nous avons bien reçu votre demande et vous répondons sous 48 h ouvrées. Un accusé de réception vient de vous être envoyé.',
 ok_ref='Référence',ok_back='Retour à l\'accueil',ok_home='/',ok_another='Faire une autre demande',
 noscript='Ce formulaire nécessite JavaScript. Vous pouvez aussi nous écrire à contact@tyros-group.com.',
 switch='Choisir un autre type de demande'),
'en':dict(
 tabs=[('general','General enquiry'),('recruitment','Recruitment'),('consulting','Consulting'),('academy','Tyros Academy')],
 eyebrow='Request',
 h1={'general':'A confidential conversation.','recruitment':'Recruitment request.','consulting':'Consulting request.','academy':'Tyros Academy.','programme':'Request the programme.','session':'Arrange a session.'},
 lede={'general':'Tell us what matters. We reply within 48 hours, in full confidence.',
       'recruitment':'Describe the role or profile you are looking for. Every search is run as a direct approach and in strict confidence.',
       'consulting':'Describe the topic or need. We reply with a first reading and next steps.',
       'academy':'Tell us the programme, audience and format you have in mind. We build the session with you.',
       'programme':'Tell us which programme interests you. We will review your request and come back to you to share it.',
       'session':'Tell us the programme, audience and format you have in mind. We build the session with you.'},
 f=dict(name='Name',company='Company',email='Email',message='Message',message_opt='Message (optional)',
        role='Role or profile sought',location='Location',timing='Timing',
        topic='Topic or need',deadline='Deadline, if any',
        programme='Programme',participants='Approximate number of participants',format='Preferred format',period='Intended period'),
 timing=[('urgent','Urgent (under one month)'),('1-3','1 to 3 months'),('3-6','3 to 6 months'),('open','To be defined')],
 participants=[('<10','Fewer than 10'),('10-25','10 to 25'),('25-50','25 to 50'),('50+','More than 50'),('tbd','To be confirmed')],
 formats=[('remote','Remote'),('in-person','In person'),('discuss','To discuss')],
 choose='Select',multi=('multiple','Several programmes / to discuss'),
 send={'general':'Send','recruitment':'Send the request','consulting':'Send the request','academy':'Send the request','programme':'Request the programme','session':'Send the request'},
 sending='Sending…',
 privacy='By sending this form, you agree that Tyros Group will process your request in order to reply to it.',
 privacy_link='Privacy policy',privacy_url='/en/privacy-policy/',
 ctx='Your request concerns',orig='Originating page',
 err_required='Please fill in this field.',err_email='Please enter a valid email address.',
 err_send='We could not send your request. Please try again in a moment or write to contact@tyros-group.com.',
 ok_h='Thank you, your request has been sent.',
 ok_p='We have received your request and will reply within 48 working hours. An acknowledgement has just been sent to you.',
 ok_ref='Reference',ok_back='Back to the home page',ok_home='/en/',ok_another='Make another request',
 noscript='This form needs JavaScript. You can also write to us at contact@tyros-group.com.',
 switch='Choose another type of request'),
}
E=lambda x:html.escape(x,quote=True)

def field(id_,label,kind='text',req=True,extra='',autocomplete=None,t=None):
    ac=' autocomplete="%s"'%autocomplete if autocomplete else ''
    r=' required aria-required="true"' if req else ''
    return f'<div class="fld"><label for="{id_}">{E(label)}{"" if not req else ""}</label><input id="{id_}" name="{id_.split("__")[-1]}" type="{kind}"{r}{ac}{extra}><span class="fld-err" role="alert"></span></div>'

def select(id_,label,opts,t,req=True,first=True):
    o=''.join('<option value="%s">%s</option>'%(E(v),E(l)) for v,l in opts)
    ph='<option value="" selected disabled>%s</option>'%E(t['choose']) if first else ''
    return f'<div class="fld"><label for="{id_}">{E(label)}</label><select id="{id_}" name="{id_.split("__")[-1]}"{" required aria-required=true" if req else ""}>{ph}{o}</select><span class="fld-err" role="alert"></span></div>'

def textarea(id_,label,req,rows=5):
    return f'<div class="fld fld-wide"><label for="{id_}">{E(label)}</label><textarea id="{id_}" name="message" rows="{rows}"{" required aria-required=true" if req else ""}></textarea><span class="fld-err" role="alert"></span></div>'

def radios(id_,label,opts):
    r=''.join(f'<label class="opt"><input type="radio" name="{id_.split("__")[-1]}" value="{E(v)}"{" required" if i==0 else ""}><span>{E(l)}</span></label>' for i,(v,l) in enumerate(opts))
    return f'<fieldset class="fld fld-wide fld-opts"><legend>{E(label)}</legend><div class="opts">{r}</div><span class="fld-err" role="alert"></span></fieldset>'

def form(lang,type_,uid,hero=True):
    """Returns the <form> element for one journey. uid prefixes ids so several forms can coexist."""
    t=T[lang];f=t['f'];p=lambda n:'%s__%s'%(uid,n)
    rows=[field(p('name'),f['name'],autocomplete='name'),field(p('company'),f['company'],autocomplete='organization'),field(p('email'),f['email'],'email',autocomplete='email',extra=' inputmode="email"')]
    if type_=='recruitment':
        rows+=[field(p('role'),f['role']),field(p('location'),f['location']),select(p('timing'),f['timing'],t['timing'],t),textarea(p('message'),f['message_opt'],False)]
    elif type_=='consulting':
        rows+=[field(p('topic'),f['topic']),field(p('deadline'),f['deadline'],req=False),textarea(p('message'),f['message_opt'],False)]
    elif type_=='academy':
        progs=[(pid,name) for pid,name,_,_ in PROGRAMMES]+[t['multi']]
        rows+=[select(p('programme'),f['programme'],progs,t),select(p('participants'),f['participants'],t['participants'],t),radios(p('format'),f['format'],t['formats']),field(p('period'),f['period'],req=False),textarea(p('message'),f['message_opt'],False)]
    else:
        rows+=[textarea(p('message'),f['message'],True,4)]
    priv='<p class="req-privacy">%s <a href="%s">%s</a>.</p>'%(E(t['privacy']),t['privacy_url'],E(t['privacy_link']))
    return f'''<form class="req-form" data-type="{type_}" data-lang="{lang}" method="post" action="#" novalidate>
  <div class="req-grid">{"".join(rows)}</div>
  <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="type" value="{type_}"><input type="hidden" name="offer" value=""><input type="hidden" name="intent" value=""><input type="hidden" name="lang" value="{lang}"><input type="hidden" name="page" value=""><input type="hidden" name="t0" value="">
  <p class="req-status" role="status" aria-live="polite"></p>
  <div class="req-actions"><button class="btn btn-primary req-send" type="submit" data-label="{E(t['send'][type_])}" data-sending="{E(t['sending'])}">{E(t['send'][type_])}</button>{priv}</div>
</form>'''

def success(lang):
    t=T[lang]
    return f'''<div class="req-ok" hidden tabindex="-1">
  <h2>{E(t['ok_h'])}</h2>
  <p class="ok-p">{E(t['ok_p'])}</p>
  <p class="ok-ref">{E(t['ok_ref'])} <strong></strong></p>
  <p><a class="btn btn-ghost" href="{t['ok_home']}">{E(t['ok_back'])}</a></p>
</div>'''

def config(lang):
    t=T[lang]
    offers={k:{'type':v[0],'label':v[1] if lang=='fr' else v[2]} for k,v in OFFERS.items()}
    return json.dumps({'offers':offers,'err_required':t['err_required'],'err_email':t['err_email'],'err_send':t['err_send'],'h1':t['h1'],'lede':t['lede'],'send':t['send'],'ctx':t['ctx'],'orig':t['orig']},ensure_ascii=False)
