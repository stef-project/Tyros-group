// Node harness for tools/apps-script/Code.gs with stubs of the Google services.
const fs=require('fs'),crypto=require('crypto');
let fails=0;const ok=(c,m)=>{if(!c){fails++;console.log('  FAIL',m)}else console.log('  ok  ',m)};
function env(props){
  const rows=[],mails=[],cache={},files=[];
  const sheet={getRange(r,c){return{setValues(v){if(r>1&&rows[r-2])rows[r-2].splice(c-1,v[0].length,...v[0]);return this},setFontWeight(){return this},setBackground(){return this},setFontColor(){return this}}},setFrozenRows(){},appendRow(r){rows.push(r)},getLastRow(){return rows.length+1}};
  const g={console,Date,Math,JSON,parseInt,String,Array,RegExp,Object,
   ContentService:{MimeType:{JSON:'json'},createTextOutput:s=>({s,setMimeType(){return this}})},
   PropertiesService:{getScriptProperties:()=>({getProperty:k=>props[k]||null})},
   SpreadsheetApp:{openById:()=>({getSheetByName:()=>sheet,insertSheet:()=>sheet})},
   MailApp:{sendEmail(a,b,c,d){mails.push(typeof a==='object'?a:{to:a,subject:b,body:c,opts:d})},getRemainingDailyQuota:()=>100},
   DriveApp:{getFolderById:id=>({createFile:b=>{files.push(b);return {setSharing(){},getUrl:()=>'https://drive.google.com/file/'+files.length}}}),Access:{PRIVATE:1},Permission:{NONE:1}},
   CacheService:{getScriptCache:()=>({get:k=>cache[k]||null,put:(k,v)=>{cache[k]=v}})},
   LockService:{getScriptLock:()=>({waitLock(){},releaseLock(){}})},
   Utilities:{newBlob:(b,t,n)=>({bytes:b,name:n}),base64Decode:b=>{const x=Buffer.from(b,'base64');return [...x].map(v=>v>127?v-256:v)},formatDate:(d,tz,f)=>f.includes('yyyyMMdd')?'20261008':d.toISOString(),DigestAlgorithm:{SHA_256:1},computeDigest:(a,s)=>crypto.createHash('sha256').update(s).digest(),base64EncodeWebSafe:b=>Buffer.from(b).toString('base64url')}};
  const src=fs.readFileSync('tools/apps-script/Code.gs','utf8');
  const fn=new Function(...Object.keys(g),src+';return {doPost,doGet}');
  return {...fn(...Object.values(g)),rows,mails,files};
}
const base={type:'general',lang:'fr',name:'Jeanne',company:'Banque',email:'j@banque.fr',message:'Bonjour',t0:String(Date.now()-10000),page:'/',source_url:'https://tyros-group.com/'};
const run=(e,p)=>JSON.parse(e.doPost({parameter:p}).s);
const P={SHEET_ID:'x'};const PC={SHEET_ID:'x',CV_ENABLED:'true',CV_FOLDER_ID:'f'};
console.log('valid general');{const e=env(P);const r=run(e,base);ok(r.ok&&/^TY-20261008-/.test(r.ref),'ok + reference');ok(e.rows.length===1,'row stored');ok(e.mails.length===2,'ack + internal notification');ok(e.mails.some(m=>m.to==='j@banque.fr'),'ack to visitor');ok(e.mails.some(m=>m.to==='contact@tyros-group.com'&&m.replyTo==='j@banque.fr'),'internal mail replyTo=visitor');ok(!e.mails.some(m=>m.opts&&m.opts.attachments),'no attachment for general');}
console.log('programme request: acknowledged only, never a document');{const e=env(P);const r=run(e,{...base,type:'academy',offer:'manager-recruiter',intent:'programme',programme:'manager-recruiter',participants:'10-25',format:'remote',message:''});ok(r.ok,'ok');const ack=e.mails.find(m=>m.to==='j@banque.fr');ok(ack&&!(ack.opts&&ack.opts.attachments),'no attachment in the acknowledgement');ok(!/programme en pi|attached|joint/i.test(ack.body),'acknowledgement does not promise a document');ok(/Manager as Recruiter/.test(ack.body),'offer context recalled');ok(e.rows[0][4]==='Manager as Recruiter','offer label stored');ok(e.rows[0][5]==='programme','intent stored');const n=e.mails.find(m=>m.to==='contact@tyros-group.com');ok(/DEMANDE DE PROGRAMME/.test(n.body),'internal mail says: identify, then send by hand');ok(!e.mails.some(m=>m.opts&&m.opts.attachments),'no mail carries an attachment');}
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
const pdf=Buffer.from('%PDF-1.4 test').toString('base64'),exe=Buffer.from('MZ binary').toString('base64');
const cand={...base,type:'candidate',company:'',name:'Paul Candidat',email:'p@mail.fr',current:'Risk Manager',area:'risk',location:'Paris',consent:'yes',cv_name:'cv paul.pdf',cv_data:pdf,message:''};
console.log('candidate: disabled by default');{const e=env(P);ok(run(e,cand).error==='disabled','refused until CV_ENABLED=true and a folder exist');ok(e.files.length===0&&e.rows.length===0,'nothing stored');}
console.log('candidate: CV stored privately');{const e=env(PC);const r=run(e,cand);ok(r.ok,'accepted');ok(e.files.length===1&&/TY-20261008/.test(e.files[0].name)&&!/ /.test(e.files[0].name),'CV file stored, name sanitised, prefixed by reference');ok(String(e.rows[0][25]).startsWith('https://drive.google.com'),'Drive link in the Sheet');ok(e.rows[0][2]==='candidate'&&e.rows[0][23]==='risk','journey and area stored');ok(e.rows[0][7]==='','no company for a candidate');const a=e.mails.find(m=>m.to==='p@mail.fr');ok(a&&/candidature/.test(a.body)&&!(a.opts&&a.opts.attachments),'acknowledgement of the application, no attachment');ok(!e.mails.some(m=>m.opts&&m.opts.attachments)&&!e.mails.some(m=>/cv_data/.test(JSON.stringify(m))),'CV content never mailed');const n=e.mails.find(m=>m.to==='contact@tyros-group.com');ok(/CANDIDATURE/.test(n.body)&&/drive.google.com/.test(n.body),'internal mail links to the private file and warns not to forward it');}
console.log('candidate: rejections');{const e=env(PC);ok(run(e,{...cand,consent:''}).error==='consent','consent required');ok(run(e,{...cand,cv_name:'cv.exe',cv_data:exe}).error==='cv','extension refused');ok(run(e,{...cand,cv_name:'cv.pdf',cv_data:exe}).error==='cv','fake pdf refused by signature');ok(run(e,{...cand,cv_data:Buffer.alloc(4*1024*1024+10,0x25).toString('base64')}).error==='cv_size','oversize refused');ok(run(e,{...cand,cv_name:'',cv_data:''}).error==='cv','missing CV refused');ok(run(e,{...cand,area:'x'}).error==='required','area whitelist');ok(e.files.length===0,'no file kept');}
console.log('\n'+(fails?fails+' FAILURES':'ALL PASSED'));process.exit(fails?1:0);
