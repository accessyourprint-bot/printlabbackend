import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Patch 1: add markOutForDelivery function after markComplete ---
old1 = """  }catch(e){alert('Failed to mark complete');}
}

function fj(t,el){"""

new1 = """  }catch(e){alert('Failed to mark complete');}
}

async function markOutForDelivery(orderId){
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
}

function fj(t,el){"""

c1 = content.count(old1)
print(f"Patch 1 anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
    print("markOutForDelivery() added")
else:
    print("WARNING: Patch 1 anchor not unique, aborting")
    exit()

# --- Patch 2: make the Status column dynamic + clickable ---
old2 = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<span style="background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>'
        +'</td>'
        +'</tr>';"""

new2 = """        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +(o.status==='out_for_delivery'
          ?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; Out for Delivery</span>'
          :'<span onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="cursor:pointer;background:#f0fdf4;color:#16a34a;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#10003; Completed</span>')
        +'</td>'
        +'</tr>';"""

c2 = content.count(old2)
print(f"Patch 2 anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
    print("Status column made dynamic + clickable")
else:
    print("WARNING: Patch 2 anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
