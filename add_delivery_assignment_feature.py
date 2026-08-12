import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Add "Out for Delivery" button back to Completed tab rows ---
old1 = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>'
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
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }"""

new1 = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>'
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<button onclick="openOFDPicker(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>'
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
  }"""

c1 = content.count(old1)
print(f"[1] Completed-tab block found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
else:
    print("ABORT [1]"); exit()

# --- 2. Update markOutForDelivery to accept a delivery_person_id ---
old2 = """async function markOutForDelivery(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    rJ(allOrds.filter(o=>o.status==='ready'));
  }catch(e){alert('Failed to mark out for delivery');}
}"""

new2 = """async function markOutForDelivery(orderId,deliveryPersonId){
  try{
    let url=API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery';
    if(deliveryPersonId) url+='&delivery_person_id='+deliveryPersonId;
    const resp = await fetch(url,{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    rJ(allOrds.filter(o=>o.status==='completed'||o.status==='ready'));
  }catch(e){alert('Failed to mark out for delivery');}
}

let _ofdOrderId=null;
async function openOFDPicker(orderId){
  _ofdOrderId=orderId;
  const body=document.getElementById('ofdB');
  body.innerHTML='<div class="loading">Loading&#8230;</div>';
  oMo('ofdMo');
  try{
    const d=await api('/api/v1/delivery-persons');
    const persons=Array.isArray(d)?d:(d.data||[]);
    body.innerHTML=persons.length
      ? persons.map(p=>'<div class="ag" style="cursor:pointer" onclick="confirmOFD(&quot;'+p.id+'&quot;)"><div class="av">&#128666;</div><div><div class="an">'+p.name+'</div><div class="ai"><span>&#128222; '+(p.phone||'&mdash;')+'</span><span>&#128661; '+(p.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      : '<div class="empty">No delivery persons added yet. Add one from Delivery Team first.</div>';
  }catch(e){ body.innerHTML='<div class="empty">Error loading delivery team</div>'; }
}
function confirmOFD(personId){
  cMo('ofdMo');
  markOutForDelivery(_ofdOrderId, personId);
}"""

c2 = content.count(old2)
print(f"[2] markOutForDelivery found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
else:
    print("ABORT [2]"); exit()

# --- 3. Make Delivery Team cards clickable to show their assigned orders ---
old3 = """    document.getElementById('dtB').innerHTML=ag.length
      ?ag.map(a=>'<div class="ag"><div class="av">&#128100;</div><div><div class="an">'+a.name+'</div><div class="aa">'+(a.age?'Age '+a.age:'')+'</div><div class="ai"><span>&#128222; '+(a.phone||'&mdash;')+'</span><span>&#128661; '+(a.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      :'<div class="empty">No delivery persons yet</div>';"""

new3 = """    document.getElementById('dtB').innerHTML=ag.length
      ?ag.map(a=>'<div class="ag" style="cursor:pointer" onclick="showPartnerOrders(&quot;'+a.id+'&quot;,&quot;'+a.name.replace(/"/g,'')+'&quot;)"><div class="av">&#128100;</div><div><div class="an">'+a.name+'</div><div class="aa">'+(a.age?'Age '+a.age:'')+'</div><div class="ai"><span>&#128222; '+(a.phone||'&mdash;')+'</span><span>&#128661; '+(a.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      :'<div class="empty">No delivery persons yet</div>';"""

c3 = content.count(old3)
print(f"[3] Delivery cards render found {c3} time(s)")
if c3 == 1:
    content = content.replace(old3, new3)
else:
    print("ABORT [3]"); exit()

# --- 4. Add showPartnerOrders function ---
old4 = "function openAA(){"
new4 = """async function showPartnerOrders(personId,personName){
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

function openAA(){"""

c4 = content.count(old4)
print(f"[4] openAA anchor found {c4} time(s)")
if c4 == 1:
    content = content.replace(old4, new4)
else:
    print("ABORT [4]"); exit()

# --- 5. Insert the two new modals before </body> ---
old5 = "</script>\n</body>"
new5 = """<!-- OUT FOR DELIVERY PICKER MODAL -->
<div id="ofdMo" class="mo hidden">
  <div class="mb">
    <div class="mh">
      <div><h3>Assign Delivery Partner</h3><p>Choose who will deliver this order.</p></div>
      <button class="mx" onclick="cMo('ofdMo')">&#10005;</button>
    </div>
    <div class="mbody" id="ofdB"><div class="loading">Loading&#8230;</div></div>
  </div>
</div>

<!-- PARTNER ORDERS MODAL -->
<div id="poMo" class="mo hidden">
  <div class="mb mb-wide">
    <div class="mh">
      <div><h3>Orders for <span id="poName"></span></h3><p>All orders currently assigned to this partner.</p></div>
      <button class="mx" onclick="cMo('poMo')">&#10005;</button>
    </div>
    <div class="mbody" id="poB"><div class="loading">Loading&#8230;</div></div>
  </div>
</div>

</script>
</body>"""

c5 = content.count(old5)
print(f"[5] </body> anchor found {c5} time(s)")
if c5 == 1:
    content = content.replace(old5, new5)
else:
    print("ABORT [5]"); exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("ALL PATCHES APPLIED")
