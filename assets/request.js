/* Tyros Group: request forms (recruitment, consulting, academy, general).
   Messages and labels come from the page itself (#req-config), so each language page is self-contained.
   The endpoint is a Google Apps Script web app: its URL is public by design and carries no secret.
   Replace the placeholder after deployment (see tools/apps-script/README.md). */
(function(){
  'use strict';
  var ENDPOINT='https://script.google.com/macros/s/__DEPLOY_ID__/exec';
  var d=document,cfgEl=d.getElementById('req-config');
  if(!cfgEl)return;
  var cfg=JSON.parse(cfgEl.textContent),q=new URLSearchParams(location.search);
  var forms=[].slice.call(d.querySelectorAll('.req-form'));
  var lang=d.documentElement.lang==='en'?'en':'fr';
  var isPage=!!d.querySelector('.req-panels');
  var offer=q.get('offer')||'',intent=q.get('intent')||'';
  if(offer&&!cfg.offers[offer])offer='';
  if(intent!=='programme'&&intent!=='session')intent='';
  var type=q.get('type');
  if(['general','recruitment','consulting','academy'].indexOf(type)<0)type=offer?cfg.offers[offer].type:'general';
  var from=(q.get('from')||'').replace(/[^\w\-\/\.]/g,'').slice(0,160);
  var pagePath=from||location.pathname;
  var t0=Date.now();

  function $(s,r){return (r||d).querySelector(s);}
  function setHidden(f,n,v){var e=f.elements[n];if(e)e.value=v;}

  function prep(f){
    setHidden(f,'offer',offer&&cfg.offers[offer].type===f.dataset.type?offer:'');
    setHidden(f,'intent',f.dataset.type==='academy'?intent:'');
    setHidden(f,'page',pagePath);
    setHidden(f,'t0',String(t0));
    if(f.dataset.type==='academy'&&offer&&cfg.offers[offer].type==='academy'){
      var s=f.elements.programme;if(s)s.value=offer;
    }
  }
  forms.forEach(prep);

  if(isPage){
    d.querySelectorAll('.req-sec').forEach(function(s){s.hidden=s.dataset.type!==type;});
    d.querySelectorAll('.req-tabs a').forEach(function(a){
      var on=a.dataset.tab===type;a.classList.toggle('on',on);
      if(on)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');
      if(from)a.href=a.href+'&from='+encodeURIComponent(from);
    });
    var key=type==='academy'&&intent?intent:type;
    $('#req-h1').textContent=cfg.h1[key];
    $('#req-lede').textContent=cfg.lede[key];
    var send=$('.req-sec:not([hidden]) .req-send');if(send){send.textContent=cfg.send[key];send.dataset.label=cfg.send[key];}
    if(offer){var c=$('#req-ctx');c.hidden=false;$('strong',c).textContent=cfg.offers[offer].label;}
  }

  function fieldOf(el){return el.closest('.fld');}
  function showErr(el,msg){
    var f=fieldOf(el);if(!f)return;f.classList.add('bad');
    var e=$('.fld-err',f);if(e)e.textContent=msg;
    el.setAttribute('aria-invalid','true');
  }
  function clearErr(el){
    var f=fieldOf(el);if(!f)return;f.classList.remove('bad');
    var e=$('.fld-err',f);if(e)e.textContent='';
    el.removeAttribute('aria-invalid');
  }
  var emailRe=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validate(f){
    var first=null,ok=true;
    [].slice.call(f.elements).forEach(function(el){
      if(!el.name||el.type==='hidden'||el.name==='website')return;
      if(el.type==='radio'){
        var group=f.querySelectorAll('input[name="'+el.name+'"]');
        if(el!==group[0])return;
        var any=[].some.call(group,function(r){return r.checked;});
        var fs=el.closest('.fld');if(fs){fs.classList.toggle('bad',!any);var er=$('.fld-err',fs);if(er)er.textContent=any?'':cfg.err_required;}
        if(!any&&group[0].required){ok=false;first=first||group[0];}
        return;
      }
      var v=(el.value||'').trim();clearErr(el);
      if(el.required&&!v){showErr(el,cfg.err_required);ok=false;first=first||el;}
      else if(el.type==='email'&&v&&!emailRe.test(v)){showErr(el,cfg.err_email);ok=false;first=first||el;}
    });
    if(first)first.focus();
    return ok;
  }

  function status(f,msg,bad){var s=$('.req-status',f);s.textContent=msg||'';s.classList.toggle('bad',!!bad);}

  function success(f,ref,body){
    var ok=$('.req-ok');
    if(ok){
      $('.ok-ref strong',ok).textContent=ref||'';
      $('.ok-ref',ok).hidden=!ref;
      if(isPage){d.querySelector('.req-panels').hidden=true;var t=$('.req-tabs');if(t)t.hidden=true;var c=$('#req-ctx');if(c)c.hidden=true;}
      else f.hidden=true;
      ok.hidden=false;ok.focus();
      ok.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    }
    try{(window.dataLayer=window.dataLayer||[]).push({event:'request_submitted',request_type:f.dataset.type,request_offer:f.elements.offer.value||undefined,request_lang:lang});}catch(e){}
  }

  forms.forEach(function(f){
    f.addEventListener('input',function(e){if(e.target.name)clearErr(e.target);});
    f.addEventListener('submit',function(e){
      e.preventDefault();
      status(f,'');
      if(!validate(f))return;
      var btn=$('.req-send',f);
      if(ENDPOINT.indexOf('__DEPLOY_ID__')>-1){status(f,cfg.err_send,true);return;}
      btn.disabled=true;btn.textContent=btn.dataset.sending;f.setAttribute('aria-busy','true');
      var data=new URLSearchParams(new FormData(f));
      data.set('source_url',location.href);
      fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body:data.toString()})
        .then(function(r){return r.json();})
        .then(function(j){
          if(j&&j.ok){success(f,j.ref);}
          else{throw new Error(j&&j.error||'error');}
        })
        .catch(function(){status(f,cfg.err_send,true);})
        .then(function(){btn.disabled=false;btn.textContent=btn.dataset.label;f.removeAttribute('aria-busy');});
    });
  });
})();
