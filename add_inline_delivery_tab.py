import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Restyle the button to match .ttab and call showDelivery() instead of window.open ----
old_btn = """          <button onclick="window.open('/static/delivery_tracking.html','_blank')" style="margin-left:auto;background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer">&#128666; Out for Delivery</button>"""

new_btn = """          <button class="ttab" style="margin-left:auto" onclick="showDelivery(this)">&#128666; Out for Delivery</button>"""

c1 = content.count(old_btn)
print(f"Button anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_btn, new_btn)
    print("Button restyled to match tabs")
else:
    print("WARNING: button anchor not found")

# ---- 2. Add showDelivery() function that swaps table content in place ----
old_fn = "async function markComplete(orderId){"
new_fn = """async function showDelivery(el){
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

async function markComplete(orderId){"""

c2 = content.count(old_fn)
print(f"markComplete anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_fn, new_fn)
    print("showDelivery() function added")
else:
    print("WARNING: markComplete anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
