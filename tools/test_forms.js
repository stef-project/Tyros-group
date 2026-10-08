// Playwright test of the single contact form with a mocked endpoint. NODE_PATH=$(npm root -g) node tools/test_forms.js
const {chromium}=require('playwright');const fs=require('fs');
const BASE='http://localhost:8810';const EP='https://script.google.com/macros/s/TEST/exec';
const js=fs.readFileSync('assets/request.js','utf8').replace('https://script.google.com/macros/s/__DEPLOY_ID__/exec',EP);
let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
async function open(url,vw=1360,mode='ok'){const c=await b.newContext({viewport:{width:vw,height:900}});const p=await c.newPage();const posts=[],errs=[];
 p.on('pageerror',e=>errs.push(e.message));
 await p.route('**/assets/request.js*',r=>r.fulfill({contentType:'application/javascript',body:js}));
 await p.route(EP,r=>{posts.push(Object.fromEntries(new URLSearchParams(r.request().postData())));
  if(mode==='fail')return r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:false,error:'server'})});
  if(mode==='abort')return r.abort();
  r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify({ok:true})})});
 await p.route(/googletagmanager|google-analytics/,r=>r.abort());await p.goto(BASE+url);await p.waitForTimeout(400);return {c,p,posts,errs}}
const sel='form.req-form';
const J=[
 ['FR general','/demande/','Échange confidentiel',{lang:'fr'}],
 ['FR programme (button from Manager as Recruiter)','/demande/?type=academy&offer=manager-recruiter&intent=programme&from=/formation-manager-recrutement/','Demande de programme : Manager as Recruiter',{offer:'manager-recruiter',intent:'programme',page:'/formation-manager-recrutement/',lang:'fr'}],
 ['FR session','/demande/?offer=dora-awareness&intent=session&from=/dora-awareness/','Organisation d\'une session : DORA Awareness',{intent:'session',lang:'fr'}],
 ['FR recruitment (CRO)','/demande/?offer=cro&from=/recrutement-chief-risk-officer/','Recrutement : Chief Risk Officer',{offer:'cro',lang:'fr'}],
 ['FR consulting (AI Act)','/demande/?offer=ai-act&from=/ai-act-gouvernance-ia-finance/','Conseil : AI Act & gouvernance de l\'IA',{offer:'ai-act'}],
 ['FR membership','/demande/?offer=membership-professional&from=/','Membership Professional',{offer:'membership-professional'}],
 ['EN programme','/en/request/?offer=ai-literacy&intent=programme&from=/en/ai-literacy-responsible-use-training/','Programme request : AI Literacy & Responsible Use',{lang:'en',offer:'ai-literacy',intent:'programme'}],
 ['EN general mobile','/en/request/','Confidential discussion',{lang:'en'},390],
 ['EN recruitment mobile','/en/request/?offer=cco&from=/en/chief-compliance-officer-recruitment/','Recruitment : Chief Compliance Officer',{lang:'en',offer:'cco'},390],
 ['FR home embedded','/','Échange confidentiel',{lang:'fr',page:'/'},1360,'.contact-form form'],
 ['EN home embedded mobile','/en/','Confidential discussion',{lang:'en',page:'/en/'},390,'.contact-form form'],
];
for(const [name,url,subj,exp,vw,fsel] of J){console.log('\n'+name);
 const {c,p,posts,errs}=await open(url,vw||1360);const f=p.locator(fsel||sel).first();
 ok(await f.isVisible(),'form visible');
 ok(await f.locator('[name=subject]').inputValue()===subj,'subject prefilled: '+subj);
 await f.locator('[name=subject]').fill('');await f.locator('.req-send').click();await p.waitForTimeout(150);
 ok(await f.locator('.fld.bad').count()>=4,'empty fields flagged ('+await f.locator('.fld.bad').count()+')');ok(posts.length===0,'nothing sent when invalid');
 await f.locator('[name=subject]').fill(subj);await f.locator('[name=name]').fill('Jeanne');await f.locator('[name=email]').fill('nope');await f.locator('[name=message]').fill('Bonjour');
 await f.locator('.req-send').click();await p.waitForTimeout(120);ok(await f.locator('.fld.bad [name=email]').count()===1,'invalid email flagged');ok(posts.length===0,'invalid email not sent');
 await f.locator('[name=email]').fill('j@banque.fr');
 await f.locator('.req-send').click();await p.waitForTimeout(700);
 ok(posts.length===1,'one POST');const d=posts[0]||{};
 ok(d.subject===subj,'subject sent');ok(d.company==='','company optional');ok(d.email==='j@banque.fr'&&d.message==='Bonjour','email and message sent');
 for(const [k,v] of Object.entries(exp))ok(d[k]===v,`payload ${k}=${v} (got ${d[k]})`);
 ok(+d.t0>0,'timer sent');
 ok(await p.locator('.req-ok').first().isVisible(),'confirmation shown after success');
 ok(await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth)<=0,'no horizontal overflow');ok(errs.length===0,'no JS errors');await c.close()}
for(const mode of ['fail','abort']){console.log('\nno confirmation when sending fails: '+mode);
 const {c,p}=await open('/demande/',1360,mode);const f=p.locator(sel);await f.locator('[name=name]').fill('A');await f.locator('[name=email]').fill('a@b.fr');await f.locator('[name=message]').fill('m');
 await f.locator('.req-send').click();await p.waitForTimeout(600);
 ok(!(await p.locator('.req-ok').isVisible()),'no confirmation');ok((await f.locator('.req-status').textContent()).includes('contact@tyros-group.com'),'error with fallback address');ok(!(await f.locator('.req-send').isDisabled()),'can retry');ok((await f.locator('[name=message]').inputValue())==='m','message kept');await c.close()}
{console.log('\nplaceholder endpoint');const c=await b.newContext();const p=await c.newPage();await p.route(/googletagmanager/,r=>r.abort());await p.goto(BASE+'/demande/');
 await p.locator(sel+' [name=name]').fill('A');await p.locator(sel+' [name=email]').fill('a@b.fr');await p.locator(sel+' [name=message]').fill('m');await p.locator(sel+' .req-send').click();await p.waitForTimeout(200);
 ok(!(await p.locator('.req-ok').isVisible())&&(await p.locator('.req-status').textContent()).length>10,'unconfigured: explicit error, never a fake confirmation');await c.close()}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));await b.close();process.exit(fails?1:0)})()
