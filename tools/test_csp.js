// Content Security Policy + consent-gated conversion event. BASE=http://localhost:8821 NODE_PATH=$(npm root -g) node tools/test_csp.js
const {chromium}=require('playwright');const fs=require('fs');
const BASE=process.env.BASE||'http://localhost:8810';
const EP='https://script.google.com/macros/s/AKfycbxX83PNbXRDifumBvL51uNwCRGl0QBaAgT_an447QLt1gYkTw2cgIdUUOAVOE9u0IL0Ww/exec';
let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
async function ctx(){const c=await b.newContext({viewport:{width:1280,height:900}});const p=await c.newPage();const issues=[];
 p.on('console',m=>{if(m.type()==='error'||/Refused|Content Security/i.test(m.text()))issues.push(m.text().slice(0,120))});p.on('pageerror',e=>issues.push('pageerror '+e.message));
 await p.addInitScript(()=>{document.addEventListener('securitypolicyviolation',e=>console.error('Refused to '+e.violatedDirective+' '+e.blockedURI))});
 await p.route(/googletagmanager\.com\/gtm\.js/,r=>r.fulfill({contentType:'application/javascript',body:'window.__g=1;'}));
 await p.route(/google-analytics|googletagmanager\.com\/(?!gtm\.js)/,r=>r.fulfill({status:204,body:''}));
 await p.route(EP,r=>r.fulfill({status:200,contentType:'application/json',headers:{'access-control-allow-origin':'*'},body:JSON.stringify({ok:true})}));
 return {c,p,issues}}
// 1. every page of the sitemap: no CSP or script error, consent accepted, cookie settings opened
const sm=fs.readFileSync('sitemap.xml','utf8');const urls=[...sm.matchAll(/<loc>https:\/\/tyros-group\.com([^<]*)<\/loc>/g)].map(m=>m[1]).concat(['/demande/','/en/request/','/404.html']);
for(const u of urls){const {c,p,issues}=await ctx();await p.goto(BASE+u);await p.waitForTimeout(300);
 const acc=p.locator('#consent button',{hasText:/Accepter|Accept/}).first();if(await acc.count())await acc.click();await p.waitForTimeout(250);
 const ck=p.locator('#cookie-settings');if(await ck.count()){await ck.click();await p.waitForTimeout(100)}
 ok(issues.length===0,u+' CSP/JS issues: '+issues.join(';'));await c.close()}
console.log('pages scanned:',urls.length);
// 2. conversion event: only after consent was granted, exactly once
async function submit(p){await p.waitForTimeout(4200);const f=p.locator('form.req-form').first();await f.locator('[name=name]').fill('Test');await f.locator('[name=email]').fill('t@example.com');await f.locator('[name=message]').fill('Bonjour');await f.locator('.req-send').click();await p.waitForTimeout(800)}
const count=p=>p.evaluate(()=>(window.dataLayer||[]).filter(e=>e&&e.event==='contact_submitted').length);
{const {c,p}=await ctx();await p.goto(BASE+'/demande/');await p.locator('#consent button',{hasText:/Refuser/}).click();await submit(p);ok(await count(p)===0,'refused: no conversion event');await c.close()}
{const {c,p}=await ctx();await p.goto(BASE+'/demande/');await p.locator('#consent button',{hasText:/Accepter/}).click();await p.waitForTimeout(300);await submit(p);ok(await count(p)===1,'accepted: exactly one conversion event');await c.close()}
{const {c,p}=await ctx();await p.goto(BASE+'/demande/');await submit(p);ok(await count(p)===0,'submitted before choosing: nothing queued');await p.locator('#consent button',{hasText:/Accepter/}).click();await p.waitForTimeout(400);ok(await count(p)===0,'accepting afterwards does not replay the event');await c.close()}
console.log(fails?'FAILURES: '+fails:'ALL PASSED');await b.close()})()
