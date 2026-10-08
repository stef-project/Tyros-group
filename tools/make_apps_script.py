#!/usr/bin/env python3
import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import forms
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'apps-script/Code.gs.tpl'),encoding='utf-8').read()
progs={p[0]:p[1] for p in forms.PROGRAMMES}
offers={k:[v[1],v[2]] for k,v in forms.OFFERS.items()}
out=tpl.replace('__PROGRAMMES__',json.dumps(progs,ensure_ascii=False)).replace('__OFFERS__',json.dumps(offers,ensure_ascii=False))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'apps-script/Code.gs'),'w',encoding='utf-8').write(out)
print('Code.gs generated')
