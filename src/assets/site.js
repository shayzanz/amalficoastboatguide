(function(){
var KEY='acbg-consent';
function get(){try{return localStorage.getItem(KEY)}catch(e){return null}}
function set(v){try{localStorage.setItem(KEY,v)}catch(e){}}
var btn=document.querySelector('.menu-btn'),nav=document.getElementById('mainnav');
if(btn&&nav)btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
/* GetYourGuide widget, loaded only after consent */
var gygLoaded=false;
function loadGYG(){
  document.querySelectorAll('.gyg-wrap').forEach(function(w){
    if(w.dataset.done)return;w.dataset.done=1;
    var d=document.createElement('div');
    d.setAttribute('data-gyg-href','https://widget.getyourguide.com/default/activities.frame');
    d.setAttribute('data-gyg-locale-code',w.dataset.locale);
    d.setAttribute('data-gyg-widget','activities');
    d.setAttribute('data-gyg-number-of-items',w.dataset.n||'3');
    d.setAttribute('data-gyg-cmp',w.dataset.cmp||'');
    d.setAttribute('data-gyg-partner-id',window.GYG_PID);
    if(w.dataset.ids)d.setAttribute('data-gyg-tour-ids',w.dataset.ids);else d.setAttribute('data-gyg-q',w.dataset.q);
    var tpl=w.querySelector('template.viator-tpl');
    w.innerHTML='';w.appendChild(d);
    if(tpl){var v=document.createElement('div');v.className='viator-wrap';v.appendChild(tpl.content.cloneNode(true));w.appendChild(v);
      v.querySelectorAll('script').forEach(function(o){var n=document.createElement('script');for(var i=0;i<o.attributes.length;i++)n.setAttribute(o.attributes[i].name,o.attributes[i].value);n.text=o.text;o.replaceWith(n)})}
  });
  if(gygLoaded)return;gygLoaded=true;
  var s=document.createElement('script');s.async=true;s.defer=true;
  s.src='https://widget.getyourguide.com/dist/pa.umd.production.min.js';
  s.setAttribute('data-gyg-partner-id',window.GYG_PID);document.body.appendChild(s);
}
var banner=document.querySelector('.consent');
function hide(){if(banner)banner.hidden=true}
var c=get();
if(c==='yes')loadGYG();else if(!c&&banner)banner.hidden=false;
document.addEventListener('click',function(e){
  var t=e.target;
  if(t.closest('.js-consent-yes')){set('yes');hide();loadGYG()}
  else if(t.closest('.js-consent-no')){set('no');hide()}
  else if(t.closest('.js-gyg-accept')){set('yes');hide();loadGYG()}
  else if(t.closest('.js-consent-reset')){e.preventDefault();try{localStorage.removeItem(KEY)}catch(x){}if(banner)banner.hidden=false}
});
/* Comparator */
var data=document.getElementById('tour-data');
if(data){
  var tours=JSON.parse(data.textContent),ui=JSON.parse(document.getElementById('ui-data').textContent),
      grotto=JSON.parse(document.getElementById('grotto-label').textContent),
      form=document.getElementById('filters'),out=document.getElementById('results'),count=document.getElementById('count');
  function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function render(){
    var f=new FormData(form),from=f.get('from'),type=f.get('type'),dur=f.get('dur'),sort=f.get('sort');
    var list=tours.filter(function(t){
      if(from&&t.from.indexOf(from)<0)return false;
      if(type==='private'&&!t.private)return false;if(type==='shared'&&t.private)return false;
      if(dur&&t.h1>+dur)return false;
      if(f.get('capri')&&!t.capri)return false;if(f.get('grotto')&&!t.grotto)return false;if(f.get('kids')&&!t.kids)return false;
      return true});
    list.sort(function(a,b){
      if(sort==='price')return (a.unit==='pp'?a.lo:a.lo/6)-(b.unit==='pp'?b.lo:b.lo/6);
      if(sort==='dur')return a.h1-b.h1;return b.score-a.score});
    count.textContent=list.length?list.length+' '+ui.results:ui.no_results;
    out.innerHTML=list.map(function(t){
      var tags='<span class="tag">'+esc(t.private?ui.private:ui.shared)+'</span>'+(t.capri?'<span class="tag">Capri</span>':'')+(t.grotto?'<span class="tag">'+esc(grotto)+'</span>':'');
      return '<article class="card"><a class="card-img '+(t.img?'':t.ph)+'"'+(t.img?' style="background-image:url(\''+esc(t.img)+'\')"':'')+' href="'+t.url+'"><span class="score" title="'+esc(ui.our_score)+'">'+t.score.toFixed(1)+'</span></a><div class="card-body"><div class="card-top">'+tags+'</div>'+
      '<h3><a href="'+t.url+'">'+esc(t.name)+'</a></h3><p>'+esc(t.short)+'</p><ul class="facts">'+
      '<li><span>'+esc(ui.from)+'</span>'+esc(t.fromLabel)+'</li><li><span>'+esc(ui.duration)+'</span>'+esc(t.dur)+'</li><li><span>'+esc(ui.typical_price)+'</span>'+esc(t.price)+'</li></ul>'+
      '<div class="cta-row"><a class="btn btn-ghost" href="'+t.url+'">'+esc(ui.details)+'</a>'+t.partners.slice(0,1).map(function(p,i){return '<a class="btn '+(i?'btn-secondary':'btn-primary')+' btn-partner" rel="sponsored nofollow noopener" target="_blank" href="'+esc(p[1])+'">'+esc(i?ui.compare_prices:ui.book_now)+'<small>'+esc(ui.via)+' '+esc(p[0])+'</small></a>'}).join('')+'</div></div></article>'}).join('');
  }
  form.addEventListener('change',render);render();
}
/* Route map */
var m=document.getElementById('map');
if(m&&window.L){
  var pts=JSON.parse(m.dataset.route),ll=pts.map(function(p){return[p[0],p[1]]});
  m.innerHTML='';var map=L.map(m,{scrollWheelZoom:false});
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:17,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
  L.polyline(ll,{color:'#e76f51',weight:4,dashArray:'8 8'}).addTo(map);
  var seen={};pts.forEach(function(p){if(p[2]&&!seen[p[2]]){seen[p[2]]=1;L.circleMarker([p[0],p[1]],{radius:7,color:'#0b4f6c',fillColor:'#fff',fillOpacity:1,weight:3}).addTo(map).bindTooltip(p[2])}});
  map.fitBounds(L.latLngBounds(ll),{padding:[20,20]});
}
})();
