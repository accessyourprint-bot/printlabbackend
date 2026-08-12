const API = window.location.origin;
const TC = {Bw:'#3b82f6',Colour:'#f97316',Photo:'#10b981',Tshirt:'#8b5cf6',Project:'#ef4444'};
const TN = ['Bw','Colour','Photo','Tshirt','Project'];
const TL = {Bw:'B/W',Colour:'Colour',Photo:'Photo',Tshirt:'T-Shirt',Project:'Project'};

let tok = localStorage.getItem('pl_s');
let curShop = null;
let allOrds = [];
let shDat = {};
let shCh = null;
let curSHT = 'all';
let curTK = 'customer';

if(tok) initD();

async function doLogin(){
  const em = document.getElementById('em').value;
  const pw = document.getElementById('pw').value;
  try{
    const r = await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em,password:pw})});
    const d = await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);initD();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect to server';}
}

function doLogout(){localStorage.removeItem('pl_s');location.reload();}

async function initD(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('dw').classList.remove('hidden');
  try{
    const d = await api('/api/v1/shops');
    const s = Array.isArray(d)?d:(d.data||[]);
    if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
  }catch(e){}
  loadJ();
  setInterval(loadJ,15000);
}

async function api(u,m,b){
  const o={method:m||'GET',headers:{Authorization:'Bearer '+tok}};
  if(b){o.headers['Content-Type']='application/json';o.body=JSON.stringify(b);}
  return (await fetch(API+u,o)).json();
}

function gT(o){
  const s=JSON.stringify(o).toLowerCase();
  if(s.includes('colour')||s.includes('color'))return'Colour';
  if(s.includes('photo'))return'Photo';
  if(s.includes('tshirt')||s.includes('t-shirt'))return'Tshirt';
  if(s.includes('project'))return'Project';
  return'Bw';
}

function stC(s){return{pending:'st-pending',confirmed:'st-confirmed',completed:'st-completed',cancelled:'st-cancelled'}[s]||'st-pending';}
function stL(s){return(s||'pending').charAt(0).toUpperCase()+(s||'pending').slice(1);}

async function loadJ(){
  try{
    const d = await api('/api/v1/orders');
    allOrds = Array.isArray(d)?d:(d.items||d.data||d.orders||[]);
    rJ(allOrds);
  }catch(e){document.getElementById('jl').innerHTML='<div class="empty">Error loading orders</div>';}
}

async function dlFile(fileId, filename){
  try{
    const r = await fetch(API + '/api/v1/files/' + fileId + '/download', {headers:{Authorization:'Bearer '+tok}});
    if(!r.ok){ alert('Download failed'); return; }
    const blob = await r.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'file';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  }catch(e){ alert('Download failed'); }
}
function fj(t,el){
  document.querySelectorAll('.ttab').forEach(x=>x.classList.remove('on'));
  el.classList.add('on');
  if(t==='all'){rJ(allOrds);return;}
  const m={bw:'black_white',colour:'colour',photo:'photo',tshirt:'tshirt',project:'project'};
  rJ(allOrds.filter(o=>JSON.stringify(o).toLowerCase().includes(m[t]||t)));
}

function rJ(jobs){
  if(!jobs.length){document.getElementById('jl').innerHTML='<div class="empty">No active jobs</div>';return;}
  const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  document.getElementById('jl').innerHTML=jobs.map(o=>{
    const dt=new Date(o.created_at);
    const ds=dt.getDate()+' '+MN[dt.getMonth()]+', '+dt.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'});
    return '<div class="ji"><div class="ji-top"><span class="ji-id">'+(o.order_number||o.id?.slice(0,12)||'&mdash;')+'</span><span class="ji-st '+stC(o.status)+'">'+stL(o.status)+'</span></div><div class="ji-name">'+(o.user_name||o.customer_name||'Customer')+'</div><div class="ji-phone">'+(o.user_phone||o.customer_phone||'')+'</div><div class="ji-bot">'+((o.files&&o.files.length)?o.files.map(function(f){return '<span class="ji-file" style="cursor:pointer;text-decoration:underline" onclick="event.stopPropagation();dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/"/g,'')+'&quot;)">&#8595; '+(f.original_filename||'document.pdf')+'</span>';}).join(''):'<span class="ji-file">&#8595; No file</span>')+'<span class="ji-copies">x'+(o.copies||1)+'</span><span class="ji-type">'+TL[gT(o)]+'</span><span class="ji-date">'+ds+'</span></div></div>';
  }).join('');
}

/* DROPDOWNS */
function toggleSD(){document.getElementById('sdrop').classList.toggle('hidden');}
function closeSD(){document.getElementById('sdrop').classList.add('hidden');}
function toggleTD(){document.getElementById('tdrop').classList.toggle('hidden');}
function closeTD(){document.getElementById('tdrop').classList.add('hidden');}
document.addEventListener('click',function(e){
  if(!e.target.closest('#siBtn'))document.getElementById('sdrop').classList.add('hidden');
  if(!e.target.closest('#tBtn'))document.getElementById('tdrop').classList.add('hidden');
});

/* MODALS */
function oMo(id){document.getElementById(id).classList.remove('hidden');}
function cMo(id){document.getElementById(id).classList.add('hidden');}

/* DELIVERY TEAM */
async function openDT(){
  oMo('dtMo');
  if(curShop)document.getElementById('dtSub').textContent='People assigned to '+curShop.name+'.';
  try{
    const d = await api('/api/v1/delivery-persons');
    const ag = Array.isArray(d)?d:(d.data||[]);
    document.getElementById('dtB').innerHTML=ag.length
      ?ag.map(a=>'<div class="ag"><div class="av">&#128100;</div><div><div class="an">'+a.name+'</div><div class="aa">'+(a.age?'Age '+a.age:'')+'</div><div class="ai"><span>&#128222; '+(a.phone||'&mdash;')+'</span><span>&#128661; '+(a.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      :'<div class="empty">No delivery persons yet</div>';
  }catch(e){document.getElementById('dtB').innerHTML='<div class="empty">Error loading</div>';}
}

function openAA(){
  cMo('dtMo');
  ['aNm','aAge','aPh','aVeh'].forEach(id=>document.getElementById(id).value='');
  oMo('aaMo');
}

async function subAA(){
  const nm=document.getElementById('aNm').value,ph=document.getElementById('aPh').value;
  if(!nm||!ph)return alert('Name and phone required');
  try{
    await api('/api/v1/delivery-persons?shop_id='+(curShop?curShop.id:'shop-001'),'POST',{name:nm,phone:ph,vehicle_number:document.getElementById('aVeh').value,age:document.getElementById('aAge').value?parseInt(document.getElementById('aAge').value):null});
    cMo('aaMo');openDT();
  }catch(e){alert('Error adding person');}
}

/* PERFORMANCE STATUS */
async function openPS(){
  oMo('psMo');
  try{
    const d=await api('/api/v1/orders');
    const all=Array.isArray(d)?d:(d.items||d.data||d.orders||[]);
    const tot=all.length,pend=all.filter(o=>o.status==='pending').length,proc=all.filter(o=>o.status==='confirmed').length,del=all.filter(o=>['completed','delivered'].includes(o.status)).length;
    document.getElementById('psS').innerHTML='<div class="psc"><div class="psl">Total Orders</div><div class="psv">'+tot+'</div></div><div class="psc"><div class="psl">Pending</div><div class="psv or">'+pend+'</div></div><div class="psc"><div class="psl">Processing</div><div class="psv bl">'+proc+'</div></div><div class="psc"><div class="psl">Delivered</div><div class="psv gr">'+del+'</div></div>';
    const tc={Bw:0,Colour:0,Photo:0,Tshirt:0,Project:0},td=new Date().toDateString();
    all.filter(o=>new Date(o.created_at).toDateString()===td).forEach(o=>{const t=gT(o);if(tc[t]!==undefined)tc[t]+=(parseFloat(o.grand_total)||0);});
    const mx=Math.max(...Object.values(tc),1);
    document.getElementById('psB').innerHTML=TN.map(t=>'<div class="eb"><div class="ebd" style="background:'+TC[t]+'"></div><div class="ebl">'+TL[t]+'</div><div class="ebtr"><div class="ebf" style="width:'+(tc[t]/mx*100)+'%;background:'+TC[t]+'"></div></div><div class="ebv" style="color:'+TC[t]+'">&#8377;'+tc[t]+'</div></div>').join('');
    bShD(all);
  }catch(e){document.getElementById('psS').innerHTML='<div class="empty">Error loading</div>';}
}

/* BUILD SALES DATA */
function bShD(all){
  const today=new Date();today.setHours(0,0,0,0);
  const days=Array.from({length:8},(_,i)=>{const dt=new Date(today);dt.setDate(dt.getDate()-(7-i));return dt;});
  const db=days.map(day=>{
    const ds=day.toDateString();
    const dO=all.filter(o=>new Date(o.created_at).toDateString()===ds);
    const res={date:day,Bw:0,Colour:0,Photo:0,Tshirt:0,Project:0,total:0};
    dO.forEach(o=>{const t=gT(o);if(res[t]!==undefined){res[t]+=(parseFloat(o.grand_total)||0);res.total+=(parseFloat(o.grand_total)||0);}});
    return res;
  });
  shDat={db};
}

/* SALES HISTORY */
async function openSH(){
  cMo('psMo');oMo('shMo');
  if(!shDat.db){try{const d=await api('/api/v1/orders');bShD(Array.isArray(d)?d:(d.items||d.data||d.orders||[]));}catch(e){}}
  // reset tabs
  document.querySelectorAll('.shtab').forEach(t=>{t.style.background='';t.style.color='';t.style.borderColor='';});
  const f=document.querySelector('.shtab');if(f){f.style.background='#1a1a1a';f.style.color='#fff';f.style.borderColor='#1a1a1a';}
  curSHT='all';rSH('all');
}

function shF(type,el){
  document.querySelectorAll('.shtab').forEach(t=>{t.style.background='';t.style.color='';t.style.borderColor='';});
  const col=type==='all'?'#1a1a1a':(TC[type]||'#1a1a1a');
  el.style.background=col;el.style.color='#fff';el.style.borderColor=col;
  curSHT=type;rSH(type);
}

function rSH(type){
  if(!shDat.db)return;
  const db=shDat.db;
  const vals=type==='all'?db.map(d=>d.total):db.map(d=>d[type]||0);
  const tv=vals[7]||0,tot=vals.reduce((a,b)=>a+b,0),avg=tot/8;
  const col=type==='all'?'#3b82f6':(TC[type]||'#3b82f6');
  document.getElementById('shT').textContent='&#8377;'+tv.toFixed(0);
  document.getElementById('shT').style.color=col;
  document.getElementById('sh8').textContent='&#8377;'+tot.toFixed(0);
  document.getElementById('shA').textContent='&#8377;'+avg.toFixed(0);
  document.getElementById('shCT').textContent='Sales Over Time \u2014 '+(type==='all'?'All Types':TL[type]);
  const ctx=document.getElementById('shC').getContext('2d');
  if(shCh)shCh.destroy();
  shCh=new Chart(ctx,{type:'bar',data:{labels:db.map((_,i)=>'Day '+(i+1)),datasets:[{label:type==='all'?'All':TL[type],data:vals,backgroundColor:col,borderRadius:4}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{ticks:{callback:v=>'\u20b9'+v},grid:{color:'#f0f0f0'}}}}});
  const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  document.getElementById('shH').innerHTML=db.slice().reverse().map((d,ri)=>{
    const i=7-ri;const dt=d.date;
    const dv=type==='all'?d.total:(d[type]||0);
    const dots=TN.map(t=>'<span class="dhdot"><span class="dhdc" style="background:'+TC[t]+'"></span>'+TL[t]+' &#8377;'+(d[t]||0)+'</span>').join('');
    return '<div class="dhr"><div><div class="dhd">Day '+(i+1)+'</div><div class="dhdt">'+dt.getDate()+' '+MN[dt.getMonth()]+'</div><div class="dhdots">'+dots+'</div></div><div class="dhv" style="color:'+col+'">&#8377;'+dv.toFixed(0)+'</div></div>';
  }).join('');
}

/* TICKET */
const TKM={customer:{t:'Customer Ticket Raise',s:'Raise a customer support ticket'},stock:{t:'Stock Ticket Raise',s:'Report a stock or supply issue'},technical:{t:'Technical Issue',s:'Report a technical problem'}};
function openTK(type){
  curTK=type;closeTD();
  const m=TKM[type];
  document.getElementById('tkT').textContent=m.t;
  document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'');
  ['tBy','tSj','tDt'].forEach(id=>document.getElementById(id).value='');
  oMo('tkMo');
}
async function subTK(){
  const by=document.getElementById('tBy').value,sj=document.getElementById('tSj').value;
  if(!by||!sj)return alert('Fill Raised By and Subject');
  try{
    await api('/api/v1/tickets','POST',{subject:sj,description:document.getElementById('tDt').value,priority:curTK==='technical'?'high':'medium',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    cMo('tkMo');alert('Ticket raised successfully!');
  }catch(e){alert('Error raising ticket');}
}
