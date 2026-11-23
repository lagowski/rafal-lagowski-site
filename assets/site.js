(function(){
  var body=document.body, root=document.documentElement, btns=document.querySelectorAll('.langs button');
  function setLang(l){
    body.className=l; root.lang=l;
    var t=root.getAttribute('data-title-'+l); if(t) document.title=t;
    btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l?'true':'false')});
    var cl=document.getElementById('clang'); if(cl) cl.value=l;
    try{localStorage.setItem('lagowski-lang',l)}catch(e){}
    document.dispatchEvent(new CustomEvent('langchange',{detail:l}));
  }
  document.addEventListener('langchange',function(e){document.querySelectorAll('option[data-'+e.detail+']').forEach(function(o){o.textContent=o.getAttribute('data-'+e.detail)})});
  setLang(window.__lang||'es');
  btns.forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.l)})});

  // phone menu: the nav is folded behind one button (only when JS runs; without it the nav stays open)
  var mb=document.querySelector('.menu-btn'), nav=document.getElementById('mainnav');
  if(mb&&nav){
    mb.addEventListener('click',function(){var o=mb.getAttribute('aria-expanded')!=='true';mb.setAttribute('aria-expanded',String(o));nav.classList.toggle('open',o)});
    nav.addEventListener('click',function(e){if(e.target.closest('a')){mb.setAttribute('aria-expanded','false');nav.classList.remove('open')}});
  }

  // contact form: works without JS (server redirects); with JS it posts in place
  var f=document.getElementById('cform'); if(!f) return;
  var st=document.getElementById('cstatus'), ct=document.getElementById('ct'), tp=document.getElementById('ctopic');
  ct.value=String(Date.now());
  try{var q=new URLSearchParams(location.search).get('topic'); if(q&&tp.querySelector('option[value="'+q+'"]')) tp.value=q}catch(e){}
  var M={sending:{en:'Sending…',es:'Enviando…',pl:'Wysyłanie…'},
    ok:{en:'Thank you. Your message is on its way; I reply within two working days.',es:'Gracias. Tu mensaje está en camino; respondo en dos días laborables.',pl:'Dziękuję. Wiadomość wysłana; odpowiem w ciągu dwóch dni roboczych.'},
    invalid:{en:'Please fill in your name, a valid email and a message of at least 10 characters.',es:'Completa tu nombre, un correo válido y un mensaje de al menos 10 caracteres.',pl:'Podaj imię, poprawny e-mail i wiadomość o długości co najmniej 10 znaków.'},
    rate:{en:'Too many messages right now. Please try again later or write on LinkedIn.',es:'Demasiados mensajes ahora mismo. Inténtalo más tarde o escríbeme por LinkedIn.',pl:'Zbyt wiele wiadomości. Spróbuj później albo napisz na LinkedIn.'},
    fail:{en:'The message could not be sent. Please try again in a few minutes or write on LinkedIn.',es:'No se pudo enviar el mensaje. Inténtalo en unos minutos o escríbeme por LinkedIn.',pl:'Nie udało się wysłać wiadomości. Spróbuj za kilka minut albo napisz na LinkedIn.'}};
  function say(k){st.textContent=(M[k][body.className]||M[k].en)}
  f.addEventListener('submit',function(ev){
    if(!window.fetch) return; ev.preventDefault();
    var b=f.querySelector('button[type=submit]'); b.disabled=true; say('sending');
    fetch(f.action,{method:'POST',headers:{'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()})
      .then(function(r){return r.json().catch(function(){return {ok:false,error:'fail'}})})
      .then(function(j){ if(j.ok){f.reset();ct.value=String(Date.now());say('ok')} else say(j.error==='invalid'?'invalid':j.error==='rate'?'rate':'fail'); b.disabled=false })
      .catch(function(){say('fail');b.disabled=false});
  });
})();
