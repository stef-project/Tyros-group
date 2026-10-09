"""Shared page shell for generated pages (legal, request). Chrome regions are filled by tools/sync.py."""
import re,os
ROOT=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
_t=open(os.path.join(ROOT,'formation-manager-recrutement/index.html'),encoding='utf-8').read()
ICON=re.search(r'<link rel="icon"[^>]*>',_t).group(0)
GTM=''
GTM_NS=''
CSP=re.search(r'<meta http-equiv="Content-Security-Policy"[^>]*>',_t).group(0)
SITE='https://tyros-group.com'
def shell(lang,url,title,desc,main,og='og-tyros-group',robots=None,body_class='page-main',jsonld=True):
    alt={'fr':'Tyros Group. Services financiers.','en':'Tyros Group. Financial services.'}[lang]
    locale={'fr':'fr_FR','en':'en_GB'}[lang]
    ld=''
    if jsonld:
        home='/' if lang=='fr' else '/en/';hn='Accueil' if lang=='fr' else 'Home'
        ld='<script type="application/ld+json">\n{"@context": "https://schema.org", "@type": "WebPage", "name": "%s", "description": "%s", "url": "%s%s", "inLanguage": "%s", "isPartOf": {"@type": "WebSite", "name": "Tyros Group", "url": "https://tyros-group.com/"}}\n</script>\n'%(title.replace('"','\\"'),desc.replace('"','\\"'),SITE,url,lang)
    rb='<meta name="robots" content="%s">\n'%robots if robots else ''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{rb}<link rel="canonical" href="{SITE}{url}">
{ICON}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Tyros Group">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:locale" content="{locale}">
<meta property="og:image" content="{SITE}/assets/og/{og}-{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og/{og}-{lang}.png">
{CSP}
<meta name="referrer" content="strict-origin-when-cross-origin">
{GTM}
{ld}<!--@css--><!--@/css-->
</head>
<body class="{body_class}">
{GTM_NS}
<!--@top--><!--@/top-->

<main id="main">
{main}
</main>
<!--@bottom--><!--@/bottom-->
<!--@scripts--><!--@/scripts-->
</body>
</html>
'''
def write(url,html):
    d=os.path.join(ROOT,url.strip('/'))
    os.makedirs(d,exist_ok=True);open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(html)
