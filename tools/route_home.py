#!/usr/bin/env python3
"""One-shot: routes the home CTAs, embeds the general form in #contact, removes the public PDF link."""
import os,re,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import sync,forms
req=sync.req
def run(f,lang):
    s=open(f,encoding='utf-8').read()
    home=sync.L[lang]['home'];li=0 if lang=='fr' else 1
    a=s.index('<main id="main">');b=s.index('</main>')
    m=s[a:b]
    seq=[ # ordered replacement of every #contact target inside <main>
      ('general',None,None),            # hero primary
      ('recruitment','executive-search',None),   # divi Executive Search
      ('general','private',None),       # divi Tyros Private
      ('general','briefing',None),      # ihub Talent Mapping
      ('general','briefing',None),      # ihub Market Trends
      ('general','briefing',None),      # ihub Compensation Benchmark
      ('general','briefing',None),      # Request a briefing
      ('general','membership-essential',None),
      ('general','membership-professional',None),
      ('general','membership-enterprise',None),
      ('academy',None,'session'),       # organiser une session
    ]
    it=iter(seq);cnt=[0]
    def rep(mo):
        try:k,o,i=next(it)
        except StopIteration: raise SystemExit('more #contact anchors than expected in '+f)
        cnt[0]+=1
        return 'href="%s"'%req(lang,k,o,i)
    m=re.sub(r'href="#contact"',rep,m)
    assert cnt[0]==len(seq),(f,cnt[0])
    # programme PDF -> request
    pdf=re.search(r'<a href="/downloads/tyros-academy-programme\.pdf" class="btn btn-ghost">[^<]*</a>',m);assert pdf
    label='Demander le programme' if lang=='fr' else 'Request the programme'
    m=m.replace(pdf.group(0),'<a href="%s" class="btn btn-ghost">%s</a>'%(req(lang,'academy',None,'programme'),label))
    # contact section: embedded general form
    i=m.index('<section class="contact" id="contact">');j=m.index('</section>',i)+10
    t=forms.T[lang]
    sec=m[i:j]
    eyebrow=re.search(r'<div class="eyebrow">.*?</div>',sec).group(0)
    h2=re.search(r'<h2>.*?</h2>',sec).group(0)
    sub=re.search(r'<p class="sub">.*?</p>',sec).group(0)
    cinfo=re.search(r'<div class="cinfo">.*?</div>\s*</div>\s*</div>\s*</section>',sec,re.S)
    rows=re.search(r'<div class="cinfo">.*?(?=</div>\s*</div>\s*</section>)',sec,re.S).group(0)+'</div>'
    new=('<section class="contact" id="contact">\n  <div class="wrap contact-inner">\n    <div>\n      %s\n      %s\n      %s\n      %s\n    </div>\n'
         '    <div class="contact-form">\n      %s\n      %s\n    </div>\n  </div>\n  <script type="application/json" id="req-config">%s</script>\n</section>')%(eyebrow,h2,sub,rows,forms.form(lang,'general','home'),forms.success(lang),forms.config(lang))
    m=m[:i]+new+m[j:]
    s=s[:a]+m+s[b:]
    # EN: FR link leftovers
    open(f,'w',encoding='utf-8').write(s)
    print(f,'ok')
run('index.html','fr');run('en/index.html','en')
