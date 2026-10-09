/* Tyros Group: shared behaviour. No translation logic: each language is its own page. */
(function(){
  var d=document,root=d.documentElement,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* MOBILE NAV */
  var nt=d.getElementById('nav-toggle'),nm=d.getElementById('mobile-nav');
  if(nt&&nm){
    var close=function(){nm.hidden=true;nt.setAttribute('aria-expanded','false');};
    nt.addEventListener('click',function(){var o=nm.hidden;nm.hidden=!o;nt.setAttribute('aria-expanded',o?'true':'false');});
    nm.querySelectorAll('a').forEach(function(a){a.addEventListener('click',close);});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!nm.hidden){close();nt.focus();}});
  }

  /* REVEAL (one observer, transform/opacity only; instant when motion is reduced) */
  var els=d.querySelectorAll('.reveal, .sec, .divi, .ind, .ins');
  els.forEach(function(e){e.classList.add('reveal');});
  if(!reduce&&'IntersectionObserver'in window){
    var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
    els.forEach(function(e){io.observe(e);});
  }else els.forEach(function(e){e.classList.add('in');});

  /* COUNT-UP (hero figures) */
  var strip=d.querySelector('.hero-stats,.stats');
  if(strip&&!reduce){
    var done=false,run=function(){
      if(done)return;done=true;
      d.querySelectorAll('.stat .v[data-count]').forEach(function(el){
        var end=+el.getAttribute('data-count'),u=el.querySelector('.u'),suf=u?u.outerHTML:'',cur=0,step=Math.max(1,Math.round(end/40));
        var iv=setInterval(function(){cur+=step;if(cur>=end){cur=end;clearInterval(iv);}el.innerHTML=cur+suf;},22);
      });
    };
    if('IntersectionObserver'in window){var so=new IntersectionObserver(function(e){if(e[0].isIntersecting){run();so.disconnect();}},{threshold:.4});so.observe(strip);}else run();
  }

  /* CONSENT: Google Tag Manager (audience measurement) loads only after an explicit "Accept". Refusing is as easy as accepting. */
  var GTM_ID='GTM-PJW2HKZN',KEY='tyros_consent',lang=d.documentElement.lang==='en'?'en':'fr';
  var TXT={fr:{t:'Mesure d’audience',p:'Nous utilisons Google Tag Manager pour mesurer l’audience du site, seulement avec votre accord. Vous pouvez refuser aussi simplement qu’accepter, et changer d’avis à tout moment.',a:'Accepter',r:'Refuser',l:'Politique de confidentialité',u:'/confidentialite/'},
           en:{t:'Audience measurement',p:'We use Google Tag Manager to measure site audience, only with your agreement. You can refuse as easily as accept, and change your mind at any time.',a:'Accept',r:'Refuse',l:'Privacy policy',u:'/en/privacy-policy/'}}[lang];
  function get(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function set(v){try{localStorage.setItem(KEY,v);}catch(e){}}
  function loadGtm(){
    if(window.__gtmLoaded)return;window.__gtmLoaded=true;
    window.dataLayer=window.dataLayer||[];window.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});
    var s=d.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtm.js?id='+GTM_ID;d.head.appendChild(s);
  }
  function banner(){
    var old=d.getElementById('consent');if(old)old.remove();
    var b=d.createElement('div');b.id='consent';b.setAttribute('role','dialog');b.tabIndex=-1;b.setAttribute('aria-labelledby','consent-t');
    b.innerHTML='<div class="consent-in"><div><strong id="consent-t">'+TXT.t+'</strong><p>'+TXT.p+' <a href="'+TXT.u+'">'+TXT.l+'</a>.</p></div><div class="consent-btns"><button type="button" class="btn btn-ghost" data-c="denied">'+TXT.r+'</button><button type="button" class="btn btn-ghost" data-c="granted">'+TXT.a+'</button></div></div>';
    d.body.appendChild(b);
    b.querySelectorAll('button').forEach(function(x){x.addEventListener('click',function(){set(x.dataset.c);b.remove();if(x.dataset.c==='granted')loadGtm();});});
    b.focus({preventScroll:true});
  }
  var c=get();
  if(c==='granted')loadGtm();else if(!c)banner();
  var cs=d.getElementById('cookie-settings');if(cs)cs.addEventListener('click',banner);
})();
