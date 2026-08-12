import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """function rJ(jobs){
  if(!jobs.length){document.getElementById('jl').innerHTML='<div class="empty">No active jobs</div>';return;}
  const MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  document.getElementById('jl').innerHTML=jobs.map(o=>{
    const dt=new Date(o.created_at);
    const ds=dt.getDate()+' '+MN[dt.getMonth()]+', '+dt.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'});
    return '<div class="ji"><div class="ji-top"><span class="ji-id">'+(o.order_number||o.id?.slice(0,12)||'&mdash;')+'</span><span class="ji-st '+stC(o.status)+'">'+stL(o.status)+'</span></div><div class="ji-name">'+(o.user_name||o.customer_name||'Customer')+'</div><div class="ji-phone">'+(o.user_phone||o.customer_phone||'')+'</div><div class="ji-bot">'+((o.files&&o.files.length)?o.files.map(function(f){return '<span class="ji-file" style="cursor:pointer;text-decoration:underline" onclick="event.stopPropagation();dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/"/g,'')+'&quot;)">&#8595; '+(f.original_filename||'document.pdf')+'</span>';}).join(''):'<span class="ji-file">&#8595; No file</span>')+'<span class="ji-copies">x'+(o.copies||1)+'</span><span class="ji-type">'+TL[gT(o)]+'</span><span class="ji-date">'+ds+'</span></div></div>';
  }).join('');
}"""

new = """function rJ(jobs){
  if(!jobs.length){document.getElementById('jl').innerHTML='<div class="empty">No active jobs</div>';return;}
  let rows=jobs.map(function(o){
    const docsHtml=(o.files&&o.files.length)?o.files.map(function(f){
      return '<div style="cursor:pointer;text-decoration:underline;color:#2563eb" onclick="event.stopPropagation();dlFile(&quot;'+f.id+'&quot;,&quot;'+(f.original_filename||'file').replace(/"/g,'')+'&quot;)">&#8595; '+(f.original_filename||'document.pdf')+'</div>';
    }).join(''):'<span style="color:#999">No file</span>';
    return '<tr>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_name||o.customer_name||'Customer')+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+docsHtml+'</td>'
      +'<td style="padding:10px 12px;border-bottom:1px solid #eee"><span class="ji-st '+stC(o.status)+'">'+stL(o.status)+'</span></td>'
      +'</tr>';
  }).join('');
  document.getElementById('jl').innerHTML='<table style="width:100%;border-collapse:collapse;font-size:13px">'
    +'<thead><tr style="background:#f8f8fa;text-align:left">'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Order ID</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Customer Name</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Phone Number</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Document</th>'
    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd">Status</th>'
    +'</tr></thead><tbody>'+rows+'</tbody></table>';
}"""

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Active Jobs converted to table format")
else:
    print("WARNING: anchor not unique - manual fix needed")
