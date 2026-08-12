import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    return '<tr>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c\">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+(o.user_name||o.customer_name||'Customer')+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+docsHtml+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\"><span class=\"ji-st '+stC(o.status)+'\">'+stL(o.status)+'</span></td>'
      +'</tr>';"""

new = """    return '<tr>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee;font-weight:700;color:#ea580c\">'+(o.order_number||(o.id?o.id.slice(0,12):'&mdash;'))+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+(o.user_name||o.customer_name||'Customer')+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+(o.user_phone||o.customer_phone||'&mdash;')+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+docsHtml+'</td>'
      +'<td style=\"padding:10px 12px;border-bottom:1px solid #eee\">'+((o.files&&o.files.length)?'<button onclick=\"downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)\" style=\"background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600\">&#8595; Download</button>':'<span style=\"color:#999;font-size:12px\">No files</span>')+'</td>'
      +'</tr>';"""

c = content.count(old)
print(f"Row anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Status column replaced with Download button")
else:
    print("WARNING: row anchor not unique")

old_header = """    +'<th style=\"padding:10px 12px;border-bottom:2px solid #ddd\">Document</th>'
    +'<th style=\"padding:10px 12px;border-bottom:2px solid #ddd\">Status</th>'"""

new_header = """    +'<th style=\"padding:10px 12px;border-bottom:2px solid #ddd\">Document</th>'
    +'<th style=\"padding:10px 12px;border-bottom:2px solid #ddd\">Download</th>'"""

c2 = content.count(old_header)
print(f"Header anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_header, new_header)
    print("Header updated")
else:
    print("WARNING: header anchor not unique")

# Add the downloadAllZip helper function near dlFile
anchor2 = "function toggleSD(){"
new_func = """async function downloadAllZip(orderId, orderNumber){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/download-all', {headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to download files');return;}
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = orderNumber+'_documents.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }catch(e){alert('Failed to download files');}
}

function toggleSD(){"""

c3 = content.count(anchor2)
print(f"toggleSD anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(anchor2, new_func)
    print("downloadAllZip function added")
else:
    print("WARNING: toggleSD anchor not unique")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
