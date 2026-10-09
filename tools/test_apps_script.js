const fs=require('fs');let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
function env(opts={}){const mails=[],cache={};const g={console,Date,Math,JSON,parseInt,String,Array,RegExp,Object,
 ContentService:{MimeType:{JSON:'json'},createTextOutput:s=>({s,setMimeType(){return this}})},
 PropertiesService:{getScriptProperties:()=>({getProperty:k=>(opts.props||{})[k]||null})},
 MailApp:{sendEmail(m){if(opts.mailFails)throw new Error('quota');mails.push(m)},getRemainingDailyQuota:()=>100},
 CacheService:{getScriptCache:()=>({get:k=>cache[k]||null,put:(k,v)=>{cache[k]=v}})},
 Utilities:{formatDate:()=>'2026-10-08 12:00',DigestAlgorithm:{SHA_256:1},computeDigest:(a,s)=>require('crypto').createHash('sha256').update(s).digest(),base64EncodeWebSafe:b=>Buffer.from(b).toString('base64url')}};
 const fn=new Function(...Object.keys(g),fs.readFileSync('tools/apps-script/Code.gs','utf8')+';return {doPost,doGet}');return {...fn(...Object.values(g)),mails}}
const base={name:'Jeanne',email:'J@Banque.fr',company:'Banque',subject:'Tyros Academy : Demande de programme : Manager as Recruiter',message:'Bonjour',lang:'fr',page:'/formation-manager-recrutement/',offer:'manager-recruiter',intent:'programme',source_url:'https://tyros-group.com/demande/',t0:String(Date.now()-10000)};
const run=(e,p)=>JSON.parse(e.doPost({parameter:p}).s);
console.log('valid');{const e=env();const r=run(e,base);ok(r.ok,'ok only after the mail is sent');ok(e.mails.length===1,'exactly one mail (none to the visitor)');const m=e.mails[0];ok(m.to==='contact@tyros-group.com','sent to the Tyros address');ok(m.replyTo==='j@banque.fr','Reply goes to the visitor');ok(/Manager as Recruiter/.test(m.subject),'subject carries the offer');ok(/Page d'origine : \/formation-manager-recrutement\//.test(m.body),'origin page in the notification');ok(/Offre : manager-recruiter \(programme\)/.test(m.body),'offer and intent in the notification');ok(/Langue : FR/.test(m.body),'language in the notification');ok(!e.mails.some(x=>x.to==='j@banque.fr'),'no automatic mail to the visitor');}
console.log('NOTIFY_TO');{const e=env({props:{NOTIFY_TO:'stef@tyros-group.com'}});run(e,base);ok(e.mails[0].to==='stef@tyros-group.com','configurable recipient');}
console.log('mail failure is never reported as success');{const e=env({mailFails:true});ok(run(e,base).error==='server','error returned, so the site shows no confirmation');}
console.log('company optional');{const e=env();ok(run(e,{...base,company:''}).ok&&/Entreprise : -/.test(e.mails[0].body),'ok without company');}
console.log('EN');{const e=env();run(e,{...base,lang:'en'});ok(/\(EN\)/.test(e.mails[0].subject),'language tag');}
console.log('honeypot');{const e=env();const r=run(e,{...base,website:'http://x'});ok(r.ok&&e.mails.length===0,'silent success, no mail');}
console.log('timing');{const e=env();ok(run(e,{...base,t0:String(Date.now()-500)}).error==='timing','too fast');ok(run(e,{...base,t0:''}).error==='timing','missing');ok(run(e,{...base,t0:String(Date.now()-90000000)}).error==='timing','stale');ok(e.mails.length===0,'no mail');}
console.log('validation');{const e=env();ok(run(e,{...base,name:''}).error==='required','name');ok(run(e,{...base,message:''}).error==='required','message');ok(run(e,{...base,subject:''}).error==='required','subject');ok(run(e,{...base,email:'bad'}).error==='email','email');ok(e.mails.length===0,'no mail');}
console.log('double send');{const e=env();const r1=run(e,base),r2=run(e,base);ok(r1.ok&&r2.ok,'both confirmed');ok(e.mails.length===1,'only one mail for the same message');ok(run(e,{...base,message:'Autre message'}).ok&&e.mails.length===2,'a different message is sent');}
console.log('rate limit');{const e=env();const rs=[1,2,3,4].map(i=>run(e,{...base,message:'m'+i}));ok(rs[2].ok&&rs[3].error==='rate','4th in an hour refused');}
console.log('header injection / length');{const e=env();run(e,{...base,subject:'Hi\r\nBcc: x@y.z',message:'a'.repeat(9000)});ok(!/[\r\n]/.test(e.mails[0].subject),'no line break in the subject');ok(e.mails[0].body.length<5600,'message capped');}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));process.exit(fails?1:0);
