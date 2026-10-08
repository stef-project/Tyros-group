// Node harness for tools/apps-script/Code.gs with stubs of the Google services.
const fs=require('fs'),crypto=require('crypto');
let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
function env(props){
  const rows=[],mails=[],cache={};
  const sheet={getRange(r,c){return{setValues(v){if(r>1&&rows[r-2])rows[r-2].splice(c-1,v[0].length,...v[0]);return this},setFontWeight(){return this},setBackground(){return this},setFontColor(){return this}}},setFrozenRows(){},appendRow(r){rows.push(r)},getLastRow(){return rows.length+1}};
  const g={console,Date,Math,JSON,parseInt,String,Array,RegExp,Object,
   ContentService:{MimeType:{JSON:'json'},createTextOutput:s=>({s,setMimeType(){return this}})},
   PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k]||null})},
   SpreadsheetApp:{openById:()=>({getSheetByName:()=>sheet,insertSheet:()=>sheet})},
   MailApp:{sendEmail(a,b,c,d){mails.push(typeof a==='object'?a:{to:a,subject:b,body:c,opts:d})},getRemainingDailyQuota:()=>100},
   DriveApp:{getFileById:id=>({getBlob:()=>({setName(n){this.n=n;return this},id})})},
   CacheService:{getScriptCache:()=>({get:k=>cache[k]||null,put:(k,v)=>{cache[k]=v}})},
   LockService:{getScriptLock:()=>({waitLock(){},releaseLock(){}})},
   Utilities:{formatDate:(d,tz,f)=>f.includes('yyyyMMdd')?'20261008':d.toISOString(),DigestAlgorithm:{SHA_256:1},computeDigest:(a,s)=>crypto.createHash('sha256').update(s).digest(),base64EncodeWebSafe:b=>Buffer.from(b).toString('base64url')}};
  const src=fs.readFileSync('tools/apps-script/Code.gs','utf8');
  const fn=new Function(...Object.keys(g),src+';return {doPost,doGet}');
  return {...fn(...Object.values(g)),rows,mails};
}
const base={type:'general',lang:'fr',name:'Jeanne',company:'Banque',email:'j@banque.fr',message:'Bonjour',t0:String(Date.now()-10000),page:'/',source_url:'https://tyros-group.com/'};
const run=(e,p)=>JSON.parse(e.doPost({parameter:p}).s);
const P={SHEET_ID:'x',PDF_FILE_ID_DEFAULT:'pdf1'};
console.log('valid general');{const e=env(P);const r=run(e,base);ok(r.ok&&/^TY-20261008-/.test(r.ref),'ok + reference');ok(e.rows.length===1,'row stored');ok(e.mails.length===2,'ack + internal notification');ok(e.mails.some(m=>m.to==='j@banque.fr'),'ack to visitor');ok(e.mails.some(m=>m.to==='contact@tyros-group.com'&&m.replyTo==='j@banque.fr'),'internal mail replyTo=visitor');ok(!e.mails.some(m=>m.opts&&m.opts.attachments),'no attachment for general');}
console.log('programme request attaches the PDF');{const e=env(P);const r=run(e,{...base,type:'academy',offer:'manager-recruiter',intent:'programme',programme:'manager-recruiter',participants:'10-25',format:'remote',message:''});ok(r.ok,'ok');const ack=e.mails.find(m=>m.to==='j@banque.fr');ok(ack&&ack.opts.attachments&&ack.opts.attachments.length===1,'PDF attached to the acknowledgement');ok(e.rows[0][4]==='Manager as Recruiter','offer label stored');ok(e.rows[0][22]==='attached','sheet records attached');}
console.log('programme without PDF configured');{const e=env({SHEET_ID:'x'});const r=run(e,{...base,type:'academy',offer:'dora-awareness',intent:'programme',programme:'dora-awareness',participants:'tbd',format:'discuss'});ok(r.ok,'still acknowledged');ok(e.rows[0][22]==='MISSING','flagged MISSING in sheet');ok(/PDF/.test(e.mails.find(m=>m.to==='contact@tyros-group.com').body),'internal mail warns about missing PDF');}
console.log('EN acknowledgement');{const e=env(P);run(e,{...base,lang:'en'});ok(/we will reply|received your request/i.test(e.mails.find(m=>m.to==='j@banque.fr').body||''),'English body');}
console.log('honeypot');{const e=env(P);const r=run(e,{...base,website:'http://spam'});ok(r.ok&&e.rows.length===0&&e.mails.length===0,'silent success, nothing stored or sent');}
console.log('submission timing');{const e=env(P);ok(run(e,{...base,t0:String(Date.now()-500)}).error==='timing','too fast rejected');ok(run(e,{...base,t0:''}).error==='timing','missing t0 rejected');ok(run(e,{...base,t0:String(Date.now()-90000000)}).error==='timing','stale rejected');ok(e.rows.length===0,'nothing stored');}
console.log('validation');{const e=env(P);
 ok(run(e,{...base,email:'bad'}).error==='email','bad email');ok(run(e,{...base,name:''}).error==='required','name required');ok(run(e,{...base,type:'x'}).error==='invalid','unknown type');ok(run(e,{...base,lang:'de'}).error==='invalid','unknown lang');
 ok(run(e,{...base,type:'recruitment'}).error==='required','recruitment needs role/location/timing');ok(run(e,{...base,type:'consulting',message:''}).error==='required','consulting needs topic');ok(run(e,{...base,message:''}).error==='required','general needs message');
 ok(run(e,{...base,type:'academy',programme:'nope',participants:'tbd',format:'remote'}).error==='required','academy unknown programme');ok(e.rows.length===0,'nothing stored on invalid');}
console.log('sanitising');{const e=env(P);run(e,{...base,name:'=HYPERLINK("http://x")',message:'a'.repeat(9000)});ok(String(e.rows[0][6]).startsWith("'"),'formula injection neutralised');ok(e.rows[0][17].length<=5000,'message capped');}
console.log('rate limit per email');{const e=env(P);const rs=[1,2,3,4].map(()=>run(e,base));ok(rs[2].ok&&rs[3].error==='rate','4th request in the hour refused');}
console.log('unknown offer ignored, context kept');{const e=env(P);run(e,{...base,type:'recruitment',offer:'<script>',role:'CRO',location:'Paris',timing:'open'});ok(e.rows[0][4]==='','unknown offer dropped');ok(e.rows[0][3]==='fr'&&e.rows[0][18]==='/','lang and page stored');}
console.log('doGet health');{const e=env(P);ok(JSON.parse(e.doGet().s).ok,'ok');}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));process.exit(fails?1:0);
