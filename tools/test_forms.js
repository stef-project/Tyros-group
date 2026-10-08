// Playwright test of the request forms with a mocked endpoint. Run: NODE_PATH=$(npm root -g) node tools/test_forms.js
const {chromium}=require('playwright');const fs=require('fs');
const BASE='http://localhost:8810';const EP='https://script.google.com/macros/s/TEST/exec';
const js=fs.readFileSync('assets/request.js','utf8').replace('https://script.google.com/macros/s/__DEPLOY_ID__/exec',EP);
let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
async function open(url,vw=1360,mode='ok'){
  const c=await b.newContext({viewport:{width:vw,height:900}});const p=await c.newPage();const posts=[];const errs=[];
  p.on('pageerror',e=>errs.push(e.message));
  await p.route('**/assets/request.js*',r=>r.fulfill({contentType:'application/javascript',body:js}));
  await p.route(EP,async r=>{const body=r.request().postData();posts.push(Object.fromEntries(new URLSearchParams(body)));
    if(mode==='fail')return r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:false,error:'server'})});
    if(mode==='abort')return r.abort();
    r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify({ok:true,ref:'TY-20261008-ABC'})})});
  await p.route(/googletagmanager|google-analytics/,r=>r.abort());
  await p.goto(BASE+url);await p.waitForTimeout(500);return {c,p,posts,errs};
}
async function fill(p,sel,vals){for(const [n,v] of Object.entries(vals)){const e=p.locator(`${sel} [name="${n}"]`).first();
  const t=await e.evaluate(x=>x.tagName+':'+x.type);
  if(t.startsWith('SELECT'))await e.selectOption(v);else if(t.endsWith('radio'))await p.locator(`${sel} [name="${n}"][value="${v}"]`).check({force:true});else await e.fill(v);}}
const J=[
 {name:'FR general',url:'/demande/?type=general',sel:'.req-sec:not([hidden]) form',vals:{name:'Jeanne Test',company:'Banque Test',email:'j@banque.fr',message:'Bonjour'},expect:{type:'general',lang:'fr'}},
 {name:'FR recruitment (CRO)',url:'/demande/?type=recruitment&offer=cro&from=/recrutement-chief-risk-officer/',sel:'.req-sec:not([hidden]) form',vals:{name:'A B',company:'Assur SA',email:'a@assur.fr',role:'Chief Risk Officer',location:'Paris',timing:'1-3',message:''},expect:{type:'recruitment',offer:'cro',page:'/recrutement-chief-risk-officer/',lang:'fr'}},
 {name:'FR consulting (ai-act)',url:'/demande/?type=consulting&offer=ai-act&from=/ai-act-gouvernance-ia-finance/',sel:'.req-sec:not([hidden]) form',vals:{name:'A B',company:'Assur SA',email:'a@assur.fr',topic:'Gouvernance IA',deadline:'T1 2027'},expect:{type:'consulting',offer:'ai-act',lang:'fr'}},
 {name:'FR academy programme',url:'/demande/?type=academy&offer=manager-recruiter&intent=programme&from=/formation-manager-recrutement/',sel:'.req-sec:not([hidden]) form',vals:{name:'A B',company:'Assur SA',email:'a@assur.fr',participants:'10-25',format:'remote',period:'Mars 2027'},expect:{type:'academy',offer:'manager-recruiter',intent:'programme',programme:'manager-recruiter',lang:'fr'}},
 {name:'EN academy session',url:'/en/request/?type=academy&offer=dora-awareness&intent=session&from=/en/dora-awareness/',sel:'.req-sec:not([hidden]) form',vals:{name:'A B',company:'Bank plc',email:'a@bank.co.uk',participants:'25-50',format:'discuss'},expect:{type:'academy',offer:'dora-awareness',intent:'session',programme:'dora-awareness',lang:'en'}},
 {name:'EN recruitment',url:'/en/request/?type=recruitment&offer=cco&from=/en/chief-compliance-officer-recruitment/',sel:'.req-sec:not([hidden]) form',vals:{name:'A B',company:'Bank plc',email:'a@bank.co.uk',role:'CCO',location:'London',timing:'urgent'},expect:{type:'recruitment',offer:'cco',lang:'en'}},
 {name:'FR home embedded general',url:'/',sel:'.contact-form form',vals:{name:'A B',company:'X',email:'a@x.fr',message:'Hello'},expect:{type:'general',lang:'fr',page:'/'}},
 {name:'EN home embedded general',url:'/en/',sel:'.contact-form form',vals:{name:'A B',company:'X',email:'a@x.fr',message:'Hello'},expect:{type:'general',lang:'en',page:'/en/'}},
];
for(const t of J){
  console.log('\n'+t.name);
  const {c,p,posts,errs}=await open(t.url);
  const form=p.locator(t.sel);
  ok(await form.isVisible(),'form visible');
  // honeypot hidden + t0 set
  ok(await form.locator('[name="website"]').inputValue()==='', 'honeypot empty');
  ok(+(await form.locator('[name="t0"]').inputValue())>0,'t0 set');
  // empty submit -> errors
  await form.locator('.req-send').click();await p.waitForTimeout(150);
  const nerr=await form.locator('.fld.bad').count();ok(nerr>=3,'empty submit shows '+nerr+' field errors');
  ok(posts.length===0,'nothing sent when invalid');
  // invalid email
  await fill(p,t.sel,{...t.vals,email:'not-an-email'});await form.locator('.req-send').click();await p.waitForTimeout(100);
  ok(await form.locator('.fld.bad [name="email"]').count()===1,'invalid email flagged');ok(posts.length===0,'invalid email not sent');
  await fill(p,t.sel,t.vals);
  await form.locator('.req-send').click();await p.waitForTimeout(600);
  ok(posts.length===1,'exactly one POST');
  const d=posts[0]||{};
  for(const [k,v] of Object.entries(t.expect))ok(d[k]===v,`payload ${k}=${v} (got ${d[k]})`);
  ok(d.name==='A B'||d.name==='Jeanne Test','name sent');ok(!('website' in d)||d.website==='','honeypot not filled');
  ok(await p.locator('.req-ok').isVisible(),'success panel visible');
  ok((await p.locator('.req-ok .ok-ref strong').textContent())==='TY-20261008-ABC','reference shown');
  const okp=await p.locator('.req-ok .ok-p').textContent();
  if(t.expect.intent==='programme')ok(/pi[èe]ce jointe|attached/.test(okp),'programme confirmation mentions the attachment');
  ok(errs.length===0,'no JS errors '+errs.join('|'));
  await c.close();
}
// server error + network error
for(const mode of ['fail','abort']){
  console.log('\nerror path: '+mode);
  const {c,p,posts}=await open('/demande/?type=general',1360,mode);
  const f=p.locator('.req-sec:not([hidden]) form');await fill(p,'.req-sec:not([hidden]) form',{name:'A',company:'B',email:'a@b.fr',message:'m'});
  await f.locator('.req-send').click();await p.waitForTimeout(600);
  ok((await f.locator('.req-status').textContent()).includes('contact@tyros-group.com'),'error message shown with fallback address');
  ok(!(await f.locator('.req-send').isDisabled()),'button re-enabled');ok(await f.isVisible(),'form kept so nothing is lost');
  await c.close();
}
// unconfigured endpoint (production placeholder)
{console.log('\nplaceholder endpoint');const c=await b.newContext();const p=await c.newPage();await p.route(/googletagmanager/,r=>r.abort());await p.goto(BASE+'/demande/?type=general');
 await fill(p,'.req-sec:not([hidden]) form',{name:'A',company:'B',email:'a@b.fr',message:'m'});await p.locator('.req-sec:not([hidden]) .req-send').click();await p.waitForTimeout(200);
 ok((await p.locator('.req-sec:not([hidden]) .req-status').textContent()).length>10,'unconfigured endpoint shows an explicit error, never a fake success');await c.close();}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));await b.close();process.exit(fails?1:0)})()
