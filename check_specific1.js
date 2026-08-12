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
  let em = document.getElementById('em').value.trim();
  if(em && em.indexOf('@')===-1){ em = em + '@altprint.in'; }
  const pw = document.getElementById('pw').value;
  try{
    const r = await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:em,password:pw})});
    const d = await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_s',tok);if(d.shop_id)localStorage.setItem('pl_shop',d.shop_id);initD();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect to server';}
}

function doLogout(){localStorage.removeItem('pl_s');localStorage.removeItem('pl_shop');location.reload();}

async function initD(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('dw').classList.remove('hidden');
  try{
    const myShopId = localStorage.getItem('pl_shop');
    if(myShopId){
      curShop = await api('/api/v1/shops/'+myShopId);
      document.getElementById('shopName').textContent=curShop.name||'Print Lab';
    }else{
      const d = await api('/api/v1/shops');
      const s = Array.isArray(d)?d:(d.data||[]);
      if(s.length){curShop=s[0];document.getElementById('shopName').textContent=curShop.name||'Print Lab';}
    }
    if(curShop){
      document.getElementById('sdShopId').textContent=curShop.id||'-';
      document.getElementById('sdShopEmail').textContent=curShop.owner_email||'-';
      document.getElementById('sdShopPhone').textContent=curShop.owner_phone||'-';
    }
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
  const si=(o.special_instructions||'').toLowerCase();
  if(si.includes('bw_print'))return'Bw';
  if(si.includes('colour_print'))return'Colour';
  if(si.includes('photo_print'))return'Photo';
  if(si.includes('tshirt_print'))return'Tshirt';
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

let curStabFilter = 'all';
function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  const actHead = document.getElementById('actHead');
  if(actHead){
    if(s==='all') actHead.innerText = 'Download';
    else if(s==='downloaded') actHead.innerText = 'Download';
    else if(s==='completed') actHead.innerText = 'Download';
    else if(s==='out_for_delivery') actHead.innerText = 'Out for Delivery';
  }
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
  if(s==='out_for_delivery'){rJ(allOrds.filter(o=>o.status==='out_for_delivery'));return;}
}

async function showDelivery(el){
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  const jl = document.getElementById('jl');
  jl.innerHTML = '<div class="loading">Loading&#8230;</div>';
  try{
    const resp = await fetch(API+'/api/v1/delivery-persons/with-order-counts', {headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){ jl.innerHTML='<div class="empty">Could not load delivery team</div>'; return; }
    const persons = await resp.json();
    if(!persons.length){ jl.innerHTML='<div class="empty">No delivery persons added yet</div>'; return; }
    const rows = persons.map(function(p){
      return '<tr>'
        +'<td style="padding:10px 12px;border-bottom:1px solid #eee;font-weight:700">'+(p.name||'&mdash;')+'</td>'
        +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(p.phone||'&mdash;')+'</td>'
        +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(p.vehicle_number||'&mdash;')+'</td>'
        +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(p.current_status||'offline')+'</td>'
        +'<td style="padding:10px 12px;border-bottom:1px solid #eee"><span style="background:#fff3ea;color:#ea580c;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">'+(p.order_count||0)+' orders</span></td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:collapse;font-size:13px">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Name</th>'
      +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Phone</th>'
      +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Vehicle</th>'
      +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Status</th>'
      +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Orders Assigned</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
  }catch(e){
    jl.innerHTML = '<div class="empty">Something went wrong loading the delivery team</div>';
  }
}

async function markComplete(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=ready',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark complete');return;}
    await loadJ();
    document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
    const completedBtn = Array.from(document.querySelectorAll('.stabs .ttab')).find(b=>b.textContent.trim()==='Completed');
    if(completedBtn){completedBtn.classList.add('on');}
    curStabFilter='completed';
    rJ(allOrds.filter(o=>o.status==='ready'));
  }catch(e){alert('Failed to mark complete');}
}

async function markOutForDelivery(orderId,deliveryPersonId){
  try{
    let url=API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery';
    if(deliveryPersonId) url+='&delivery_person_id='+deliveryPersonId;
    const resp = await fetch(url,{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
    const ofdBtn = Array.from(document.querySelectorAll('.stabs .ttab')).find(b=>b.textContent.trim()==='Out for Delivery');
    if(ofdBtn){ofdBtn.classList.add('on');}
    curStabFilter='out_for_delivery';
    rJ(allOrds.filter(o=>o.status==='out_for_delivery'));
  }catch(e){alert('Failed to mark out for delivery');}
}

let _ofdOrderId=null;
async function openOFDPicker(orderId){
  _ofdOrderId=orderId;
  const body=document.getElementById('ofdB');
  body.innerHTML='<div class="loading">Loading&#8230;</div>';
  oMo('ofdMo');
  try{
    const resp=await fetch(API+'/api/v1/delivery-persons',{headers:{'Authorization':'Bearer '+tok}});
    const persons=await resp.json();
    const list=Array.isArray(persons)?persons:(persons.data||[]);
    body.innerHTML=list.length
      ? list.map(p=>'<div class="ag" style="cursor:pointer" onclick="confirmOFD(&quot;'+p.id+'&quot;)"><div class="av">&#128666;</div><div><div class="an">'+p.name+'</div><div class="ai"><span>&#128222; '+(p.phone||'&mdash;')+'</span><span>&#128661; '+(p.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      : '<div class="empty">No delivery persons added yet. Add one from Delivery Team first.</div>';
  }catch(e){ body.innerHTML='<div class="empty">Error loading delivery team</div>'; }
}
function confirmOFD(personId){
  cMo('ofdMo');
  markOutForDelivery(_ofdOrderId, personId);
}

function fj(t,el){
  document.querySelectorAll('.ttab').forEach(x=>x.classList.remove('on'));
  el.classList.add('on');
  if(t==='all'){rJ(allOrds);return;}
  const tabToType={bw:'Bw',colour:'Colour',photo:'Photo',tshirt:'Tshirt'};
  rJ(allOrds.filter(o=>gT(o)===tabToType[t]));
}

function rJ(jobs){
  const jl = document.getElementById('jl');
  if(!jobs.length){jl.innerHTML='<div class="empty">No active jobs</div>';return;}

  if(curStabFilter==='completed'){
    window.completedJobsCache = jobs;
    let rows=jobs.map(function(o){
      const hasFiles=(o.files&&o.files.length);
      return '<tr>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c;font-size:14px">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_name||o.customer_name||'Customer')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(o.status==='out_for_delivery'
          ?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; Out for Delivery</span>'
          :'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(o.status==='out_for_delivery'
          ?'<span style="color:#999;font-size:12px">Assigned</span>'
          :'<button onclick="openOFDPicker(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>')
        +'</td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Order ID</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Customer Name</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Phone Number</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Download</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Status</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Action</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }

  // header-sync-injected
  (function(){
    const actHead = document.getElementById('actHead');
    if(actHead){
      if(curStabFilter==='all') actHead.innerText = 'Download';
      else if(curStabFilter==='downloaded') actHead.innerText = 'Download';
      else if(curStabFilter==='out_for_delivery') actHead.innerText = 'Out for Delivery';
    }
  })();
  let rows=jobs.map(function(o){
    const docsHtml=(o.files&&o.files.length)?o.files.map(function(f){
      return '<div style="cursor:pointer;text-decoration:underline;color:#2563eb" onclick="event.stopPropagation();dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/"/g,'')+'&quot;)">&#8595; '+(f.original_filename||'document.pdf')+'</div>';
    }).join(''):'<span style="color:#999">No file</span>';
    return '<tr>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_name||o.customer_name||'Customer')+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+docsHtml+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='out_for_delivery'?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; En route</span>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')))+'</td>'
      +'</tr>';
  }).join('');
  jl.innerHTML='<table style="width:100%;border-collapse:collapse;font-size:13px">'
    +'<thead><tr style="background:#f8f8fa;text-align:left">'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Order ID</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Customer Name</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Phone Number</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Document</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd" id="actHead">'+(curStabFilter==='out_for_delivery'?'Out for Delivery':'Download')+'</th>'
    +'</tr></thead><tbody>'+rows+'</tbody></table>';
}

function openDeliveryDetailsPage(orderId){
  const jobs = window.completedJobsCache || [];
  const o = jobs.find(function(j){return j.id===orderId;});
  if(!o){return;}
  const jl = document.getElementById('jl');
  const docsHtml = (o.files&&o.files.length) ? o.files.map(function(f){
    return '<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f0f0f0">'
      +'<span style="font-size:13px;color:#333">'+(f.original_filename||'document.pdf')+'</span>'
      +'<button onclick="dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/"/g,'')+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>'
      +'</div>';
  }).join('') : '<div style="color:#999;font-size:13px;padding:10px 0">No files</div>';
  const row = function(label, value){
    return '<div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f0f0f0">'
      +'<span style="color:#666;font-size:13px">'+label+'</span>'
      +'<span style="font-weight:600;font-size:13px;color:#222;text-align:right">'+(value||'Not provided')+'</span>'
      +'</div>';
  };
  jl.innerHTML = '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
    + '<div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">'
    + '<button onclick="fs(&quot;completed&quot;,document.querySelector(&quot;.stabs .ttab.on&quot;)||document.querySelector(&quot;.stabs .ttab&quot;))" style="background:none;border:1px solid #ddd;border-radius:6px;padding:6px 12px;font-size:13px;cursor:pointer">&larr; Back</button>'
    + '<h2 style="margin:0;font-size:18px;font-weight:700;color:#222">Delivery Details</h2>'
    + '</div>'
    + row('Order ID', o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))
    + row('Customer Name', o.user_name||o.customer_name)
    + row('Phone Number', o.user_phone||o.customer_phone)
    + row('Delivery Address', o.delivery_address||o.address)
    + row('Assigned Delivery Partner', o.delivery_partner_name||o.delivery_partner)
    + row('Delivery Notes', o.delivery_instructions||o.special_instructions)
    + '<div style="margin-top:16px"><div style="color:#666;font-size:13px;margin-bottom:8px">Uploaded Documents</div>' + docsHtml + '</div>'
    + '<button onclick="confirmOutForDeliveryPage(&quot;'+o.id+'&quot;)" style="width:100%;margin-top:24px;background:#2563eb;color:#fff;border:none;border-radius:8px;padding:14px;font-size:15px;cursor:pointer;font-weight:700">Out For Delivery</button>'
    + '</div>';
}

async function confirmOutForDeliveryPage(orderId){
  await markOutForDelivery(orderId);
}

/* DROPDOWNS */
async function downloadAllZip(orderId, orderNumber){
  try{
    const resp = await fetch(API+'/api/v1/files/orders/'+orderId+'/download-all', {headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to download files');return;}
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = orderNumber+'_documents.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }catch(e){alert('Failed to download files');}
}



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
      ?ag.map(a=>'<div class="ag" style="cursor:pointer" onclick="showPartnerOrders(&quot;'+a.id+'&quot;,&quot;'+a.name.replace(/"/g,'')+'&quot;)"><div class="av">&#128100;</div><div><div class="an">'+a.name+'</div><div class="aa">'+(a.age?'Age '+a.age:'')+'</div><div class="ai"><span>&#128222; '+(a.phone||'&mdash;')+'</span><span>&#128661; '+(a.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      :'<div class="empty">No delivery persons yet</div>';
  }catch(e){document.getElementById('dtB').innerHTML='<div class="empty">Error loading</div>';}
}

async function showPartnerOrders(personId,personName){
  cMo('dtMo');
  document.getElementById('poName').textContent=personName;
  const body=document.getElementById('poB');
  body.innerHTML='<div class="loading">Loading&#8230;</div>';
  oMo('poMo');
  try{
    if(!window.allOrds || !allOrds.length){ await loadJ(); }
    const orders=(allOrds||[]).filter(o=>o.delivery_person_id===personId);
    body.innerHTML=orders.length
      ? '<table style="width:100%;border-collapse:collapse;font-size:13px">'
        +'<thead><tr style="background:#f8f8fa;text-align:left">'
        +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Order ID</th>'
        +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Customer</th>'
        +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Phone</th>'
        +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Status</th>'
        +'</tr></thead><tbody>'
        +orders.map(o=>'<tr><td style="padding:10px 12px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c">'+(o.order_number||o.id.slice(0,12))+'</td><td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_name||o.customer_name||'Customer')+'</td><td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td><td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.status||'&mdash;')+'</td></tr>').join('')
        +'</tbody></table>'
      : '<div class="empty">No orders currently assigned to '+personName+'</div>';
  }catch(e){ body.innerHTML='<div class="empty">Error loading orders</div>'; }
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
  document.getElementById('tkOid').textContent=(curShop&&curShop.owner_email)?('Outlet ID: '+curShop.owner_email.split('@')[0]):'';
  ['tBy','tSj','tDt'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('tSjSelect').selectedIndex=0;
  if(type==='technical'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.add('hidden');
    document.getElementById('tSjSelectField').classList.remove('hidden');
  }else if(type==='stock'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }else{
    document.getElementById('tByField').classList.remove('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }
  oMo('tkMo');
}
let tkSubmitting=false;
async function subTK(){
  if(tkSubmitting)return;
  const isTech=curTK==='technical';
  const isStock=curTK==='stock';
  const by=isTech?'N/A':(isStock?(curShop?curShop.name:'Outlet'):document.getElementById('tBy').value);
  const sj=isTech?document.getElementById('tSjSelect').value:document.getElementById('tSj').value;
  const dt=(document.getElementById('tDt').value||'').trim();
  if(isTech){ if(!dt)return alert('Please explain the issue in Details'); }
  else if(isStock){ if(!sj)return alert('Fill Subject'); }
  else if(!by||!sj)return alert('Fill Raised By and Subject');
  tkSubmitting=true;
  const btn=document.querySelector('#tkMo .bsb');
  if(btn){btn.disabled=true;btn.textContent='Raising...';}
  try{
    const dtVal=(document.getElementById('tDt').value||'').trim();const r = await api('/api/v1/tickets','POST',{subject:sj,description:dtVal.length>=3?dtVal:sj,priority:curTK==='technical'?'high':'normal',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});
    if(r && (r.id || (r.data && r.data.id))){
      document.getElementById('tBy').value='';document.getElementById('tSj').value='';document.getElementById('tDt').value='';
      cMo('tkMo');alert('Ticket raised successfully!');
    }
    else{alert('Error raising ticket: '+(r&&r.detail?r.detail:'Please try logging in again'));}
  }catch(e){alert('Error raising ticket');}
  finally{
    tkSubmitting=false;
    if(btn){btn.disabled=false;btn.textContent='Raise Ticket';}
  }
}
