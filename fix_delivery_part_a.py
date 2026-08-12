import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Remove the dead duplicate markOutForDelivery (the first, unused one) ---
old1 = """async function markOutForDelivery(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    rJ(allOrds.filter(o=>o.status==='ready'));
  }catch(e){alert('Failed to mark out for delivery');}
}

async function showDelivery(el){"""

new1 = """async function showDelivery(el){"""

c1 = content.count(old1)
print(f"[1] dead duplicate found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
else:
    print("ABORT [1]"); exit()

# --- 2. Update the real markOutForDelivery to accept delivery_person_id, and add picker functions ---
old2 = """async function markOutForDelivery(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
    const ofdBtn = Array.from(document.querySelectorAll('.stabs .ttab')).find(b=>b.textContent.trim()==='Out for Delivery');
    if(ofdBtn){ofdBtn.classList.add('on');}
    curStabFilter='out_for_delivery';
    rJ(allOrds.filter(o=>o.status==='out_for_delivery'));
  }catch(e){alert('Failed to mark out for delivery');}
}"""

new2 = """async function markOutForDelivery(orderId,deliveryPersonId){
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
}"""

c2 = content.count(old2)
print(f"[2] real markOutForDelivery found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
else:
    print("ABORT [2]"); exit()

# --- 3. Route the Completed badge click through the picker instead of directly marking ---
old3 = """        +(o.status==='out_for_delivery'
          ?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; Out for Delivery</span>'
          :'<span onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="cursor:pointer;background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>')
        +'</td>'
        +'</tr>';"""

new3 = """        +(o.status==='out_for_delivery'
          ?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; Out for Delivery</span>'
          :'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>')
        +'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(o.status==='out_for_delivery'
          ?'<span style="color:#999;font-size:12px">Assigned</span>'
          :'<button onclick="openOFDPicker(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>')
        +'</td>'
        +'</tr>';"""

c3 = content.count(old3)
print(f"[3] Completed badge block found {c3} time(s)")
if c3 == 1:
    content = content.replace(old3, new3)
else:
    print("ABORT [3]"); exit()

# --- 4. Add "Action" column header for the Completed table ---
old4 = """      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Download</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Status</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }"""

new4 = """      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Download</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Status</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Action</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;
  }"""

c4 = content.count(old4)
print(f"[4] header row found {c4} time(s)")
if c4 == 1:
    content = content.replace(old4, new4)
else:
    print("ABORT [4]"); exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PART A APPLIED (1-4)")
