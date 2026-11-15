(function(){
var $=function(id){return document.getElementById(id)};
function lang(){var c=document.body.className;return c==='es'||c==='pl'?c:'en'}
/* ---- demo 1 ---- */
var RES={
 bad:{es:['Posible práctica prohibida','Detén el despliegue y consulta con un especialista jurídico antes de seguir. Las excepciones son muy limitadas.'],en:['Possible prohibited practice','Stop the rollout and consult a legal specialist before continuing. Exceptions are very narrow.'],pl:['Możliwa praktyka zakazana','Wstrzymaj wdrożenie i skonsultuj się ze specjalistą prawnym. Wyjątki są bardzo wąskie.'],c:'bad'},
 high:{es:['Probable sistema de alto riesgo','Suele exigir gestión de riesgos, documentación técnica, registro de actividad, supervisión humana y evaluación de conformidad. Es el caso en el que más compensa un diagnóstico.','' ],en:['Likely high-risk system','This usually requires risk management, technical documentation, activity logging, human oversight and a conformity assessment. This is where a diagnostic pays off most.'],pl:['Prawdopodobny system wysokiego ryzyka','Zwykle wymaga zarządzania ryzykiem, dokumentacji technicznej, rejestrowania zdarzeń, nadzoru ludzkiego i oceny zgodności. To przypadek, w którym diagnostyka opłaca się najbardziej.'],c:'warn'},
 tr:{es:['Obligaciones de transparencia','Hay que informar a la persona de que interactúa con una IA y etiquetar el contenido sintético, según el caso.'],en:['Transparency obligations','People must be told they are interacting with an AI and synthetic content must be labelled, depending on the case.'],pl:['Obowiązki przejrzystości','Trzeba poinformować osobę, że rozmawia z AI, i oznaczać treści syntetyczne, zależnie od przypadku.'],c:'info'},
 min:{es:['Riesgo mínimo con estas respuestas','No aparecen obligaciones especiales con lo marcado. Mantén un inventario y revisa si cambia el uso del sistema.'],en:['Minimal risk on these answers','No special obligations appear from what you ticked. Keep an inventory and review if the use changes.'],pl:['Minimalne ryzyko przy tych odpowiedziach','Przy zaznaczonych odpowiedziach nie widać szczególnych obowiązków. Prowadź inwentarz i sprawdzaj, czy zmienia się sposób użycia.'],c:'ok'}
};
function risk(){
  var on={};document.querySelectorAll('#rq input').forEach(function(i){if(i.checked)on[i.dataset.r]=1});
  var k='min';
  if(on.t1||on.t2)k='tr';
  if(on.h1||on.h2||on.h3||on.h4||on.h5)k='high';
  if(on.p1||on.p2)k='bad';
  var r=RES[k],t=r[lang()];
  $('rres').innerHTML='<span class="lvl '+r.c+'">'+k.toUpperCase()+'</span><b>'+t[0]+'</b>'+t[1];
}
document.querySelectorAll('#rq input').forEach(function(i){i.addEventListener('change',risk)});
/* ---- demo 2 ---- */
var DOCS={
 es:[['Política de vacaciones, art. 2','Cada empleado tiene 23 días laborables de vacaciones al año. Las solicitudes se envían al responsable con 15 días de antelación.'],['Gastos de viaje, art. 4','Los gastos de viaje se reembolsan en 30 días con factura. El hotel tiene un límite de 120 euros por noche.'],['Teletrabajo, art. 1','Se puede teletrabajar hasta dos días por semana previo acuerdo con el responsable. El equipo de la empresa se usa solo para fines laborales.'],['Seguridad, art. 6','Los datos de clientes no se suben a herramientas de IA externas no aprobadas. Cualquier duda se consulta con el equipo de seguridad.']],
 en:[['Vacation policy, art. 2','Each employee has 23 working days of leave per year. Requests are sent to the line manager 15 days in advance.'],['Travel expenses, art. 4','Travel expenses are reimbursed within 30 days with a receipt. Hotels are capped at 120 euros per night.'],['Remote work, art. 1','Remote work is allowed up to two days a week by agreement with the manager. Company equipment is used for work purposes only.'],['Security, art. 6','Customer data must not be uploaded to unapproved external AI tools. Any doubt goes to the security team.']],
 pl:[['Polityka urlopowa, art. 2','Każdy pracownik ma 23 dni robocze urlopu w roku. Wnioski składa się do przełożonego z 15-dniowym wyprzedzeniem.'],['Koszty podróży, art. 4','Koszty podróży są zwracane w ciągu 30 dni na podstawie faktury. Hotel ma limit 120 euro za noc.'],['Praca zdalna, art. 1','Praca zdalna jest możliwa do dwóch dni w tygodniu za zgodą przełożonego. Sprzęt firmowy służy wyłącznie do celów służbowych.'],['Bezpieczeństwo, art. 6','Danych klientów nie wolno wprowadzać do niezatwierdzonych zewnętrznych narzędzi AI. Wątpliwości zgłasza się zespołowi bezpieczeństwa.']]
};
var PRE={es:['¿Cuántos días de vacaciones tengo?','¿Cuánto puedo gastar en un hotel?','¿Puedo teletrabajar tres días?','¿Cuánto cobra el director?','¿Puedo pegar datos de clientes en ChatGPT?'],en:['How many vacation days do I get?','How much can I spend on a hotel?','Can I work remotely three days?','What is the CEO\'s salary?','Can I paste customer data into ChatGPT?'],pl:['Ile dni urlopu mam?','Ile mogę wydać na hotel?','Czy mogę pracować zdalnie trzy dni?','Ile zarabia prezes?','Czy mogę wkleić dane klientów do ChatGPT?']};
var STOP={es:'cuanto cuantos cuanta como cual donde puedo tengo tiene para con una unos unas los las del por que'.split(' '),en:'how much many what can the and for with from has have does into are is my our'.split(' '),pl:'ile czy mam moge jaka jest jak dla nie sie przez'.split(' ')};
var NO={es:['No lo encuentro en los documentos','Lo paso a una persona en lugar de inventar una respuesta.'],en:['I cannot find this in the documents','I am handing it to a person instead of making up an answer.'],pl:['Nie znajduję tego w dokumentach','Przekazuję sprawę człowiekowi zamiast zgadywać.']};
var SRC={es:'Fuente',en:'Source',pl:'Źródło'};
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/ł/g,'l')}
function toks(s,l){return norm(s).split(/[^a-z0-9]+/).filter(function(w){return w.length>=3&&STOP[l].indexOf(w)<0}).map(function(w){return w.slice(0,5)})}
function ask(q){
  var l=lang(),qt=toks(q,l),best=-1,bi=-1;
  DOCS[l].forEach(function(d,i){var dt=toks(d[0]+' '+d[1],l),s=0;qt.forEach(function(t){if(dt.indexOf(t)>=0)s++});if(s>best){best=s;bi=i}});
  var out=$('ares');
  if(!q.trim()){out.innerHTML='';return}
  if(best<1){out.innerHTML='<span class="lvl warn">'+(l==='es'?'Derivado':l==='en'?'Escalated':'Przekazane')+'</span><b>'+NO[l][0]+'</b>'+NO[l][1];return}
  var d=DOCS[l][bi];
  out.innerHTML='<b>'+d[1]+'</b><div class="src">'+SRC[l]+': '+d[0]+'</div>';
}
function drawDocs(){
  var l=lang();
  $('adocs').innerHTML=DOCS[l].map(function(d){return '<div><b>'+d[0]+'</b>: '+d[1]+'</div>'}).join('');
  $('presets').innerHTML='';
  PRE[l].forEach(function(p){var b=document.createElement('button');b.type='button';b.textContent=p;b.addEventListener('click',function(){$('askq').value=p;ask(p)});$('presets').appendChild(b)});
  $('askq').placeholder=PRE[l][0];
  ask($('askq').value);
}
$('askf').addEventListener('submit',function(e){e.preventDefault();ask($('askq').value)});
/* ---- demo 3 ---- */
var BV=[{n:9.3,f:99.6},{n:15.1,f:56.8},{n:19.9,f:21.0}];
var BL={es:['nacionales','extranjeros'],en:['national','foreign'],pl:['obywatele','cudzoziemcy']};
var BT={
 es:['B1: etiquetas sesgadas y nacionalidad como variable. El modelo marca a casi todos los extranjeros.','B2: sin la columna nacionalidad, pero queda una variable correlacionada. El sesgo baja, no desaparece.','B3: entrenado con una muestra aleatoria de controles y sin variable proxy. Los dos grupos se marcan casi igual.'],
 en:['B1: biased labels and nationality as a feature. The model flags almost every foreign household.','B2: nationality column removed, but a correlated variable remains. The bias drops, it does not disappear.','B3: trained on a random sample of audits and with no proxy variable. Both groups are flagged almost equally.'],
 pl:['B1: stronnicze etykiety i narodowość jako cecha. Model oznacza niemal wszystkie gospodarstwa cudzoziemców.','B2: bez kolumny narodowość, ale zostaje skorelowana zmienna. Stronniczość maleje, ale nie znika.','B3: uczony na losowej próbie kontroli i bez zmiennej zastępczej. Obie grupy są oznaczane prawie tak samo.']
};
var bsel=0;
function drawB(){
  var l=lang(),v=BV[bsel],r=v.f/v.n;
  $('bbars').innerHTML='<div class="bar"><span>'+BL[l][0]+'</span><i style="width:'+v.n+'%"></i><span>'+v.n.toFixed(1)+'%</span></div><div class="bar"><span>'+BL[l][1]+'</span><i class="f" style="width:'+v.f+'%"></i><span>'+v.f.toFixed(1)+'%</span></div>';
  $('bres').innerHTML='<b>'+(l==='es'?'Relación entre grupos':l==='en'?'Ratio between groups':'Stosunek między grupami')+': '+r.toFixed(1)+'×</b>'+BT[l][bsel];
}
document.querySelectorAll('#bseg button').forEach(function(b){b.addEventListener('click',function(){bsel=+b.dataset.v;document.querySelectorAll('#bseg button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});drawB()})});
/* ---- demo 4 ---- */
var CL={es:['Contacto aleatorio','Regla: menor ingreso','Modelo','elegibles encontrados'],en:['Random outreach','Rule: lowest income','Model','eligible households found'],pl:['Losowe docieranie','Reguła: najniższy dochód','Model','znalezionych uprawnionych']};
function drawS(){
  var n=+$('nrange').value,l=lang();$('nval').textContent=n.toLocaleString(l);
  var p=[.083,.85,.852];
  $('cmp').innerHTML=p.map(function(x,i){return '<div><b class="big-n">'+Math.round(n*x).toLocaleString(l)+'</b><small>'+CL[l][i]+' · '+CL[l][3]+'</small></div>'}).join('');
}
$('nrange').addEventListener('input',drawS);
function all(){risk();drawDocs();drawB();drawS()}
document.addEventListener('langchange',all);
all();
})();
