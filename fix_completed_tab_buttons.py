import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    let rows=jobs.map(function(o){
      return '<tr>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c;font-size:14px">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_name||o.customer_name||'Customer')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'+((o.files&&o.files.length)?'<button onclick="openDeliveryDetailsPage(&quot;'+o.id+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')+'</td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Order ID</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Customer Name</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Phone Number</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Status</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;"""

new = """    let rows=jobs.map(function(o){
      const hasFiles=(o.files&&o.files.length);
      return '<tr>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c;font-size:14px">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_name||o.customer_name||'Customer')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee;font-size:14px">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
        +'<td style="padding:16px 20px;border-bottom:1px solid #eee">'
        +'<div style="display:flex;flex-direction:column;gap:6px;align-items:flex-start">'
        +'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>'
        +(hasFiles?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:8px;padding:8px 18px;font-size:13px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')
        +'</div>'
        +'</td>'
        +'</tr>';
    }).join('');
    jl.innerHTML = '<table style="width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:#fff;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">'
      +'<thead><tr style="background:#f8f8fa;text-align:left">'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Order ID</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Customer Name</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Phone Number</th>'
      +'<th style="padding:14px 20px;border-bottom:2px solid #ddd;font-size:15px;font-weight:700">Out for Delivery</th>'
      +'</tr></thead><tbody>'+rows+'</tbody></table>';
    return;"""

c = content.count(old)
print(f"Completed-branch anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Completed tab rows updated: Out for Delivery + Download stacked")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
