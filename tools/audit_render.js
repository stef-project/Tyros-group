// Rendered audit: overflow, JS errors, forbidden effects, fonts, small text, contrast. NODE_PATH=$(npm root -g) node tools/audit_render.js [widths...]
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
const BASE='http://localhost:8810';
const pages=[];(function walk(d){for(const f of fs.readdirSync(d)){if(['design-system','.git','tools','assets','fonts','node_modules'].includes(f))continue;const p=path.join(d,f);
  if(fs.statSync(p).isDirectory())walk(p);else if(f==='index.html'||f==='404.html'){const s=fs.readFileSync(p,'utf8');if(s.includes('<h1'))pages.push('/'+p.replace(/index\.html$/,''))}}})('.');
pages.sort();
const widths=process.argv.slice(2).map(Number);const W=widths.length?widths:[360,1360];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});let bad=0;const summary={};
for(const vw of W){for(const url of pages){
  const c=await b.newContext({viewport:{width:vw,height:900},reducedMotion:'reduce'});const p=await c.newPage();const errs=[];
  p.on('pageerror',e=>errs.push(e.message));p.on('requestfailed',r=>{if(!/googletagmanager|google-analytics/.test(r.url()))errs.push('req:'+r.url())});
  await p.route(/googletagmanager|google-analytics/,r=>r.abort());
  await p.goto(BASE+url);await p.waitForTimeout(250);
  await p.addStyleTag({content:'.reveal{opacity:1!important;transform:none!important;transition:none!important}'});
  const r=await p.evaluate(()=>{
    const out={ovf:document.documentElement.scrollWidth-innerWidth,bad:[],fonts:new Set(),small:0,low:[]};
    const lum=c=>{const a=c.map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]};
    const parse=s=>{const m=s.match(/[\d.]+/g);return m?m.map(Number):[0,0,0,0]};
    const bgOf=el=>{for(let e=el;e;e=e.parentElement){const c=parse(getComputedStyle(e).backgroundColor);if((c[3]===undefined?1:c[3])>.9)return c}return [5,14,29]};
    document.querySelectorAll('body *').forEach(e=>{const cs=getComputedStyle(e);
      if(/gradient/.test(cs.backgroundImage)&&!/data:image/.test(cs.backgroundImage))out.bad.push('gradient:'+e.className);
      if(cs.boxShadow!=='none')out.bad.push('shadow:'+e.className);
      if(cs.backdropFilter&&cs.backdropFilter!=='none')out.bad.push('blur:'+e.className);
      if(e.tagName==='IMG')out.bad.push('img');
      if(cs.fontStyle==='italic'&&e.textContent.trim()&&e.tagName!=='EM')out.bad.push('italic:'+e.tagName+'.'+e.className);
      if(parseFloat(cs.borderRadius)>0&&e.offsetWidth>60&&e.offsetHeight>60&&!/icon-btn|nav-toggle/.test(e.className))out.bad.push('radius:'+e.className);
      out.fonts.add(cs.fontFamily.split(',')[0].replace(/['"]/g,''));
      const own=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>1);
      if(own&&e.offsetParent!==null&&cs.visibility!=='hidden'){
        const fs=parseFloat(cs.fontSize);if(fs<11.99&&!/logo-sub/.test(e.className))out.small++;
        const fg=parse(cs.color);const bg=bgOf(e);const a=fg[3]===undefined?1:fg[3];
        const f=[0,1,2].map(i=>Math.round(fg[i]*a+bg[i]*(1-a)));const L1=lum(f),L2=lum(bg);const ratio=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
        const large=fs>=24||(fs>=18.66&&parseInt(cs.fontWeight)>=700);
        if(ratio<(large?3:4.5))out.low.push(e.tagName+'.'+(e.className||'')+' '+ratio.toFixed(2)+' '+(e.textContent.trim().slice(0,28)));}
    });
    out.fonts=[...out.fonts];out.bad=[...new Set(out.bad)];return out;});
  const fontsOk=r.fonts.every(f=>/Fraunces|Plex Sans/.test(f)||/^(Arial|system-ui|sans-serif)$/.test(f));
  const issues=[];if(r.ovf>0)issues.push('overflow '+r.ovf);if(errs.length)issues.push('errs '+errs.slice(0,2).join(';'));if(r.bad.length)issues.push('fx '+r.bad.slice(0,5).join(','));
  if(!fontsOk)issues.push('fonts '+r.fonts.join('|'));if(r.small)issues.push('small '+r.small);if(r.low.length)issues.push('contrast '+r.low.slice(0,3).join(' / '));
  if(issues.length){bad++;console.log(vw,url,'->',issues.join(' | '))}
  await c.close()}}
console.log('\nchecked',pages.length,'pages x',W.length,'widths; pages with issues:',bad);await b.close()})()
