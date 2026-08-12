import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Update rJ() column: Order->Download, Status->Complete, Completed->Out for Delivery ----
old_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>'))+'</td>'"""

new_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')))+'</td>'"""

c1 = content.count(old_col)
print(f"rJ() column anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_col, new_col)
    print("rJ() updated with 3-way button logic")
else:
    print("WARNING: rJ() column anchor not found")

# ---- 2. Add markOutForDelivery() function next to markComplete() ----
old_fn = "async function showDelivery(el){"
new_fn = """async function markOutForDelivery(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=out_for_delivery',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark out for delivery');return;}
    await loadJ();
    rJ(allOrds.filter(o=>o.status==='ready'));
  }catch(e){alert('Failed to mark out for delivery');}
}

async function showDelivery(el){"""

c2 = content.count(old_fn)
print(f"showDelivery anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_fn, new_fn)
    print("markOutForDelivery() function added")
else:
    print("WARNING: showDelivery anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
