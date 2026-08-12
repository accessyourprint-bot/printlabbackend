import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 5. Make Delivery Team cards clickable, add showPartnerOrders function ---
old5 = """    document.getElementById('dtB').innerHTML=ag.length
      ?ag.map(a=>'<div class="ag"><div class="av">&#128100;</div><div><div class="an">'+a.name+'</div><div class="aa">'+(a.age?'Age '+a.age:'')+'</div><div class="ai"><span>&#128222; '+(a.phone||'&mdash;')+'</span><span>&#128661; '+(a.vehicle_number||'&mdash;')+'</span></div></div></div>').join('')
      :'<div class="empty">No delivery persons yet</div>';
  }catch(e){document.getElementById('dtB').innerHTML='<div class="empty">Error loading</div>';}
}

function openAA(){"""

new5 = """    document.getElementById('dtB').innerHTML=ag.length
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

function openAA(){"""

c5 = content.count(old5)
print(f"[5] openDT/openAA block found {c5} time(s)")
if c5 == 1:
    content = content.replace(old5, new5)
else:
    print("ABORT [5]"); exit()

# --- 6. Insert the two new modals before </body> ---
old6 = "</script>\n</body>"
new6 = """<!-- OUT FOR DELIVERY PICKER MODAL -->
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

c6 = content.count(old6)
print(f"[6] </body> anchor found {c6} time(s)")
if c6 == 1:
    content = content.replace(old6, new6)
else:
    print("ABORT [6]"); exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PART B APPLIED (5-6)")
