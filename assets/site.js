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
  var els=d.querySelectorAll('.reveal, .sec, .divi, .ind, .mem, .ins');
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
})();
