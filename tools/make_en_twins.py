#!/usr/bin/env python3
"""One-shot: creates the English twins of the three FR pages that only had a chrome-level toggle."""
import re,os,json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
T={
'dora-awareness':dict(en='en/dora-awareness',
 title='DORA Awareness: digital risk awareness | Tyros Academy',
 desc='DORA Awareness: digital risk awareness for banks, insurers, fintechs and asset managers. Incidents, critical ICT providers, reporting.',
 og='og-tyros-academy-en.png',alt='Tyros Academy. Executive Education for Financial Services.',
 crumb='DORA Awareness',
 main='''
<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">Tyros Academy</div>
    <h1>DORA Awareness: helping non-technical teams understand digital risk.</h1>
    <p class="lede">A short programme, free of technical jargon, for banks, insurers, fintechs and asset managers: incidents, critical ICT providers and good reporting reflexes.</p>
  </div>
</div>
<article class="page-body">

<h2>What the DORA regulation changes in practice</h2>
<p>The European Digital Operational Resilience Act (DORA) requires financial entities and their critical ICT providers to manage digital risk in a structured way: mapping, incident management, resilience testing and oversight of third-party providers. These obligations are not limited to technical teams: they involve the whole organisation.</p>
<h2>A programme designed for non-technical teams</h2>
<ul>
<li><strong>Understanding the DORA stakes</strong>: what the regulation changes, without technical jargon or IT prerequisites.</li>
<li><strong>Incidents &amp; critical providers</strong>: recognising an incident and understanding the role of critical ICT providers in the resilience chain.</li>
<li><strong>Good reporting reflexes</strong>: knowing when and how to escalate an incident, to whom, and why timing matters.</li>
</ul>
<p>Cybersecurity fundamentals (phishing, passwords, sensitive data) and data protection are built into the programme rather than treated as separate trainings.</p>
<h2>Who it is for</h2>
<p>This programme is for <strong>banks, insurers, fintechs and asset managers</strong>: business teams, managers, HR and L&amp;D functions, with no technical prerequisite.</p>
<h2>A complementary second programme: AI Literacy &amp; Responsible Use</h2>
<p>DORA Awareness combines naturally with our second programme, <strong>AI Literacy &amp; Responsible Use</strong>, dedicated to the responsible use of AI. Both address the same decision-makers (Risk, Compliance, HR and L&amp;D) and can be organised for the same organisation.</p>

<div class="page-cta">
  <a href="/en/#contact" class="btn btn-primary">Talk to us in confidence</a>
  <a href="/en/" class="btn btn-ghost">Discover Tyros Group →</a>
</div>
</article>
<div class="see-also">
  <div class="see-also-inner">
    <h2>See also</h2>
    <a href="/en/ai-literacy-responsible-use-training/">AI Literacy &amp; Responsible Use</a>
<a href="/en/ai-act-ai-governance-financial-services/">AI Act &amp; AI governance</a>
<a href="/en/executive-search-banking-insurance/">Executive search for banking &amp; insurance</a>
  </div>
</div>
'''),
'executive-search-banque-assurance':dict(en='en/executive-search-banking-insurance',
 title='Executive search for banking & insurance | Tyros Group',
 desc='Specialist executive search for banking and insurance: general management, risk, compliance, audit, actuarial, AI. Direct and confidential approach.',
 og='og-executive-search-en.png',alt='Tyros Group Executive Search. Financial Services.',
 crumb='Executive search for banking & insurance',
 main='''
<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">Executive Search</div>
    <h1>Executive search for banking &amp; insurance: hiring the roles that cannot afford a mistake.</h1>
    <p class="lede">Tyros Group is an executive search firm dedicated exclusively to financial services. We search for the leaders and strategic executives of banks, insurers and regulated financial institutions.</p>
  </div>
</div>
<article class="page-body">

<h2>One sector, six domains</h2>
<p>Our specialisation is strict: banking, insurance and financial services, nothing else. This focus gives us a fine reading of organisation charts, career paths and regulatory issues that generalist firms cannot have.</p>
<ul>
<li><strong>General management &amp; executive committees</strong>: CEOs, managing directors and executive committee members for banks, insurers and regulated fintechs.</li>
<li><strong>Risk management</strong>: Chief Risk Officers and risk functions, from credit to model risk.</li>
<li><strong>Compliance</strong>: Chief Compliance Officers facing growing regulatory demands.</li>
<li><strong>Internal audit &amp; control</strong>: the third line of defence.</li>
<li><strong>Actuarial</strong>: from pricing to the Solvency II key function.</li>
<li><strong>AI, data &amp; transformation</strong>: the new executive profiles redefining finance.</li>
</ul>
<h2>A direct approach, in strict confidence</h2>
<p>The best executives do not answer job adverts: they are in post. Every search is run as a direct approach: identification, confidential outreach, in-depth assessment, a restricted short-list, and support through to integration. No search is ever advertised.</p>
<h2>Why boards and executive teams trust us</h2>
<p>Because a sensitive appointment shapes the organisation's trajectory: reputation, compliance, governance, performance. Our network of banking and insurance leaders is built over time, search after search: it cannot be bought.</p>

<div class="page-cta">
  <a href="/en/#contact" class="btn btn-primary">Talk to us in confidence</a>
  <a href="/en/" class="btn btn-ghost">Discover Tyros Group →</a>
</div>
</article>
<div class="see-also">
  <div class="see-also-inner">
    <h2>See also</h2>
    <a href="/en/chief-risk-officer-recruitment/">Recruiting a Chief Risk Officer</a>
<a href="/en/chief-compliance-officer-recruitment/">Recruiting a Chief Compliance Officer</a>
<a href="/en/executive-search-actuarial-insurance/">Executive search for actuarial roles</a>
  </div>
</div>
'''),
'executive-search-actuariat-assurance':dict(en='en/executive-search-actuarial-insurance',
 title='Executive search for actuarial roles & insurance | Tyros Group',
 desc='Recruitment of actuarial leaders: Solvency II actuarial function, pricing, reserving, actuarial data science. Insurance specialist firm.',
 og='og-executive-search-en.png',alt='Tyros Group Executive Search. Financial Services.',
 crumb='Executive search for actuarial roles',
 main='''
<div class="page-hero">
  <div class="page-hero-inner">
    <div class="eyebrow">Executive Search · Actuarial</div>
    <h1>Executive search for actuarial roles: rare profiles for key functions.</h1>
    <p class="lede">Actuarial is one of the tightest functions in the insurance market: few profiles, strong regulatory requirements, and a deep transformation driven by data science and AI.</p>
  </div>
</div>
<article class="page-body">

<h2>Functions under structural tension</h2>
<p>The Solvency II actuarial function, pricing, reserving, reinsurance, modelling: every senior actuarial role pits insurers, mutuals, brokers and consulting firms against each other for a narrow talent pool. The best actuaries are never on the market: they are in post, and in demand.</p>
<h2>A profession transformed by data</h2>
<p>The actuarial profile is changing: technical fundamentals are now joined by data science, machine learning applied to pricing, and the ability to govern complex models within a strict regulatory framework. Boards look for actuaries who can bridge the technical, the regulator and the business.</p>
<h2>Our value in this market</h2>
<ul>
<li>A maintained map of actuarial functions in France and across Europe.</li>
<li>A credible approach to highly solicited profiles: precise context, strict confidentiality.</li>
<li>An assessment that goes beyond the CV: career path, risk appetite, cultural fit.</li>
</ul>

<div class="page-cta">
  <a href="/en/#contact" class="btn btn-primary">Talk to us in confidence</a>
  <a href="/en/" class="btn btn-ghost">Discover Tyros Group →</a>
</div>
</article>
<div class="see-also">
  <div class="see-also-inner">
    <h2>See also</h2>
    <a href="/en/executive-search-banking-insurance/">Executive search for banking &amp; insurance</a>
<a href="/en/chief-risk-officer-recruitment/">Recruiting a Chief Risk Officer</a>
<a href="/en/ai-literacy-responsible-use-training/">AI Literacy &amp; Responsible Use</a>
  </div>
</div>
'''),
}
for slug,t in T.items():
    s=open(slug+'/index.html',encoding='utf-8').read()
    fr_url='/'+slug+'/';en_url='/'+t['en']+'/'
    s=s.replace('<html lang="fr">','<html lang="en">')
    s=re.sub(r'<title>.*?</title>','<title>%s</title>'%t['title'].replace('&','&amp;') if False else '<title>%s</title>'%t['title'],s,count=1)
    s=re.sub(r'(<meta name="description" content=")[^"]*"',lambda m:m.group(1)+t['desc']+'"',s,count=1)
    s=re.sub(r'(<meta property="og:title" content=")[^"]*"',lambda m:m.group(1)+t['title']+'"',s,count=1)
    s=re.sub(r'(<meta property="og:description" content=")[^"]*"',lambda m:m.group(1)+t['desc']+'"',s,count=1)
    s=s.replace('content="fr_FR"','content="en_GB"')
    s=re.sub(r'og-[a-z-]+-fr\.png',t['og'],s)
    s=re.sub(r'(<meta property="og:image:alt" content=")[^"]*"',lambda m:m.group(1)+t['alt']+'"',s,count=1)
    s=s.replace('https://tyros-group.com'+fr_url,'https://tyros-group.com'+en_url)
    # json-ld
    s=re.sub(r'("name": ")[^"]*(", "description": ")[^"]*(", "url")',lambda m:m.group(1)+t['title']+m.group(2)+t['desc']+m.group(3),s,count=1)
    s=s.replace('"inLanguage": "fr"','"inLanguage": "en"').replace('"name": "Accueil", "item": "https://tyros-group.com/"','"name": "Home", "item": "https://tyros-group.com/en/"')
    s=re.sub(r'("position": 2, "name": ")[^"]*(")',lambda m:m.group(1)+t['crumb']+m.group(2),s,count=1)
    s=re.sub(r'<main id="main">.*?</main>','<main id="main">'+t['main']+'</main>',s,flags=re.S)
    os.makedirs(t['en'],exist_ok=True);open(t['en']+'/index.html','w',encoding='utf-8').write(s)
    print('wrote',t['en'])
# register types
ty=json.load(open('tools/types.json'))
for slug,t in T.items(): ty['/'+t['en']+'/']='page'
ty['/en/']='home'
json.dump(ty,open('tools/types.json','w'),indent=1)
