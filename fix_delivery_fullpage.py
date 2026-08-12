import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "function rJ(jobs){"
end_marker = "\n\n/* DROPDOWNS */"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("WARNING: markers not found, no changes made")
else:
    new_fn = r"""function rJ(jobs){
  const jl = document.getElementById('jl');
  if(!jobs.length){jl.innerHTML='<div class="empty">No active jobs</div>';return;}

  if(curStabFilter==='completed'){
    window.completedJobsCache = jobs;
    let rows=jobs.map(function(o){
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
}"""
    content = content[:start_idx] + new_fn + content[end_idx:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("rJ replaced with full-page Delivery Details workflow (modal removed)")
