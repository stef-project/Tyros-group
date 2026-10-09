const {chromium}=require('playwright');let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const [url,acc,ref] of [['/','Accepter','Refuser'],['/en/','Accept','Refuse']]){
 console.log('\n'+url);
 for(const choice of ['none','accept','refuse','reload-after-accept','reload-after-refuse']){
  const c=await b.newContext({viewport:{width:1360,height:800}});const p=await c.newPage();const gtm=[];
  p.on('request',r=>{if(/googletagmanager\.com/.test(r.url()))gtm.push(r.url())});
  await p.route(/googletagmanager\.com/,r=>r.fulfill({contentType:'application/javascript',body:'window.__gtmRan=1'}));
  await p.goto('http://localhost:8810'+url);await p.waitForTimeout(500);
  const banner=await p.locator('#consent').isVisible();
  if(choice==='none'){ok(banner,'banner shown on first visit');ok(gtm.length===0,'GTM NOT requested before consent');
    const bs=await p.locator('#consent button').evaluateAll(a=>a.map(x=>{const r=x.getBoundingClientRect(),s=getComputedStyle(x);return [Math.round(r.width),Math.round(r.height),s.backgroundColor,s.color,s.fontWeight].join('|')}));ok(bs.length===2&&bs[0]===bs[1],'accept and refuse look identical: '+bs[0]);}
  if(choice==='accept'){await p.click('#consent button:has-text("'+acc+'")');await p.waitForTimeout(400);ok(!(await p.locator('#consent').isVisible()),'banner closes');ok(gtm.length>0,'GTM requested after Accept');}
  if(choice==='refuse'){await p.click('#consent button:has-text("'+ref+'")');await p.waitForTimeout(400);ok(!(await p.locator('#consent').isVisible()),'banner closes');ok(gtm.length===0,'GTM never requested after Refuse');
    await p.click('#cookie-settings');ok(await p.locator('#consent').isVisible(),'footer link reopens the choice');}
  if(choice==='reload-after-accept'){await p.click('#consent button:has-text("'+acc+'")');await p.reload();await p.waitForTimeout(500);ok(!(await p.locator('#consent').isVisible()),'no banner on later visits');ok(gtm.length>0,'GTM loads on later visits');}
  if(choice==='reload-after-refuse'){await p.click('#consent button:has-text("'+ref+'")');gtm.length=0;await p.reload();await p.waitForTimeout(500);ok(!(await p.locator('#consent').isVisible()),'no banner on later visits');ok(gtm.length===0,'GTM stays off');}
  await c.close()}}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));await b.close();process.exit(fails?1:0)})()
