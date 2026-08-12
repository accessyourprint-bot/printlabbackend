import io, re

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r'(<th[^>]*)>Download<')
matches = pattern.findall(content)
print(f"Header <th>Download</th> anchor found {len(matches)} time(s)")
if len(matches) == 1:
    content = pattern.sub(r'\1 id="actHead">Download<', content, count=1)
    print("id=actHead added to header cell")
else:
    print("WARNING: header anchor not found/ambiguous, skipping")

old_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
  if(s==='out_for_delivery'){rJ(allOrds.filter(o=>o.status==='out_for_delivery'));return;}
}"""

new_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  const actHead = document.getElementById('actHead');
  if(actHead){
    if(s==='all') actHead.innerText = 'Download';
    else if(s==='downloaded') actHead.innerText = 'Complete';
    else if(s==='completed') actHead.innerText = 'Out for Delivery';
    else if(s==='out_for_delivery') actHead.innerText = 'Out for Delivery';
  }
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
  if(s==='out_for_delivery'){rJ(allOrds.filter(o=>o.status==='out_for_delivery'));return;}
}"""

c2 = content.count(old_fs)
print(f"fs() anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated to sync header text per tab")
else:
    print("WARNING: fs() anchor not found")

old_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>':(curStabFilter==='out_for_delivery'?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; En route</span>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>'))))+'</td>'"""

new_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Completed</button>':(curStabFilter==='out_for_delivery'?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; En route</span>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>'))))+'</td>'"""

c3 = content.count(old_col)
print(f"rJ() column anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_col, new_col)
    print("Row button text updated to 'Completed' on the Completed tab")
else:
    print("WARNING: rJ() column anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
