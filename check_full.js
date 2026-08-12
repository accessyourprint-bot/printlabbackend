function openRaiseTicket(){document.getElementById('raiseTicketModal').style.display='flex';}
async function submitRaiseTicket(){
  const subject=document.getElementById('rtSubject').value;
  if(!subject)return alert('Subject required');
  const r=await api('/api/v1/tickets','POST',{subject,description:document.getElementById('rtDesc').value,category:document.getElementById('rtCat').value,priority:'medium'});
  if(r&&r.id){document.getElementById('raiseTicketModal').style.display='none';loadTickets();alert('Ticket raised!');}
  else alert('Error raising ticket');
}


const API=window.location.origin;
let tok=localStorage.getItem('pl_full');
let revChartObj=null;
let allOutlets=[],allTickets=[],allCustomers=[],allSubAdmins=[],allStock=[];
let curOtType='own',curTkFilter='customer';
if(tok) initApp();
async function doLogin(){
  try{
    const em=document.getElementById('em').value;
    const email=em.includes('@')?em:em+'@altprint.in';
    const r=await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email,password:document.getElementById('pw').value})});
    const d=await r.json();
    if(d.access_token){tok=d.access_token;localStorage.setItem('pl_full',tok);initApp();}
    else document.getElementById('lerr').textContent='Invalid credentials';
  }catch(e){document.getElementById('lerr').textContent='Cannot connect';}
}
function doLogout(){localStorage.removeItem('pl_full');location.reload();}
async function loadFeatureFlags(){
  const flags=await api('/api/v1/features');
  const list=document.getElementById('fcFeatureList');
  if(!Array.isArray(flags)){list.innerHTML='<p style="color:#c00">Failed to load features</p>';return;}
  list.innerHTML=flags.map(f=>
    '<label style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border:1px solid #ececf1;border-radius:10px;cursor:pointer;background:'+(f.enabled?'#fff':'#faf7f5')+'">'+
    '<span style="font-size:.86rem;font-weight:600;color:'+(f.enabled?'#1a223e':'#aaa')+'">'+f.label+'</span>'+
    '<span class="switch"><input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleFeatureFlag(\''+f.feature_name+'\', this.checked)"><span class="slider"></span></span>'+
    '</label>'
  ).join('');
}
async function toggleFeatureFlag(name, enabled){
  const r=await api('/api/v1/features/toggle','POST',{feature_name:name, enabled:enabled, shop_id:null});
  if(!r || !r.data){alert('Failed to update feature');}
  loadFeatureFlags();
}

function initApp(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('appWrap').classList.remove('hidden');
  loadDashSummary();
}
async function api(u,m,b){
  const o={method:m||'GET',headers:{Authorization:'Bearer '+tok}};
  if(b){o.headers['Content-Type']='application/json';o.body=JSON.stringify(b);}
  try{const r=await fetch(API+u,o);return await r.json();}catch(e){return null;}
}
function fmtDate(d){try{return new Date(d).toLocaleDateString('en-GB');}catch(e){return'+ï¿½+ï¿½+ï¿½';}}
function fmtTime(d){try{return new Date(d).toLocaleString('en-GB',{hour:'2-digit',minute:'2-digit',hour12:true});}catch(e){return'+ï¿½+ï¿½+ï¿½';}}
const PAGE_TITLES={
  liveprint:'Live Print Update',printdone:'Print Done',paymentday:'Payment for Day',
  paymenthist:'Payment History',delivery:'Delivery Person',customer:'Project',
  outlet:'Outlet Account',subadmin:'Sub-Admin Management',accountmgmt:'Account Management',
  ticket:'Ticket Management',stock:'Stock Management',appcontrol:'App Control'
};
function openPage(id){
  document.querySelectorAll('[id^="pg-"]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('pg-'+id).classList.remove('hidden');
  document.getElementById('cSep').style.display='inline';
  document.getElementById('cDash').style.display='inline';
  document.getElementById('cTitle').textContent=PAGE_TITLES[id]||'';
  const loaders={liveprint:loadLivePrint,printdone:loadPrintDone,paymentday:loadPaymentDay,
    paymenthist:loadPaymentHist,delivery:loadDelivery,customer:loadCustomers,
    outlet:loadOutlets,subadmin:loadSubAdmins,accountmgmt:loadAccountMgmt,
    ticket:loadTickets,stock:loadStock,appcontrol:loadAppControl};
  if(loaders[id]) loaders[id]();
}
function goDash(){
  document.querySelectorAll('[id^="pg-"]').forEach(p=>p.classList.add('hidden'));
  document.getElementById('pg-dash').classList.remove('hidden');
  document.getElementById('cSep').style.display='none';
  document.getElementById('cDash').style.display='none';
  document.getElementById('cTitle').textContent='';
  loadDashSummary();
}
async function loadDashSummary(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const today=new Date().toDateString();
  const inProg=orders.filter(o=>o.status==='confirmed'||o.status==='printing').length;
  const doneToday=orders.filter(o=>['completed','delivered'].includes(o.status)&&new Date(o.created_at).toDateString()===today).length;
  document.getElementById('liveInProg').textContent=inProg;
  document.getElementById('liveDone').textContent=doneToday;
  document.getElementById('liveSub').textContent='Auto-refreshing every 30s';
}
async function loadLivePrint(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const inProg=orders.filter(o=>o.status==='confirmed'||o.status==='printing');
  const today=new Date().toDateString();
  const doneToday=orders.filter(o=>['completed','delivered'].includes(o.status)&&new Date(o.created_at).toDateString()===today);
  document.getElementById('lpInProg').textContent=inProg.length;
  document.getElementById('lpDone').textContent=doneToday.length;
  document.getElementById('lpCount').textContent=inProg.length;
  document.getElementById('lpTable').innerHTML=inProg.length?
    '<table><tr><th>#</th><th>User ID</th><th>Product</th><th>Qty</th><th>Status</th><th>Started</th></tr>'+
    inProg.map((o,i)=>'<tr><td>'+(i+1)+'</td><td class="uid">'+(o.user_id?.toString().slice(0,8)||'USR')+'</td><td>'+(o.product_name||'Print Job')+'</td><td>'+(o.copies||1)+'</td><td><span class="badge b-orange">in progress</span></td><td>'+fmtDate(o.created_at)+', '+fmtTime(o.created_at)+'</td></tr>').join('')+'</table>':
    '<div class="empty">No jobs currently in progress</div>';
}
async function loadPrintDone(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const allDone=orders.filter(o=>['completed','delivered'].includes(o.status));
  const inProg=orders.filter(o=>['confirmed','printing'].includes(o.status));
  const today=new Date().toDateString();
  const now=new Date();
  document.getElementById('pdTotal').textContent=allDone.length;
  document.getElementById('pdInProg').textContent=inProg.length;
  document.getElementById('pdToday').textContent=allDone.filter(o=>new Date(o.created_at).toDateString()===today).length;
  let filtered=[],labels=[],chartData=[];
  if(pdFilterMode==='daily'){
    labels=['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm'];
    filtered=allDone.filter(o=>new Date(o.created_at).toDateString()===today);
    chartData=labels.map((h,i)=>{const hr=(i+8)%24;return allDone.filter(o=>new Date(o.created_at).getHours()===hr&&new Date(o.created_at).toDateString()===today).reduce((s,o)=>s+(parseFloat(o.grand_total||o.total_amount||0)),0);});
  } else if(pdFilterMode==='weekly'){
    labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    const weekAgo=new Date();weekAgo.setDate(now.getDate()-7);
    filtered=allDone.filter(o=>new Date(o.created_at)>=weekAgo);
    chartData=labels.map((day,i)=>filtered.filter(o=>(new Date(o.created_at).getDay()||7)-1===i).reduce((s,o)=>s+(parseFloat(o.grand_total||o.total_amount||0)),0));
  } else {
    const from=new Date(document.getElementById('pdFromDate').value);
    const to=new Date(document.getElementById('pdToDate').value);to.setHours(23,59,59);
    filtered=allDone.filter(o=>new Date(o.created_at)>=from&&new Date(o.created_at)<=to);
    const diff=Math.ceil((to-from)/(1000*60*60*24))+1;
    for(let i=0;i<diff;i++){const day=new Date(from);day.setDate(from.getDate()+i);labels.push(day.toLocaleDateString('en-GB',{day:'2-digit',month:'short'}));chartData.push(filtered.filter(o=>new Date(o.created_at).toDateString()===day.toDateString()).reduce((s,o)=>s+(parseFloat(o.grand_total||o.total_amount||0)),0));}
  }
  buildPdChart(labels,chartData);
  document.getElementById('pdCount').textContent=filtered.length;
  document.getElementById('pdTable').innerHTML=filtered.length?
    '<table><tr><th>User ID</th><th>Product</th><th>Qty</th><th>Status</th><th>Completed</th></tr>'+
    filtered.map(o=>'<tr><td class="uid">'+(o.user_id?.toString().slice(0,8)||'USR')+'</td><td>'+(o.product_name||'Print Job')+'</td><td>'+(o.copies||1)+'</td><td><span class="badge b-green">done</span></td><td>'+fmtDate(o.completed_at||o.created_at)+', '+fmtTime(o.completed_at||o.created_at)+'</td></tr>').join('')+'</table>':
    '<div class="empty">No completed jobs for this period</div>';
}
let pdayFilterMode='daily';
let pdayChartObj=null;
function setPdayFilter(mode,el){
  pdayFilterMode=mode;
  document.querySelectorAll('.pd-filter-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('pdayCustomBox').style.display=mode==='custom'?'flex':'none';
  if(mode!=='custom') loadPaymentDay();
}
function applyPdayCustom(){
  const f=document.getElementById('pdayFromDate').value;
  const t=document.getElementById('pdayToDate').value;
  if(!f||!t)return alert('Select both dates');
  loadPaymentDay();
}
function buildPdayChart(labels,data){
  const canvas=document.getElementById('pdayChart');
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  if(pdayChartObj)pdayChartObj.destroy();
  pdayChartObj=new Chart(ctx,{
    type:'bar',
    data:{labels:labels,datasets:[{label:'Payment (Rs)',data:data,backgroundColor:'rgba(255,87,34,0.75)',borderColor:'#ff5722',borderWidth:1,borderRadius:4}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
      scales:{
        y:{min:0,ticks:{callback:function(v){return 'Rs'+v;}},grid:{color:'#f0f0f0'},title:{display:true,text:'Amount (Rs)'}},
        x:{grid:{display:false},title:{display:true,text:'Time'}}
      }
    }
  });
}
async function loadPaymentDay(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const now=new Date();
  const today=now.toDateString();
  let filtered=[],labels=[],chartData=[];
  if(pdayFilterMode==='daily'){
    labels=['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm'];
    filtered=orders.filter(o=>new Date(o.created_at).toDateString()===today);
    chartData=labels.map((h,i)=>{const hr=(i+8)%24;return orders.filter(o=>new Date(o.created_at).getHours()===hr&&new Date(o.created_at).toDateString()===today).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0);});
  } else if(pdayFilterMode==='weekly'){
    labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    const weekAgo=new Date();weekAgo.setDate(now.getDate()-7);
    filtered=orders.filter(o=>new Date(o.created_at)>=weekAgo);
    chartData=labels.map((day,i)=>filtered.filter(o=>(new Date(o.created_at).getDay()||7)-1===i).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0));
  } else {
    const from=new Date(document.getElementById('pdayFromDate').value);
    const to=new Date(document.getElementById('pdayToDate').value);to.setHours(23,59,59);
    filtered=orders.filter(o=>new Date(o.created_at)>=from&&new Date(o.created_at)<=to);
    const diff=Math.ceil((to-from)/(1000*60*60*24))+1;
    for(let i=0;i<diff;i++){const day=new Date(from);day.setDate(from.getDate()+i);labels.push(day.toLocaleDateString('en-GB',{day:'2-digit',month:'short'}));chartData.push(filtered.filter(o=>new Date(o.created_at).toDateString()===day.toDateString()).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0));}
  }
  const total=filtered.reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0);
  document.getElementById('pdayTotal').textContent=total.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
  document.getElementById('pdayCount').textContent=filtered.length+' transactions';
  buildPdayChart(labels,chartData);
  document.getElementById('pdayTable').innerHTML=filtered.length?
    '<table><tr><th>User ID</th><th>Customer</th><th>Amount</th><th>Method</th><th>Date</th></tr>'+
    filtered.map(o=>'<tr><td class="uid">'+(o.user_id?.toString().slice(0,8)||'USR')+'</td><td>'+(o.user_name||'Customer')+'</td><td style="color:#1b7a3d;font-weight:700">&#8377;'+(parseFloat(o.grand_total)||0).toLocaleString('en-IN')+'</td><td><span class="badge b-dark">'+(o.payment_method||'upi')+'</span></td><td>'+fmtDate(o.created_at)+' '+fmtTime(o.created_at)+'</td></tr>').join('')+'</table>':
    '<div class="empty">No payments for this period</div>';
}
let phFilterMode='daily';
function setPhFilter(mode,el){
  phFilterMode=mode;
  document.querySelectorAll('.pd-filter-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  loadPaymentHist();
}
async function loadPaymentHist(){
  const d=await api('/api/v1/orders');
  const orders=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  const now=new Date();
  const today=now.toDateString();
  let filtered=[],labels=[],chartData=[];
  if(phFilterMode==='daily'){
    labels=['8am','9am','10am','11am','12pm','1pm','2pm','3pm','4pm','5pm','6pm','7pm','8pm'];
    filtered=orders.filter(o=>new Date(o.created_at).toDateString()===today);
    chartData=labels.map((h,i)=>{const hr=(i+8)%24;return orders.filter(o=>new Date(o.created_at).getHours()===hr&&new Date(o.created_at).toDateString()===today).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0);});
  } else {
    labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    const weekAgo=new Date();weekAgo.setDate(now.getDate()-7);
    filtered=orders.filter(o=>new Date(o.created_at)>=weekAgo);
    chartData=labels.map((day,i)=>filtered.filter(o=>(new Date(o.created_at).getDay()||7)-1===i).reduce((s,o)=>s+(parseFloat(o.grand_total)||0),0));
  }
  const ctx=document.getElementById('revChart').getContext('2d');
  if(revChartObj) revChartObj.destroy();
  revChartObj=new Chart(ctx,{
    type:'bar',
    data:{labels:labels,datasets:[{data:chartData,backgroundColor:'#ff5722',borderRadius:4,label:'Revenue (Rs)'}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
      scales:{
        y:{min:0,ticks:{callback:function(v){return 'Rs'+v;}},grid:{color:'#f0f0f3'},title:{display:true,text:'Amount (Rs)'}},
        x:{grid:{display:false},title:{display:true,text:phFilterMode==='daily'?'Time':'Day'}}
      }
    }
  });
  document.getElementById('phCount').textContent=filtered.length;
  document.getElementById('phWeeks').innerHTML=filtered.length?
    '<table><tr><th>Date</th><th>User ID</th><th>Customer</th><th>Amount</th><th>Method</th></tr>'+
    filtered.map(o=>'<tr><td>'+fmtDate(o.created_at)+' '+fmtTime(o.created_at)+'</td><td class="uid">'+(o.user_id?.toString().slice(0,8)||'USR')+'</td><td>'+(o.user_name||'Customer')+'</td><td style="color:#1b7a3d;font-weight:700">Rs '+(parseFloat(o.grand_total)||0).toLocaleString('en-IN')+'</td><td><span class="badge b-dark">'+(o.payment_method||'upi')+'</span></td></tr>').join('')+'</table>':
    '<div class="empty">No payment history for this period</div>';
}
async function loadDelivery(){
  const d=await api('/api/v1/delivery-persons');
  const agents=Array.isArray(d)?d:(d?.data||[]);
  document.getElementById('dpCount').textContent=agents.length;
  document.getElementById('dpList').innerHTML=agents.length?agents.map(a=>'<div class="dp-card"><div><div class="dp-name">'+a.name+'</div><div class="dp-meta">Age: '+(a.age||'+ï¿½+ï¿½+ï¿½')+' &bull; +91 '+(a.phone||'+ï¿½+ï¿½+ï¿½')+'</div><div class="dp-docs">Aadhar: '+(a.aadhar||'+ï¿½+ï¿½+ï¿½')+' &bull; PAN: '+(a.pan||'+ï¿½+ï¿½+ï¿½')+'</div><span class="badge b-blue" style="margin-top:6px;display:inline-block">'+(a.vehicle_number||'+ï¿½+ï¿½+ï¿½')+'</span></div><button class="icon-del" onclick="delAgent(\''+a.id+'\')">&#128465;</button></div>').join(''):'<div class="empty">No delivery persons yet</div>';
}
async function addDelivery(){
  const name=document.getElementById('dpName').value,phone=document.getElementById('dpPhone').value;
  if(!name||!phone) return alert('Name and phone required');
  await api('/api/v1/delivery-persons?shop_id=shop-001','POST',{
    name,phone,age:parseInt(document.getElementById('dpAge').value)||null,
    vehicle_number:document.getElementById('dpVehicle').value,
    aadhar:document.getElementById('dpAadhar').value,
    pan:document.getElementById('dpPan').value
  });
  ['dpName','dpAge','dpPhone','dpAadhar','dpPan','dpVehicle'].forEach(id=>document.getElementById(id).value='');
  loadDelivery();
}
async function delAgent(id){if(confirm('Remove this delivery person?')){await api('/api/v1/delivery-persons/'+id,'DELETE');loadDelivery();}}
let cuFilterMode='all';
let allProjects=[];
function setCuFilter(mode,el){
  cuFilterMode=mode;
  document.querySelectorAll('.pd-filter-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  renderProjects();
}
function renderProjects(){
  const SM={confirmed:'pending',processing:'pending',pending:'pending',printed:'approved',completed:'approved',delivered:'approved',cancelled:'rejected'};
  let list=cuFilterMode==='all'?allProjects:allProjects.filter(function(o){return (SM[o.status]||'pending')===cuFilterMode;});
  document.getElementById('cuCount').textContent=list.length;
  if(!list.length){document.getElementById('cuTable').innerHTML='<div class="empty">No projects found</div>';return;}
  let html='<div style="display:flex;flex-direction:column;gap:14px;padding:16px">';
  for(let i=0;i<list.length;i++){
    const o=list[i];
    const st=SM[o.status]||'pending';
    const bc=st==='approved'?'b-green':st==='rejected'?'b-red':'b-orange';
    const files=o.files||[];
    let filesHtml='';
    for(let j=0;j<files.length;j++){
      const f=files[j];
      filesHtml+='<div style="background:#f5f7fa;border-radius:8px;padding:8px 12px;font-size:.82rem">'+
        '<div style="font-weight:600;color:#1a223e">'+String.fromCodePoint(128196)+' '+(f.original_filename||'file')+'</div>'+
        '<div style="color:#666;margin-top:2px">'+f.copies+' copies - '+(f.print_color||'bw')+' - '+(f.file_type||'doc')+'</div>'+
        '<div style="color:#ff5722;font-weight:700;margin-top:2px">Rs '+(f.file_cost||0)+'</div></div>';
    }
    let btns='<div style="font-size:.8rem;color:#999">'+o.delivery_type+'</div>';
    if(st==='pending'){
      btns='<div style="display:flex;gap:8px">'+
        '<button id="ap_'+o.id+'" onclick="approveProject(this.id.slice(3))" style="padding:7px 16px;background:#22b573;color:#fff;border:none;border-radius:8px;font-size:.83rem;font-weight:600;cursor:pointer">Approve</button>'+
        '<button id="rj_'+o.id+'" onclick="rejectProject(this.id.slice(3))" style="padding:7px 16px;background:#e74c3c;color:#fff;border:none;border-radius:8px;font-size:.83rem;font-weight:600;cursor:pointer">Reject</button>'+
        '</div>';
    }
    html+='<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:18px">'+
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">'+
      '<div><div style="font-weight:700;font-size:.95rem;color:#1a223e">'+(o.order_number||o.id.slice(0,12))+'</div>'+
      '<div style="font-size:.8rem;color:#999;margin-top:3px">'+fmtDate(o.created_at)+' '+fmtTime(o.created_at)+'</div></div>'+
      '<span class="badge '+bc+'">'+st+'</span></div>'+
      '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px">'+filesHtml+'</div>'+
      '<div style="display:flex;justify-content:space-between;align-items:center">'+
      '<div style="font-weight:800;color:#1a223e">Total: Rs '+o.grand_total+'</div>'+btns+
      '</div></div>';
  }
  html+='</div>';
  document.getElementById('cuTable').innerHTML=html;
}

async function loadCustomers(){
  const d=await api('/api/v1/orders');
  allProjects=Array.isArray(d)?d:(d?.data||d?.orders||[]);
  renderProjects();
}
async function approveProject(id){await api('/api/v1/orders/'+id,'PUT',{status:'printed'});loadCustomers();}
async function rejectProject(id){await api('/api/v1/orders/'+id,'PUT',{status:'cancelled'});loadCustomers();}

let curOtPerm='blue';
function setOtPerm(type){
  curOtPerm=type;
  document.getElementById('otPermBlue').classList.toggle('on',type==='blue');
  document.getElementById('otPermWhite').classList.toggle('on',type==='white');
}
async function loadOutlets(){
  const d=await api('/api/v1/shops');
  allOutlets=Array.isArray(d)?d:(d?.data||[]);
  filterOutlets('all',document.querySelector('#pg-outlet .tab-btn.on'));
}
function filterOutlets(type,el){
  document.querySelectorAll('#pg-outlet .tab-btn').forEach(t=>t.classList.remove('on'));
  if(el) el.classList.add('on');
  const list=type==='all'?allOutlets:allOutlets.filter(o=>(o.permission_type||'blue')===type);
  document.getElementById('otCount').textContent=list.length;
  if(!list.length){document.getElementById('otTable').innerHTML='<div class="empty">No outlets yet</div>';return;}
  document.getElementById('otTable').innerHTML='<div style="display:flex;flex-direction:column;gap:12px;padding:16px">'+
  list.map(function(o){
    const perm=o.permission_type||'blue';
    const permBadge=perm==='white'?'<span class="badge b-blue">White (Own)</span>':'<span class="badge b-purple">Blue (Franchise)</span>';
    const statusBadge=o.is_active?'<span class="badge b-green">Active</span>':'<span class="badge b-red">Inactive</span>';
    const hasZone=(o.latitude&&o.longitude);
    return '<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:16px">'+
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">'+
      '<div><div style="font-weight:800;font-size:.95rem;color:#1a223e">'+o.name+'</div>'+
      '<div style="font-size:.8rem;color:#999;margin-top:2px">'+(o.city||'')+(o.state?', '+o.state:'')+'</div></div>'+
      '<div style="display:flex;gap:6px">'+permBadge+statusBadge+'</div></div>'+
      '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.82rem;margin-bottom:10px">'+
      '<div><span style="color:#999;font-weight:600">Login ID:</span> '+(o.owner_email?o.owner_email.split('@')[0]:'ï¿½')+'</div>'+
      '<div><span style="color:#999;font-weight:600">Owner:</span> '+(o.owner_name||'ï¿½')+'</div>'+
      '<div><span style="color:#999;font-weight:600">Phone:</span> '+(o.owner_phone||'ï¿½')+'</div>'+
      '<div><span style="color:#999;font-weight:600">Pincode:</span> '+(o.pincode||'ï¿½')+'</div>'+
      '<div><span style="color:#999;font-weight:600">Radius:</span> '+(o.delivery_radius_km||5)+' km</div>'+
      (hasZone?'<div><span style="color:#999;font-weight:600">Lat:</span> '+o.latitude+'</div>'+
      '<div><span style="color:#999;font-weight:600">Lng:</span> '+o.longitude+'</div>':
      '<div colspan="2" style="color:#e74c3c;font-size:.78rem">&#9888; No zone set</div>')+
      '</div>'+
      '<div style="display:flex;justify-content:space-between;align-items:center">'+
      '<div style="font-size:.78rem;color:#999">'+(o.address||'No address')+'</div>'+
      '<div style="display:flex;gap:6px">'+
      '<button id="tog_'+o.id+'" onclick="toggleOutlet(this.id.slice(4))" style="padding:5px 12px;background:'+(o.is_active?'#e74c3c':'#22b573')+';color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">'+(o.is_active?'Deactivate':'Activate')+'</button>'+
      '<button id="del_'+o.id+'" onclick="delOutlet(this.id.slice(4))" style="padding:5px 12px;background:#e74c3c;color:#fff;border:none;border-radius:6px;font-size:.78rem;cursor:pointer">Delete</button>'+
      '</div></div></div>';
  }).join('')+'</div>';
}
async function addOutlet(){
  const name=document.getElementById('otName').value;
  const owner=document.getElementById('otOwner').value;
  const loginId=document.getElementById('otLoginId').value;
  const password=document.getElementById('otPassword').value;
  if(!name||!owner) return alert('Outlet name and owner required');
  const loginEmail=loginId?loginId+'@altprint.in':null;
  if(loginId&&password&&password.length<6) return alert('Password must be at least 6 characters');
  const lat=document.getElementById('otLat').value;
  const lng=document.getElementById('otLng').value;
  const shopResp=await api('/api/v1/shops','POST',{
    name:name,
    owner_name:owner,
    owner_phone:document.getElementById('otPhone').value,
    owner_email:document.getElementById('otEmail').value||loginEmail||('outlet'+Date.now()+'@altprint.in'),
    city:document.getElementById('otCity').value,
    state:document.getElementById('otState').value,
    pincode:document.getElementById('otPin').value,
    address:document.getElementById('otAddr').value,
    latitude:lat?parseFloat(lat):null,
    longitude:lng?parseFloat(lng):null,
    delivery_radius_km:parseFloat(document.getElementById('otRadius').value)||5,
    permission_type:curOtPerm,
    is_active:true
  });
  const newShopId=shopResp&&shopResp.data&&shopResp.data.id;
  if(loginId&&password&&newShopId){
    try{
      await api('/api/v1/admin/create-shop-login','POST',{email:loginEmail,password:password,full_name:owner,shop_id:newShopId});
    }catch(e){
      alert('Outlet was created, but the login account could not be set up (the email may already be in use). You can add a login later.');
    }
  }
  ['otName','otOwner','otPhone','otEmail','otCity','otState','otPin','otAddr','otLat','otLng','otLoginId','otPassword'].forEach(id=>document.getElementById(id).value='');
  loadOutlets();
  alert('Outlet added!');
}
async function toggleOutlet(id){const el=document.getElementById('tog_'+id);const active=el.textContent.trim()==='Activate';await api('/api/v1/shops/'+id,'PUT',{is_active:active});loadOutlets();}
async function delOutlet(id){if(confirm('Delete this outlet?')){await api('/api/v1/shops/'+id,'DELETE');loadOutlets();}}

async function loadSubAdmins(){
  const d=await api('/api/v1/admin/users');
  allSubAdmins=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='sub-admin'||u.role==='admin');
  document.getElementById('saCount').textContent=allSubAdmins.length;
  document.getElementById('saTable').innerHTML=allSubAdmins.length?
    '<table><tr><th>User ID</th><th>Name</th><th>Role</th><th>Created</th><th></th></tr>'+
    allSubAdmins.map((u,i)=>'<tr><td class="uid">SA'+String(i+1).padStart(3,'0')+'</td><td>'+(u.full_name||u.name||'+ï¿½+ï¿½+ï¿½')+'</td><td><span class="badge b-dark">'+(u.role||'sub-admin')+'</span></td><td>'+fmtDate(u.created_at)+'</td><td><button class="icon-del" onclick="delSubAdmin(\''+u.id+'\')">&#128465;</button></td></tr>').join('')+'</table>':
    '<div class="empty">No sub-admins yet</div>';
}
async function addSubAdmin(){
  const id=document.getElementById('saId').value,name=document.getElementById('saName').value,pass=document.getElementById('saPass').value,role=document.getElementById('saRole').value;
  if(!name||!pass) return alert('Name and password required');
  await api('/api/v1/auth/register','POST',{email:(id||'sa').toLowerCase()+'@altprint.in',password:pass,full_name:name,role:role||'sub-admin'});
  ['saId','saName','saPass'].forEach(i=>document.getElementById(i).value='');
  loadSubAdmins();
}
async function delSubAdmin(id){if(confirm('Remove this sub-admin?')){await api('/api/v1/admin/users/'+id,'DELETE');loadSubAdmins();}}
async function loadAccountMgmt(){
  const d=await api('/api/v1/admin/users');
  const users=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='user'||u.role==='customer');
  document.getElementById('amCount').textContent=users.length;
  document.getElementById('amTable').innerHTML=users.length?
    '<table><tr><th>User ID</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>'+
    users.map((u,i)=>{const active=u.is_active!==false;return'<tr><td class="uid">CUS'+String(i+1).padStart(3,'0')+'</td><td>'+(u.full_name||u.name||'Customer')+'</td><td>+91 '+(u.phone||'+ï¿½+ï¿½+ï¿½')+'</td><td><span class="badge '+(active?'b-green':'b-red')+'">'+(active?'active':'suspended')+'</span></td><td><button class="btn-sm '+(active?'btn-red':'btn-orange')+'" onclick="toggleUserStatus(\'+u.id+\','+(!active)+')">'+(active?'&#128683; Suspend':'&#128275; Activate')+'</button></td></tr>';}).join('')+'</table>':
    '<div class="empty">No customer accounts</div>';
}
async function toggleUserStatus(id,active){await api('/api/v1/admin/users/'+id+'/status?is_active='+active,'PATCH');loadAccountMgmt();}
async function loadTickets(){
  const d=await api('/api/v1/tickets');
  allTickets=Array.isArray(d)?d:(d?.data||[]);
  renderAllTickets();
}
function renderAllTickets(){
  const list=allTickets;
  document.getElementById('tkHd').innerHTML='All Tickets (<span id="tkCount">'+list.length+'</span>)';
  document.getElementById('tkList').innerHTML=list.length?list.map(t=>'<div class="ticket-item" style="cursor:pointer" onclick="showTicketDetail(\''+t.id+'\')"><div><div class="ticket-title"><b>'+(t.subject||'Issue')+'</b><span class="badge '+(t.status==='resolved'?'b-green':'b-yellow')+'">'+(t.status||'open')+'</span></div><div class="ticket-meta">Raised by: <b>'+(t.raised_by||'Anonymous')+'</b> &bull; '+fmtDate(t.created_at)+', '+fmtTime(t.created_at)+'</div><div class="ticket-desc">'+(t.description||'No details provided.')+'</div></div><button class="btn-sm" onclick="event.stopPropagation();resolveTicket(\''+t.id+'\')">&#10003; Resolve</button></div>').join(''):'<div class="empty">No tickets raised yet</div>';
}
function showTicketDetail(id){
  const t=allTickets.find(x=>x.id===id);
  if(!t)return;
  document.getElementById('tdName').textContent=t.raised_by||'Not provided';
  document.getElementById('tdSubject').textContent=t.subject||'Issue';
  document.getElementById('tdDesc').textContent=t.description||'No details provided.';
  document.getElementById('tdStatus').textContent=t.status||'open';
  document.getElementById('tdStatus').className='badge '+(t.status==='resolved'?'b-green':'b-yellow');
  const rb=document.getElementById('tdResolveBtn');
  rb.style.display=t.status==='resolved'?'none':'inline-block';
  rb.onclick=function(){resolveTicket(t.id);document.getElementById('ticketDetailModal').style.display='none';};
  document.getElementById('ticketDetailModal').style.display='flex';
}

async function resolveTicket(id){await api('/api/v1/tickets/'+id,'PATCH',{status:'resolved'});loadTickets();}
async function loadStock(){
  const d=await api('/api/v1/stock');
  allStock=Array.isArray(d)?d:(d?.data||[]);
  document.getElementById('skCount').textContent=allStock.length;
  document.getElementById('skTable').innerHTML=allStock.length?
    '<table><tr><th>Item Name</th><th>Quantity</th><th>Unit</th><th>Last Updated</th></tr>'+
    allStock.map(i=>'<tr><td><b>'+(i.item_name||i.name)+'</b></td><td style="color:'+((i.quantity||0)<10?'#e74c3c':'#1b7a3d')+';font-weight:700">'+i.quantity+'</td><td>'+(i.unit||'units')+'</td><td>'+fmtDate(i.updated_at||i.created_at)+'</td></tr>').join('')+'</table>':
    '<div class="empty">No stock items yet</div>';
  const td=await api('/api/v1/tickets');
  const tickets=(Array.isArray(td)?td:(td?.data||[])).filter(t=>t.status==='open'||!t.status);
  document.getElementById('skTkCount').textContent=tickets.length;
  document.getElementById('skTickets').innerHTML=tickets.length?tickets.map(t=>'<div style="border:1px solid #f0f0f3;border-radius:8px;padding:10px 12px;margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span class="badge b-yellow">'+(t.status||'open')+'</span><span style="font-size:.76rem;color:#aaa">'+(t.category==='customer'?'Customer':'Outlet')+'</span></div><div style="font-weight:700;font-size:.88rem;margin-top:6px">'+(t.subject||'Issue')+'</div><div style="font-size:.78rem;color:#aaa">'+((t.raised_by||'').toString().slice(0,8)||'+ï¿½+ï¿½+ï¿½')+'</div></div>').join(''):'<div class="empty">No open tickets</div>';
}

function setFont(font,el){
  document.querySelectorAll('#acFonts .font-btn').forEach(b=>b.classList.remove('on'));
  el.classList.add('on');
}
function updatePreview(){
  const prim=document.getElementById('acPrim').value||'#ff5722';
  document.getElementById('acPrimSw').style.background=prim;
  document.getElementById('acSecSw').style.background=document.getElementById('acSec').value||'#1a223e';
  document.getElementById('prevBanner').style.background=prim;
  document.getElementById('prevBanner').textContent=document.getElementById('acBanner').value||'PrintLab Admin';
  document.getElementById('prevLogo').style.background=prim;
  ['prevIc1','prevIc2','prevIc3'].forEach(id=>document.getElementById(id).style.background=prim);
}


function openRaiseTicket(){document.getElementById('raiseTicketModal').style.display='flex';}
async function submitRaiseTicket(){
  const subject=document.getElementById('rtSubject').value;
  if(!subject)return alert('Subject required');
  const r=await api('/api/v1/tickets','POST',{subject,description:document.getElementById('rtDesc').value,category:document.getElementById('rtCat').value,priority:'medium'});
  if(r&&r.id){document.getElementById('raiseTicketModal').style.display='none';loadTickets();alert('Ticket raised!');}
  else alert('Error raising ticket');
}

function loadAppControl(){loadSavedAppearance();loadFeatureFlags();}
async function loadSavedAppearance(){
  const a=await api('/api/v1/appearance');
  if(!a||a.detail)return;
  document.getElementById('acPrim').value=a.primary_color;
  document.getElementById('acPrimSw').style.background=a.primary_color;
  document.getElementById('acSec').value=a.secondary_color;
  document.getElementById('acSecSw').style.background=a.secondary_color;
  document.getElementById('acLogo').value=a.logo_url||'';
  document.getElementById('acBanner').value=a.banner_text;
  document.querySelectorAll('#acFonts .font-btn').forEach(b=>b.classList.toggle('on', b.textContent===a.font_family));
  updatePreview();
}
async function loadSysToggles(){
  const d=await api('/api/v1/system/config');
  if(!d){document.getElementById('sysToggles').innerHTML='<div class="empty">Error</div>';return;}
  const fields=[
    {key:'app_enabled',label:'App Enabled',icon:'&#128241;',color:'#22b573'},
    {key:'maintenance_mode',label:'Maintenance Mode',icon:'&#128295;',color:'#ff9800'},
    {key:'emergency_lock',label:'Emergency Lock',icon:'&#128274;',color:'#e74c3c'},
    {key:'uploads_enabled',label:'File Uploads',icon:'&#128196;',color:'#2979ff'},
    {key:'payments_enabled',label:'Payments',icon:'&#128179;',color:'#8e44ad'},
    {key:'delivery_enabled',label:'Delivery',icon:'&#128666;',color:'#ff7043'},
    {key:'printing_enabled',label:'Printing',icon:'&#128247;',color:'#16a085'},
    {key:'login_enabled',label:'Login/Register',icon:'&#128100;',color:'#3f51b5'},
    {key:'orders_enabled',label:'Orders',icon:'&#128230;',color:'#d4a017'},
  ];
  var html='';
  for(var i=0;i<fields.length;i++){
    var f=fields[i];
    var enabled=d[f.key];
    html+='<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center">'+
      '<div>'+
      '<div style="font-size:1.2rem;margin-bottom:4px">'+f.icon+'</div>'+
      '<div style="font-weight:700;font-size:.88rem">'+f.label+'</div>'+
      '<div style="font-size:.75rem;margin-top:3px;color:'+(enabled?'#22b573':'#e74c3c')+';font-weight:600">'+(enabled?'ENABLED':'DISABLED')+'</div>'+
      '</div>'+
      '<label style="position:relative;width:46px;height:24px;flex-shrink:0;cursor:pointer">'+
      '<input type="checkbox" '+(enabled?'checked':'')+' onchange="toggleSys(\'+f.key+\',this.checked)" style="opacity:0;width:0;height:0">'+
      '<span style="position:absolute;cursor:pointer;inset:0;background:'+(enabled?f.color:'#ccc')+';border-radius:24px;transition:.2s;display:block">'+
      '<span style="position:absolute;width:18px;height:18px;left:'+(enabled?'25px':'3px')+';bottom:3px;background:#fff;border-radius:50%;transition:.2s;display:block"></span>'+
      '</span></label></div>';
  }
  document.getElementById('sysToggles').innerHTML=html;
}

async function toggleSys(key,val){const b={};b[key]=val;await api('/api/v1/system/config','PUT',b);loadSysToggles();}
async function loadFeatToggles(){
  const d=await api('/api/v1/features');
  if(!Array.isArray(d)){document.getElementById('featToggles').innerHTML='<div class="empty">Error</div>';return;}
  var html='';
  for(var i=0;i<d.length;i++){
    var f=d[i];
    html+='<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center">'+
      '<div>'+
      '<div style="font-weight:700;font-size:.88rem">'+f.label+'</div>'+
      '<div style="font-size:.75rem;color:#999;margin-top:2px">'+f.feature_name+'</div>'+
      '<div style="font-size:.75rem;margin-top:3px;color:'+(f.enabled?'#22b573':'#e74c3c')+';font-weight:600">'+(f.enabled?'ON':'OFF')+'</div>'+
      '</div>'+
      '<label style="position:relative;width:46px;height:24px;flex-shrink:0;cursor:pointer">'+
      '<input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleFeat(\'+f.feature_name+\',this.checked)" style="opacity:0;width:0;height:0">'+
      '<span style="position:absolute;cursor:pointer;inset:0;background:'+(f.enabled?'#22b573':'#ccc')+';border-radius:24px;transition:.2s;display:block">'+
      '<span style="position:absolute;width:18px;height:18px;left:'+(f.enabled?'25px':'3px')+';bottom:3px;background:#fff;border-radius:50%;transition:.2s;display:block"></span>'+
      '</span></label></div>';
  }
  document.getElementById('featToggles').innerHTML=html;
}

async function toggleFeat(name,val){await api('/api/v1/features/toggle','POST',{feature_name:name,enabled:val,scope:'global'});loadFeatToggles();}
async function loadOutletShops(){
  const shops = await api('/api/v1/shops');
  const sel = document.getElementById('outletSel');
  if(!Array.isArray(shops) || !shops.length){ sel.innerHTML='<option value="">No outlets found</option>'; return; }
  sel.innerHTML = shops.map(function(s){return '<option value="'+s.id+'">'+s.name+'</option>';}).join('');
  loadOutletFeats();
}
async function loadOutletFeats(){
  const shopId = document.getElementById('outletSel').value;
  const box = document.getElementById('outletFeats');
  if(!shopId){ box.innerHTML=''; return; }
  box.innerHTML = '<div class="loading">Loading...</div>';
  const d = await api('/api/v1/features?shop_id='+shopId);
  if(!Array.isArray(d)){ box.innerHTML='<div class="empty">Error</div>'; return; }
  const wanted = ['black_white_print','color_print'];
  const filtered = d.filter(function(f){return wanted.indexOf(f.feature_name)!==-1;});
  var html='';
  for(var i=0;i<filtered.length;i++){
    var f=filtered[i];
    html+='<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center">'+
      '<div>'+
      '<div style="font-weight:700;font-size:.88rem">'+f.label+'</div>'+
      '<div style="font-size:.75rem;color:#999;margin-top:2px">'+f.feature_name+'</div>'+
      '<div style="font-size:.75rem;margin-top:3px;color:'+(f.enabled?'#22b573':'#e74c3c')+';font-weight:600">'+(f.enabled?'ON':'OFF')+'</div>'+
      '</div>'+
      '<label style="position:relative;width:46px;height:24px;flex-shrink:0;cursor:pointer">'+
      '<input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleOutletFeat(&quot;'+f.feature_name+'&quot;,this.checked)" style="opacity:0;width:0;height:0">'+
      '<span style="position:absolute;cursor:pointer;inset:0;background:'+(f.enabled?'#22b573':'#ccc')+';border-radius:24px;transition:.2s;display:block">'+
      '<span style="position:absolute;width:18px;height:18px;left:'+(f.enabled?'25px':'3px')+';bottom:3px;background:#fff;border-radius:50%;transition:.2s;display:block"></span>'+
      '</span></label></div>';
  }
  box.innerHTML = html || '<div class="empty">No matching flags for this outlet</div>';
}
async function toggleOutletFeat(name,val){
  const shopId = document.getElementById('outletSel').value;
  await api('/api/v1/features/toggle','POST',{feature_name:name,enabled:val,shop_id:shopId});
  loadOutletFeats();
}

function setFont(font,el){document.querySelectorAll('#acFonts .font-btn').forEach(b=>b.classList.remove('on'));el.classList.add('on');}
function updatePreview(){
  const prim=document.getElementById('acPrim').value||'#ff5722';
  document.getElementById('acPrimSw').style.background=prim;
  document.getElementById('acSecSw').style.background=document.getElementById('acSec').value||'#1a223e';
  document.getElementById('prevBanner').style.background=prim;
  document.getElementById('prevBanner').textContent=document.getElementById('acBanner').value||'PrintLab';
  document.getElementById('prevLogo').style.background=prim;
  ['prevIc1','prevIc2','prevIc3'].forEach(id=>document.getElementById(id).style.background=prim);
}
async function saveAppSettings(){
  const font=document.querySelector('#acFonts .font-btn.on')?.textContent||'Inter';
  const s={primary_color:document.getElementById('acPrim').value,secondary_color:document.getElementById('acSec').value,font_family:font,logo_url:document.getElementById('acLogo').value,banner_text:document.getElementById('acBanner').value};
  const r=await api('/api/v1/appearance','PUT',s);
  if(r&&r.data)alert('Appearance saved!');else alert('Error saving - check console');
}

let pdFilterMode='daily';
let pdChartObj=null;
function setPdFilter(mode,el){
  pdFilterMode=mode;
  document.querySelectorAll('.pd-filter-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('pdCustomBox').style.display=mode==='custom'?'flex':'none';
  if(mode!=='custom') loadPrintDone();
}
function applyPdCustom(){
  const f=document.getElementById('pdFromDate').value;
  const t=document.getElementById('pdToDate').value;
  if(!f||!t) return alert('Select both dates');
  loadPrintDone();
}
function buildPdChart(labels,data){
  try{
  const canvas=document.getElementById('pdChart');
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  if(window._pdChart) window._pdChart.destroy();
  window._pdChart=new Chart(ctx,{
    type:'bar',
    data:{
      labels:labels,
      datasets:[{
        label:'Payment (Rs)',
        data:data.length?data:labels.map(()=>0),
        backgroundColor:'rgba(26,34,62,0.7)',
        borderColor:'#1a223e',
        borderWidth:1,
        borderRadius:4
      }]
    },
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        y:{min:0,max:5000,ticks:{callback:function(v){return 'Rs'+v;}},grid:{color:'#f0f0f0'},title:{display:true,text:'Payment (Rs)'}},
        x:{grid:{display:false},title:{display:true,text:'Time'}}
      }
    }
  });
  }catch(e){console.error('Chart error:',e);}
}
function buildPdChart_old(labels,data){
  if(pdChartObj) pdChartObj.destroy();
  const ctx=document.getElementById('pdChart').getContext('2d');
  pdChartObj=new Chart(ctx,{type:'bar',data:{labels:labels,datasets:[{label:'Payment (Rs)',data:data,backgroundColor:'rgba(26,34,62,0.7)',borderColor:'#1a223e',borderWidth:1,borderRadius:6}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{min:0,max:5000,ticks:{callback:v=>'Rs'+v},grid:{color:'#f0f0f0'}},x:{grid:{display:false}}}}});
}
