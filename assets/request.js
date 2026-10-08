/* Tyros Group: the single contact form.
   Messages and labels come from the page itself (#req-config), so each language page is self-contained.
   The endpoint is a Google Apps Script web app that e-mails the request to Tyros. Its URL is public by design and carries no secret.
   Replace the placeholder after deployment (see tools/apps-script/README.md). */
(function(){
  'use strict';
  var ENDPOINT='https://script.google.com/macros/s/__DEPLOY_ID__/exec';
  var EP=function(){return window.__ENDPOINT||ENDPOINT;};
  var d=document,cfgEl=d.getElementById('req-config');
  if(!cfgEl)return;
  var cfg=JSON.parse(cfgEl.textContent),q=new URLSearchParams(window.__REQ||location.search);
  var forms=[].slice.call(d.querySelectorAll('.req-form'));
  var lang=d.documentElement.lang==='en'?'en':'fr';
  var offer=q.get('offer')||'',intent=q.get('intent')||'';
  if(offer&&!cfg.offers[offer])offer='';
  if(intent!=='programme'&&intent!=='session')intent='';
  var from=(q.get('from')||'').replace(/[^\w\-\/\.]/g,'').slice(0,160);
  var pagePath=from||location.pathname;
  var t0=Date.now();

  function subject(){
    if(!offer)return cfg.default_subject;
    var o=cfg.offers[offer],label=o.label;
    if(o.kind==='plain')return label;
    var pre=(o.kind==='academy'&&intent)?cfg.prefix[intent]:cfg.prefix[o.kind];
    return pre+' : '+label;
  }
  function $(s,r){return (r||d).querySelector(s);}
  forms.forEach(function(f){
    f.elements.offer.value=offer;f.elements.intent.value=intent;f.elements.page.value=pagePath;f.elements.t0.value=String(t0);
    if(f.closest('.req-panels'))f.elements.subject.value=subject();   // the home form keeps the general subject
  });

  function fieldOf(el){return el.closest('.fld');}
  function showErr(el,msg){var f=fieldOf(el);if(!f)return;f.classList.add('bad');var e=$('.fld-err',f);if(e)e.textContent=msg;el.setAttribute('aria-invalid','true');}
  function clearErr(el){var f=fieldOf(el);if(!f)return;f.classList.remove('bad');var e=$('.fld-err',f);if(e)e.textContent='';el.removeAttribute('aria-invalid');}
  var emailRe=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validate(f){
    var first=null,ok=true;
    [].slice.call(f.elements).forEach(function(el){
      if(!el.name||el.type==='hidden'||el.name==='website'||el.tagName==='BUTTON')return;
      var v=(el.value||'').trim();clearErr(el);
      if(el.required&&!v){showErr(el,cfg.err_required);ok=false;first=first||el;}
      else if(el.type==='email'&&v&&!emailRe.test(v)){showErr(el,cfg.err_email);ok=false;first=first||el;}
    });
    if(first)first.focus();
    return ok;
  }
  function status(f,msg,bad){var s=$('.req-status',f);s.textContent=msg||'';s.classList.toggle('bad',!!bad);}
  function success(f){
    var ok=$('.req-ok',f.closest('.req-wrap')||f.parentNode);
    if(!ok)ok=$('.req-ok');
    if(ok){
      var panels=f.closest('.req-panels');if(panels)panels.hidden=true;else f.hidden=true;
      ok.hidden=false;ok.focus();
      ok.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    }
    try{(window.dataLayer=window.dataLayer||[]).push({event:'contact_submitted',contact_offer:offer||undefined,contact_lang:lang});}catch(e){}
  }
  forms.forEach(function(f){
    f.addEventListener('input',function(e){if(e.target.name)clearErr(e.target);});
    f.addEventListener('submit',function(e){
      e.preventDefault();status(f,'');
      if(!validate(f))return;
      var btn=$('.req-send',f);
      if(EP().indexOf('__DEPLOY_ID__')>-1){status(f,cfg.err_send,true);return;}
      btn.disabled=true;btn.textContent=btn.dataset.sending;f.setAttribute('aria-busy','true');
      var data=new URLSearchParams();
      [].slice.call(f.elements).forEach(function(el){if(el.name&&el.tagName!=='BUTTON')data.set(el.name,el.value);});
      data.set('source_url',location.href);
      fetch(EP(),{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body:data.toString()})
        .then(function(r){return r.json();})
        .then(function(j){if(j&&j.ok)success(f);else throw new Error(j&&j.error||'error');})
        .catch(function(){status(f,cfg.err_send,true);})
        .then(function(){btn.disabled=false;btn.textContent=btn.dataset.label;f.removeAttribute('aria-busy');});
    });
  });
})();
