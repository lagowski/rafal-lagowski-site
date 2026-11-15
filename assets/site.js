(function(){
  var body=document.body, root=document.documentElement, btns=document.querySelectorAll('.langs button');
  var msgs={es:['Dirección copiada','Selecciona y copia la dirección'],en:['Address copied','Select and copy the address'],pl:['Skopiowano adres','Zaznacz i skopiuj adres']};
  function setLang(l){
    body.className=l; root.lang=l;
    var t=root.getAttribute('data-title-'+l); if(t) document.title=t;
    btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l?'true':'false')});
    try{localStorage.setItem('lagowski-lang',l)}catch(e){}
    document.dispatchEvent(new CustomEvent('langchange',{detail:l}));
  }
  setLang(window.__lang||'en');
  btns.forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.l)})});
  var c=document.getElementById('copy');
  if(c) c.addEventListener('click',function(){
    var el=document.getElementById('addr'), out=document.getElementById('copied'), m=msgs[body.className]||msgs.en;
    function sel(){var r=document.createRange();r.selectNodeContents(el);var x=getSelection();x.removeAllRanges();x.addRange(r);out.textContent=' '+m[1]}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(el.textContent).then(function(){out.textContent=' '+m[0]},sel)} else sel();
  });
})();
