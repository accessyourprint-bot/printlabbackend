import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Remove the standalone header button (superseded by the 4th tab) ----
old_header = """          <div style="display:flex;align-items:center;gap:10px">
            <button id="odBtn" style="display:none;background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer" onclick="showDelivery(this)">&#128666; Out for Delivery</button>
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

new_header = """          <div style="display:flex;align-items:center;gap:10px">
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

c1 = content.count(old_header)
print(f"Header anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_header, new_header)
    print("Old header button removed")
else:
    print("WARNING: header anchor not found")

# ---- 2. Add 4th tab next to Completed ----
old_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>"""

new_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
          <button class="ttab" onclick="fs('out_for_delivery',this)">Out for Delivery</button>
        </div>"""

c2 = content.count(old_stabs)
print(f"Stabs row anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_stabs, new_stabs)
    print("4th tab added")
else:
    print("WARNING: stabs anchor not found")

# ---- 3. Update fs() to handle the new tab, remove odBtn toggle logic ----
old_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  const odBtn = document.getElementById('odBtn');
  if(odBtn) odBtn.style.display = (s==='completed') ? 'inline-block' : 'none';
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}"""

new_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
  if(s==='out_for_delivery'){rJ(allOrds.filter(o=>o.status==='out_for_delivery'));return;}
}"""

c3 = content.count(old_fs)
print(f"fs() anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated for 4th tab, odBtn logic removed")
else:
    print("WARNING: fs() anchor not found")

# ---- 4. Update rJ() column: Out for Delivery tab shows a neutral status badge, not a button ----
old_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')))+'</td>'"""

new_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':(curStabFilter==='completed'?'<button onclick="markOutForDelivery(&quot;'+o.id+'&quot;)" style="background:#2563eb;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#128666; Out for Delivery</button>':(curStabFilter==='out_for_delivery'?'<span style="background:#eff6ff;color:#2563eb;font-weight:700;border-radius:20px;padding:4px 12px;font-size:.8rem">&#128666; En route</span>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>'))))+'</td>'"""

c4 = content.count(old_col)
print(f"rJ() column anchor found {c4} time(s)")
if c4 == 1:
    content = content.replace(old_col, new_col)
    print("rJ() updated with 4-way logic")
else:
    print("WARNING: rJ() column anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
