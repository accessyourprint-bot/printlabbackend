import os
path = r"C:\Users\Shiva\Downloads\altprint-backend (6)\altprint\static\specific_control.html"

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PrintLab Outlet</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:"Segoe UI",system-ui,sans-serif;background:#f8f8f8;color:#1a1a1a;min-height:100vh;}
.lw{display:flex;align-items:center;justify-content:center;min-height:100vh;background:#f5f0eb;}
.lb{background:#fff;border-radius:14px;padding:40px;width:340px;box-shadow:0 4px 20px rgba(0,0,0,.08);}
.lb h2{font-size:1.3rem;font-weight:800;margin-bottom:4px;}
.lb p{color:#666;font-size:.84rem;margin-bottom:24px;}
label{display:block;font-size:.8rem;font-weight:600;color:#444;margin-bottom:5px;}
.fi{width:100%;padding:11px 12px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:.93rem;margin-bottom:14px;}
.fi:focus{outline:none;border-color:#e84c1e;}
.lpb{width:100%;padding:12px;background:#e84c1e;color:#fff;border:none;border-radius:8px;font-size:.95rem;font-weight:700;cursor:pointer;}
.err{color:#e84c1e;font-size:.8rem;margin-top:8px;text-align:center;}
.sw{min-height:100vh;background:#f5f0eb;padding:48px 24px;}
.sc{max-width:860px;margin:0 auto;}
.pi{width:72px;height:72px;background:#fde8e0;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:2rem;cursor:pointer;}
.sc>h1{text-align:center;font-size:2rem;font-weight:900;margin-bottom:8px;}
.sc>p{text-align:center;color:#888;margin-bottom:36px;}
.ohd{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;}
.ohd h2{font-size:1.1rem;font-weight:800;}
.og{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.oc{background:#fff;border-radius:12px;padding:24px;border:1.5px solid #eee;}
.oc h3{font-size:1rem;font-weight:800;margin-bottom:6px;}
.oc .ad{font-size:.83rem;color:#888;margin-bottom:14px;}
.od{color:#e84c1e;font-size:.85rem;font-weight:700;cursor:pointer;}
.ob{display:flex;align-items:center;gap:6px;padding:9px 18px;border:1.5px solid #1a1a1a;background:#fff;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:600;}
.dw{min-height:100vh;background:#f8f8f8;}
.tb{background:#fff;border-bottom:1px solid #eee;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:80;}
.tbl{display:flex;align-items:center;gap:12px;}
.si{width:42px;height:42px;background:#fde8e0;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.3rem;cursor:pointer;position:relative;flex-shrink:0;}
.sn{font-size:1rem;font-weight:800;}
.ss{font-size:.75rem;color:#888;}
.tbr{display:flex;align-items:center;gap:8px;position:relative;}
.btn{display:flex;align-items:center;gap:6px;padding:8px 16px;border:1.5px solid #ddd;background:#fff;border-radius:20px;cursor:pointer;font-size:.82rem;font-weight:600;color:#1a1a1a;white-space:nowrap;}
.btn:hover{border-color:#aaa;background:#fafafa;}
.tbtn{background:#e84c1e;color:#fff;border-color:#e84c1e;border-radius:20px;}
.tbtn:hover{background:#c73d17;}
.sdrop{position:absolute;top:calc(100% + 8px);left:0;background:#fff;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.12);width:180px;overflow:hidden;z-index:100;border:1px solid #eee;}
.sdrop.hidden{display:none;}
.si-item{display:flex;align-items:center;gap:10px;padding:12px 16px;cursor:pointer;font-size:.88rem;font-weight:500;}
.si-item:hover{background:#f7f7f7;}
.si-item.red{color:#e84c1e;}
.tdrop{position:absolute;top:calc(100% + 8px);right:0;background:#fff;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.12);width:210px;overflow:hidden;z-index:100;border:1px solid #eee;}
.tdrop.hidden{display:none;}
.ti{display:flex;align-items:center;gap:10px;padding:12px 16px;cursor:pointer;font-size:.88rem;font-weight:500;}
.ti:hover{background:#f7f7f7;}
.ct{padding:20px;}
.jp{background:#fff;border-radius:14px;border:1.5px solid #eee;overflow:hidden;}
.jh{display:flex;justify-content:space-between;align-items:center;padding:18px 22px;border-bottom:1px solid #f0f0f0;}
.jh h2{font-size:1rem;font-weight:800;}
.tt{display:flex;gap:6px;}
.t{padding:7px 16px;border:1.5px solid #eee;background:#fff;border-radius:20px;cursor:pointer;font-size:.82rem;font-weight:600;color:#555;}
.t:hover{border-color:#e84c1e;color:#e84c1e;}
.t.on{background:#1a1a1a;border-color:#1a1a1a;color:#fff;}
.jc{padding:0;}
.ji{border-bottom:1px solid #f7f7f7;padding:16px 22px;}
.ji:last-child{border-bottom:none;}
.ji:hover{background:#fafafa;}
.jr{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;}
.jid{color:#e84c1e;font-weight:700;font-size:.9rem;}
.jst{padding:4px 12px;border-radius:20px;font-size:.75rem;font-weight:700;}
.st-p{background:#fff3e0;color:#e65100;}
.st-c{background:#e3f2fd;color:#1565c0;}
.st-d{background:#e8f5e9;color:#2e7d32;}
.st-x{background:#ffebee;color:#c62828;}
.jn{font-weight:700;font-size:.92rem;}
.jp2{font-size:.8rem;color:#888;margin-top:1px;}
.jrow2{display:flex;align-items:center;gap:16px;margin-top:8px;}
.jf{display:flex;align-items:center;gap:6px;color:#e84c1e;font-size:.83rem;font-weight:500;cursor:pointer;}
.jtype{padding:3px 10px;border:1.5px solid #ddd;border-radius:20px;font-size:.76rem;font-weight:600;}
.jdate{font-size:.8rem;color:#888;}
.emp{text-align:center;padding:40px;color:#aaa;}
.loading{text-align:center;padding:30px;color:#e84c1e;}
.hidden{display:none!important;}
.mo{position:fixed;inset:0;background:rgba(0,0,0,.45);display:flex;align-items:center;justify-content:center;z-index:200;}
.mo.hidden{display:none;}
.mb{background:#fff;border-radius:14px;width:420px;max-width:92vw;overflow:hidden;max-height:85vh;overflow-y:auto;}
.mh{padding:18px 22px;border-bottom:1px solid #f0f0f0;display:flex;justify-content:space-between;align-items:flex-start;position:sticky;top:0;background:#fff;}
.mh h3{font-size:1rem;font-weight:800;}
.mh p{font-size:.78rem;color:#888;margin-top:2px;}
.mx{background:none;border:none;font-size:1.1rem;cursor:pointer;color:#888;}
.mbody{padding:18px 22px;}
.mf{padding:14px 22px;border-bottom:0;border-top:1px solid #f0f0f0;display:flex;justify-content:flex-end;gap:8px;}
.fg{margin-bottom:14px;}
.fg label{font-size:.8rem;font-weight:600;color:#333;margin-bottom:5px;display:block;}
.fg input,.fg textarea{width:100%;padding:10px 12px;border:1.5px solid #e0e0e0;border-radius:8px;font-size:.9rem;font-family:inherit;}
.fg input:focus,.fg textarea:focus{outline:none;border-color:#e84c1e;}
.fr2{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.cbtn{padding:10px 20px;border:1.5px solid #ddd;background:#fff;border-radius:8px;cursor:pointer;font-size:.88rem;font-weight:600;}
.sbtn{padding:10px 20px;background:#e84c1e;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:.88rem;font-weight:700;}
.ag{display:flex;align-items:center;gap:14px;padding:16px 22px;border-bottom:1px solid #f7f7f7;}
.ag:last-child{border-bottom:none;}
.av{width:44px;height:44px;background:#fde8e0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;}
.an{font-weight:800;font-size:.95rem;}
.aa{font-size:.78rem;color:#888;}
.ai{font-size:.84rem;color:#333;margin-top:3px;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;}
.stat{background:#fff;border:1.5px solid #eee;border-radius:10px;padding:14px 16px;}
.sl{font-size:.74rem;color:#888;font-weight:600;margin-bottom:3px;}
.sv{font-size:1.5rem;font-weight:800;}
.sv-o{color:#e65100;}
.sv-b{color:#1565c0;}
.sv-g{color:#2e7d32;}
.pb{display:flex;align-items:center;gap:10px;padding:10px 22px;border-bottom:1px solid #f7f7f7;}
.pb:last-child{border-bottom:none;}
.pdot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.plb{width:60px;font-size:.86rem;font-weight:600;}
.ptr{flex:1;height:7px;background:#f0f0f0;border-radius:5px;overflow:hidden;}
.pf{height:100%;border-radius:5px;}
.pv{font-size:.86rem;font-weight:700;min-width:55px;text-align:right;}
.sh-page{min-height:100vh;background:#f8f8f8;padding:0;}
.sh-top{background:#fff;border-bottom:1px solid #eee;padding:16px 24px;display:flex;align-items:center;gap:14px;}
.bk{background:none;border:none;cursor:pointer;font-size:.9rem;font-weight:600;color:#333;display:flex;align-items:center;gap:4px;}
.sh-top h2{font-size:1.1rem;font-weight:800;}
.sh-top p{font-size:.78rem;color:#888;margin-top:1px;}
.sh-tabs{display:flex;gap:8px;padding:16px 24px;background:#fff;border-bottom:1px solid #f0f0f0;flex-wrap:wrap;}
.sht{padding:7px 18px;border:1.5px solid #eee;background:#fff;border-radius:20px;cursor:pointer;font-size:.83rem;font-weight:600;color:#555;}
.sht.on{color:#fff;border-color:transparent;}
.sh-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:18px 24px;}
.sh-stat{background:#fff;border:1.5px solid #eee;border-radius:12px;padding:16px 18px;}
.sh-sl{font-size:.76rem;color:#888;font-weight:600;margin-bottom:4px;}
.sh-sv{font-size:1.8rem;font-weight:800;}
.ch-w{background:#fff;border:1.5px solid #eee;border-radius:12px;margin:0 24px 18px;padding:18px;}
.ch-t{font-weight:800;font-size:.95rem;margin-bottom:2px;}
.ch-s{font-size:.78rem;color:#888;margin-bottom:14px;}
.dh{background:#fff;border:1.5px solid #eee;border-radius:12px;margin:0 24px 24px;overflow:hidden;}
.dh-hd{padding:16px 20px;border-bottom:1px solid #f0f0f0;font-weight:800;font-size:.95rem;}
.dh-row{display:flex;justify-content:space-between;align-items:center;padding:13px 20px;border-bottom:1px solid #f7f7f7;}
.dh-row:last-child{border-bottom:none;}
.dh-left{display:flex;flex-direction:column;gap:4px;}
.dh-day{font-weight:700;font-size:.88rem;}
.dh-date{font-size:.76rem;color:#aaa;}
.dh-dots{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;}
.dh-dot{display:flex;align-items:center;gap:3px;font-size:.74rem;color:#666;}
.dh-dc{width:7px;height:7px;border-radius:50%;}
.dh-val{font-weight:800;font-size:.92rem;}
canvas{width:100%!important;}
@media(max-width:700px){.stats{grid-template-columns:1fr 1fr;}.og{grid-template-columns:1fr;}.tbr .btn span:not(:first-child){display:none;}}
</style>
</head>
<body>
<div id="lw"><div class="lw"><div class="lb"><h2>PrintLab Outlet</h2><p>Sign in to manage your shop</p><label>Email</label><input class="fi" type="email" id="em" placeholder="shop@printlab.in"><label>Password</label><input class="fi" type="password" id="pw" placeholder="Password"><button class="lpb" onclick="login()">Sign In</button><div class="err" id="lerr"></div></div></div></div>

<div id="slw" class="hidden"><div class="sw"><div class="sc"><div class="pi" onclick="logout()">&#128424;</div><h1>Print Lab</h1><p>Select your shop to manage operations.</p><div class="ohd"><h2>Your Outlets</h2><button class="ob" onclick="showAO()">+ New Outlet</button></div><div class="og" id="og"><div class="loading">Loading...</div></div></div></div></div>

<div id="aow" class="hidden"><div class="sw"><div class="sc" style="max-width:500px"><div class="jp"><div class="jh"><h2>&#127978; New Print Shop</h2></div><div style="padding:20px"><div class="fg"><label>Shop Name</label><input class="fi" id="snm" placeholder="e.g. Print Lab Koramangala" style="margin-bottom:0"></div><div class="fr2" style="margin-top:12px"><div class="fg"><label>Phone</label><input class="fi" id="sph" placeholder="9876543210" style="margin-bottom:0"></div><div class="fg"><label>Address</label><input class="fi" id="sad" placeholder="123 Main St" style="margin-bottom:0"></div></div><div style="display:flex;gap:10px;justify-content:flex-end;margin-top:16px"><button class="cbtn" onclick="showSL()">Cancel</button><button class="sbtn" onclick="createOutlet()">Create Outlet</button></div></div></div></div></div></div>

<div id="dw" class="hidden">
<div class="dw">
<div class="tb">
  <div class="tbl">
    <div class="si" onclick="toggleSIDrop()" id="siBtn">&#128424;<div id="sidrop" class="sdrop hidden"><div class="si-item" onclick="showLogistics()">&#128230; Logistics</div><div class="si-item" onclick="showSettings()">&#9881; Settings</div><div class="si-item red" onclick="logout()">&#8594; Logout</div></div></div>
    <div><div class="sn" id="shnm">Shop</div><div class="ss">Dashboard</div></div>
  </div>
  <div class="tbr">
    <button class="btn" onclick="openDelivTeam()">&#128101; Delivery Team</button>
    <button class="btn" onclick="openPerfStatus()">&#128202; Performance Status</button>
    <button class="btn" onclick="openSalesHistory()">&#8599; Sales History</button>
    <button class="btn tbtn" onclick="toggleTDrop()">&#127915; Ticket Raise &#9660;<div id="tdrop" class="tdrop hidden"><div class="ti" onclick="openTM('customer')">&#128100; Customer Ticket Raise</div><div class="ti" onclick="openTM('stock')">&#128230; Stock Ticket Raise</div><div class="ti" onclick="openTM('technical')">&#128295; Technical Issue</div></div></button>
  </div>
</div>
<div class="ct">
  <div class="jp">
    <div class="jh"><h2>Active Jobs</h2><div class="tt"><button class="t on" onclick="fj('all',this)">B/W</button><button class="t" onclick="fj('colour',this)">Colour</button><button class="t" onclick="fj('photo',this)">Photo</button><button class="t" onclick="fj('tshirt',this)">T-Shirt</button><button class="t" onclick="fj('project',this)">Project</button></div></div>
    <div class="jc" id="jc"><div class="loading">Loading...</div></div>
  </div>
</div>
</div>
</div>

<!-- SALES HISTORY PAGE -->
<div id="shp" class="hidden">
<div class="sh-page">
  <div class="sh-top"><button class="bk" onclick="closeSH()">&#8592; Back</button><div><h2>Sales History</h2><p>Last 8 days, by print type</p></div></div>
  <div class="sh-tabs"><button class="sht on" style="background:#1a1a1a" onclick="shFilter('all',this)">All Types</button><button class="sht" onclick="shFilter('Bw',this)">B/W</button><button class="sht" onclick="shFilter('Colour',this)">Colour</button><button class="sht" onclick="shFilter('Photo',this)">Photo</button><button class="sht" onclick="shFilter('Tshirt',this)">T-Shirt</button><button class="sht" onclick="shFilter('Project',this)">Project</button></div>
  <div class="sh-stats"><div class="sh-stat"><div class="sh-sl">Today\'s Earnings</div><div class="sh-sv" id="shToday">Rs0</div></div><div class="sh-stat"><div class="sh-sl">8-Day Total</div><div class="sh-sv" id="sh8day">Rs0</div></div><div class="sh-stat"><div class="sh-sl">Daily Average</div><div class="sh-sv" id="shAvg">Rs0</div></div></div>
  <div class="ch-w"><div class="ch-t" id="shChTitle">Sales Over Time - All Types</div><div class="ch-s">Daily sales (Rs). Day 1 = oldest, Day 8 = today.</div><canvas id="shChart" height="180"></canvas></div>
  <div class="dh"><div class="dh-hd">Daily History</div><div id="dhRows"></div></div>
</div>
</div>

<!-- DELIVERY MODAL -->
<div id="dmMo" class="mo hidden"><div class="mb"><div class="mh"><div><h3>Delivery Team</h3><p id="dmSub">People assigned to this outlet.</p></div><button class="mx" onclick="closeMo('dmMo')">&#10005;</button></div><div class="mbody" id="dmBody"><div class="loading">Loading...</div></div><div class="mf"><button class="sbtn" onclick="openAM()">+ Add Person</button></div></div></div>

<!-- ADD AGENT MODAL -->
<div id="amMo" class="mo hidden"><div class="mb"><div class="mh"><div><h3>Add Delivery Person</h3></div><button class="mx" onclick="closeMo('amMo')">&#10005;</button></div><div class="mbody"><div class="fg"><label>Name</label><input class="fi" id="amNm" placeholder="Full name" style="margin-bottom:0"></div><div class="fr2" style="margin-top:12px"><div class="fg"><label>Age</label><input class="fi" id="amAge" type="number" placeholder="26" style="margin-bottom:0"></div><div class="fg"><label>Phone</label><input class="fi" id="amPh" placeholder="9876543210" style="margin-bottom:0"></div></div><div class="fg" style="margin-top:12px"><label>Vehicle Number</label><input class="fi" id="amVeh" placeholder="KA01AB1234" style="margin-bottom:0"></div></div><div class="mf"><button class="cbtn" onclick="closeMo('amMo')">Cancel</button><button class="sbtn" onclick="submitAM()">Add Person</button></div></div></div>

<!-- PERFORMANCE MODAL -->
<div id="pmMo" class="mo hidden"><div class="mb" style="width:560px"><div class="mh"><div><h3>Performance Status</h3><p>Snapshot of orders over the last 8 days.</p></div><button class="mx" onclick="closeMo('pmMo')">&#10005;</button></div><div class="mbody"><div class="stats" id="pmStats"></div><div style="font-weight:700;font-size:.88rem;margin-bottom:10px">Earnings by Print Type (Today)</div><div id="pmBars"></div></div></div></div>

<!-- TICKET MODAL -->
<div id="tmMo" class="mo hidden"><div class="mb"><div class="mh"><div><h3 id="tmTit">Customer Ticket Raise</h3><p id="tmSub"></p></div><button class="mx" onclick="closeMo('tmMo')">&#10005;</button></div><div class="mbody"><div class="fg"><label>Raised By</label><input class="fi" id="tmBy" placeholder="Your name" style="margin-bottom:0"></div><div class="fg" style="margin-top:12px"><label>Subject</label><input class="fi" id="tmSubj" placeholder="Brief description" style="margin-bottom:0"></div><div class="fg" style="margin-top:12px"><label>Details (Optional)</label><textarea class="fi" id="tmDet" rows="3" placeholder="More details..." style="margin-bottom:0"></textarea></div></div><div class="mf"><button class="cbtn" onclick="closeMo('tmMo')">Cancel</button><button class="sbtn" onclick="submitTM()">Raise Ticket</button></div></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const API=window.location.origin;
let tok=localStorage.getItem('pl_s'),curShop=null,allOrders=[],shChObj=null;
const TC={Bw:'#3b82f6',Colour:'#f97316',Photo:'#10b981',Tshirt:'#8b5cf6',Project:'#ef4444'};
const TN=['Bw','Colour','Photo','Tshirt','Project'];
const TL={'Bw':'B/W','Colour':'Colour','Photo':'Photo','Tshirt':'T-Shirt','Project':'Project'};
if(tok)showSL();

async function login(){
  try{const r=await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:document.getElementById('em').value,password:document.getElementById('pw').value})});
  const d=await r.json();if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);showSL();}
  else document.getElementById('lerr').textContent='Invalid credentials';}
  catch(e){document.getElementById('lerr').textContent='Cannot connect';}
}
function showSL(){['lw','dw','aow','shp'].forEach(h);show('slw');loadOutlets();}
function showAO(){h('slw');show('aow');}
function logout(){localStorage.removeItem('pl_s');location.reload();}
function h(id){document.getElementById(id).classList.add('hidden');}
function show(id){document.getElementById(id).classList.remove('hidden');}
function openMo(id){document.getElementById(id).classList.remove('hidden');}
function closeMo(id){document.getElementById(id).classList.add('hidden');}

async function api(u,m,b){
  const o={method:m||'GET',headers:{Authorization:'Bearer '+tok}};
  if(b){o.headers['Content-Type']='application/json';o.body=JSON.stringify(b);}
  return (await fetch(API+u,o)).json();
}

async function loadOutlets(){
  try{const d=await api('/api/v1/shops');const s=Array.isArray(d)?d:(d.data||[]);
  if(!s.length){document.getElementById('og').innerHTML='<div class="emp">No outlets yet</div>';return;}
  document.getElementById('og').innerHTML=s.map(x=>`<div class="oc"><h3>${x.name||'Shop'}</h3><div class="ad">${x.address||'No address set'}</div><a class="od" onclick='openDash(${JSON.stringify(x)})'>Open Dashboard &rarr;</a></div>`).join('');}
  catch(e){document.getElementById('og').innerHTML='<div class="emp">Error loading</div>';}
}
async function createOutlet(){
  const nm=document.getElementById('snm').value;if(!nm)return alert('Shop name required');
  try{await api('/api/v1/shops','POST',{name:nm,phone:document.getElementById('sph').value,address:document.getElementById('sad').value,is_active:true});showSL();}
  catch(e){alert('Error creating outlet');}
}
function openDash(s){curShop=s;['slw','aow','shp'].forEach(h);show('dw');document.getElementById('shnm').textContent=s.name;loadJobs();}

function toggleSIDrop(){document.getElementById('sidrop').classList.toggle('hidden');}
function toggleTDrop(){document.getElementById('tdrop').classList.toggle('hidden');}
document.addEventListener('click',function(e){
  if(!e.target.closest('#siBtn'))document.getElementById('sidrop').classList.add('hidden');
  if(!e.target.closest('.tbtn'))document.getElementById('tdrop').classList.add('hidden');
});
function showLogistics(){alert('Logistics - coming soon');document.getElementById('sidrop').classList.add('hidden');}
function showSettings(){alert('Settings - coming soon');document.getElementById('sidrop').classList.add('hidden');}

function gT(o){const s=JSON.stringify(o).toLowerCase();if(s.includes('colour')||s.includes('color'))return'Colour';if(s.includes('photo'))return'Photo';if(s.includes('tshirt')||s.includes('t-shirt'))return'Tshirt';if(s.includes('project'))return'Project';return'Bw';}
function sCls(s){const m={pending:'st-p',confirmed:'st-c',completed:'st-d',delivered:'st-d',cancelled:'st-x'};return m[s]||'st-p';}

async function loadJobs(){
  try{const d=await api('/api/v1/orders');allOrders=Array.isArray(d)?d:(d.data||[]);renderJ(allOrders);}
  catch(e){document.getElementById('jc').innerHTML='<div class="emp">Error loading orders</div>';}
}
function fj(t,el){document.querySelectorAll('.t').forEach(x=>x.classList.remove('on'));el.classList.add('on');
  if(t==='all'){renderJ(allOrders);return;}
  const map={colour:'colour',photo:'photo',tshirt:'tshirt',project:'project'};
  renderJ(allOrders.filter(o=>JSON.stringify(o).toLowerCase().includes(map[t]||t)));
}
function renderJ(jobs){
  if(!jobs.length){document.getElementById('jc').innerHTML='<div class="emp">No active jobs</div>';return;}
  document.getElementById('jc').innerHTML=jobs.map(o=>`<div class="ji"><div class="jr"><span class="jid">${o.order_number||o.id.slice(0,10)}</span><span class="jst ${sCls(o.status)}">${(o.status||'pending').charAt(0).toUpperCase()+(o.status||'pending').slice(1)}</span></div><div class="jn">${o.user_name||'Customer'}</div><div class="jp2">${o.user_phone||''}</div><div class="jrow2"><span class="jf">&#8681; ${o.file_name||'document.pdf'}</span><span style="font-size:.82rem;color:#666">x${o.copies||1}</span><span class="jtype">${TL[gT(o)]||gT(o)}</span><span class="jdate">${new Date(o.created_at).toLocaleDateString('en-IN',{month:'short',day:'numeric'})}, ${new Date(o.created_at).toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'})}</span></div></div>`).join('');
}

async function openDelivTeam(){
  openMo('dmMo');
  document.getElementById('dmSub').textContent='People assigned to '+(curShop?curShop.name:'this outlet')+'.';
  try{const d=await api('/api/v1/delivery-persons');const ag=Array.isArray(d)?d:(d.data||[]);
  document.getElementById('dmBody').innerHTML=ag.length?ag.map(a=>`<div class="ag"><div class="av">&#128100;</div><div><div class="an">${a.name}</div><div class="aa">${a.age?'Age '+a.age:''}</div><div class="ai">&#128222; ${a.phone||'-'} &nbsp; &#127949; ${a.vehicle_number||'-'}</div></div></div>`).join(''):'<div class="emp">No delivery persons yet</div>';}
  catch(e){document.getElementById('dmBody').innerHTML='<div class="emp">Error loading</div>';}
}
function openAM(){closeMo('dmMo');['amNm','amAge','amPh','amVeh'].forEach(id=>document.getElementById(id).value='');openMo('amMo');}
async function submitAM(){
  const nm=document.getElementById('amNm').value,ph=document.getElementById('amPh').value;
  if(!nm||!ph)return alert('Name and phone required');
  try{await api('/api/v1/delivery-persons?shop_id='+(curShop?curShop.id:'shop-001'),'POST',{name:nm,phone:ph,vehicle_number:document.getElementById('amVeh').value,age:document.getElementById('amAge').value?parseInt(document.getElementById('amAge').value):null});closeMo('amMo');openDelivTeam();}
  catch(e){alert('Error adding person');}
}

async function openPerfStatus(){
  openMo('pmMo');
  try{const d=await api('/api/v1/orders');const all=Array.isArray(d)?d:(d.data||[]);
  const total=all.length,pend=all.filter(o=>o.status==='pending').length,proc=all.filter(o=>o.status==='confirmed').length,deliv=all.filter(o=>['completed','delivered'].includes(o.status)).length;
  document.getElementById('pmStats').innerHTML=`<div class="stat"><div class="sl">Total Orders</div><div class="sv">${total}</div></div><div class="stat"><div class="sl">Pending</div><div class="sv sv-o">${pend}</div></div><div class="stat"><div class="sl">Processing</div><div class="sv sv-b">${proc}</div></div><div class="stat"><div class="sl">Delivered</div><div class="sv sv-g">${deliv}</div></div>`;
  const tc={Bw:0,Colour:0,Photo:0,Tshirt:0,Project:0},td=new Date().toDateString();
  all.filter(o=>new Date(o.created_at).toDateString()===td).forEach(o=>{const t=gT(o);if(tc[t]!==undefined)tc[t]+=(o.grand_total||0);});
  const mx=Math.max(...Object.values(tc),1);
  document.getElementById('pmBars').innerHTML=TN.map(t=>`<div class="pb"><div class="pdot" style="background:${TC[t]}"></div><div class="plb">${TL[t]}</div><div class="ptr"><div class="pf" style="width:${tc[t]/mx*100}%;background:${TC[t]}"></div></div><div class="pv" style="color:${TC[t]}">Rs${tc[t]}</div></div>`).join('');}
  catch(e){document.getElementById('pmStats').innerHTML='<div class="emp">Error</div>';}
}

let shData={};
let curShType='all';
async function openSalesHistory(){
  h('dw');show('shp');
  try{const d=await api('/api/v1/orders');const all=Array.isArray(d)?d:(d.data||[]);
  const today=new Date();today.setHours(0,0,0,0);
  const days=Array.from({length:8},(_,i)=>{const dt=new Date(today);dt.setDate(dt.getDate()-(7-i));return dt;});
  const db=days.map(day=>{const ds=day.toDateString();const dayOrds=all.filter(o=>new Date(o.created_at).toDateString()===ds);const res={date:day,Bw:0,Colour:0,Photo:0,Tshirt:0,Project:0,total:0};dayOrds.forEach(o=>{const t=gT(o);if(res[t]!==undefined){res[t]+=(o.grand_total||0);res.total+=(o.grand_total||0);}});return res;});
  shData={db,all};renderSH('all');}
  catch(e){}
}
function closeSH(){h('shp');show('dw');}
function shFilter(type,el){
  document.querySelectorAll('.sht').forEach(x=>{x.classList.remove('on');x.style.background='';x.style.color='';x.style.borderColor='';});
  el.classList.add('on');
  const col=type==='all'?'#1a1a1a':(TC[type]||'#1a1a1a');
  el.style.background=col;el.style.color='#fff';el.style.borderColor=col;
  curShType=type;renderSH(type);
}
function renderSH(type){
  if(!shData.db)return;
  const db=shData.db;
  const vals=type==='all'?db.map(d=>d.total):db.map(d=>d[type]||0);
  const today=vals[7]||0;const total=vals.reduce((a,b)=>a+b,0);const avg=total/8;
  document.getElementById('shToday').textContent='Rs'+today.toFixed(0);
  document.getElementById('sh8day').textContent='Rs'+total.toFixed(0);
  document.getElementById('shAvg').textContent='Rs'+avg.toFixed(0);
  document.getElementById('shChTitle').textContent='Sales Over Time - '+(type==='all'?'All Types':TL[type]);
  const col=type==='all'?'#3b82f6':(TC[type]||'#3b82f6');
  const ctx=document.getElementById('shChart').getContext('2d');
  if(shChObj)shChObj.destroy();
  shChObj=new Chart(ctx,{type:'bar',data:{labels:db.map((_,i)=>'Day '+(i+1)),datasets:[{label:type==='all'?'All':TL[type],data:vals,backgroundColor:col,borderRadius:4}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{ticks:{callback:v=>'Rs'+v},grid:{color:'#f0f0f0'}}}}});
  const months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  document.getElementById('dhRows').innerHTML=db.slice().reverse().map((d,ri)=>{
    const i=7-ri;const dt=d.date;const dayName='Day '+(i+1);const dateStr=dt.getDate()+' '+months[dt.getMonth()];
    const dv=type==='all'?d.total:(d[type]||0);
    const dotStr=TN.map(t=>`<span class="dh-dot"><span class="dh-dc" style="background:${TC[t]}"></span>${TL[t]} Rs${d[t]||0}</span>`).join('');
    const valCol=type==='all'?'#1a1a1a':(TC[type]||'#1a1a1a');
    return`<div class="dh-row"><div class="dh-left"><div class="dh-day">${dayName}</div><div class="dh-date">${dateStr}</div><div class="dh-dots">${dotStr}</div></div><div class="dh-val" style="color:${valCol}">Rs${dv.toFixed(0)}</div></div>`;
  }).join('');
}

let curTM='customer';
const TM={customer:{t:'Customer Ticket Raise',s:'Raise a customer ticket'},stock:{t:'Stock Ticket Raise',s:'Report a stock issue'},technical:{t:'Technical Issue',s:'Report a technical issue'}};
function openTM(type){curTM=type;document.getElementById('tdrop').classList.add('hidden');const m=TM[type];document.getElementById('tmTit').textContent=m.t;document.getElementById('tmSub').textContent=m.s+(curShop?' for '+curShop.name:'');['tmBy','tmSubj','tmDet'].forEach(id=>document.getElementById(id).value='');openMo('tmMo');}
async function submitTM(){
  const by=document.getElementById('tmBy').value,subj=document.getElementById('tmSubj').value;
  if(!by||!subj)return alert('Please fill Raised By and Subject');
  try{await api('/api/v1/tickets','POST',{subject:subj,description:document.getElementById('tmDet').value,priority:curTM==='technical'?'high':'medium',category:curTM,raised_by:by,shop_id:curShop?curShop.id:null});closeMo('tmMo');alert('Ticket raised!');}
  catch(e){alert('Error raising ticket');}
}
setInterval(()=>{if(curShop&&!document.getElementById('dw').classList.contains('hidden'))loadJobs();},15000);
</script>
</body></html>"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done! File written:', len(html), 'bytes')
