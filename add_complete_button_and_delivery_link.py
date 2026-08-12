import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Add "Out for Delivery" button next to B/W tabs group ----
old_header = """        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2>Active Jobs</h2>
          <div class="ttabs">
            <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

new_header = """        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2>Active Jobs</h2>
          <div style="display:flex;align-items:center;gap:10px">
            <button onclick="window.open('/static/delivery_tracking.html','_blank')" style="background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer">&#128666; Out for Delivery</button>
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

c1 = content.count(old_header)
print(f"Header anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_header, new_header)
    print("Out for Delivery button added")
else:
    print("WARNING: header anchor not found")

# ---- 2. Close the extra wrapping div we just opened (need matching closing tag before the outer </div> that closes .jhd's first row) ----
old_close = """            <button class="ttab" onclick="fj('project',this)">Project</button>
          </div>
        </div>
        <div class="ttabs stabs">"""

new_close = """            <button class="ttab" onclick="fj('project',this)">Project</button>
            </div>
          </div>
        </div>
        <div class="ttabs stabs">"""

c2 = content.count(old_close)
print(f"Closing div anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_close, new_close)
    print("Closing div fixed")
else:
    print("WARNING: closing div anchor not found")

# ---- 3. Track current stabs filter globally, update fs() ----
old_fs = """function fs(s,el){
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}"""

new_fs = """let curStabFilter = 'all';
function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}

async function markComplete(orderId){
  try{
    const resp = await fetch(API+'/api/v1/orders/'+orderId+'/status?new_status=ready',{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    if(!resp.ok){alert('Failed to mark complete');return;}
    await loadJ();
    document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
    const completedBtn = Array.from(document.querySelectorAll('.stabs .ttab')).find(b=>b.textContent.trim()==='Completed');
    if(completedBtn){completedBtn.classList.add('on');}
    curStabFilter='completed';
    rJ(allOrds.filter(o=>o.status==='ready'));
  }catch(e){alert('Failed to mark complete');}
}"""

c3 = content.count(old_fs)
print(f"fs() anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated + markComplete() added")
else:
    print("WARNING: fs() anchor not found")

# ---- 4. Update rJ() to swap Download -> Complete button when viewing Status tab ----
old_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>')+'</td>'"""

new_col = """+'<td style="padding:10px 12px;border-bottom:1px solid #eee">'+(curStabFilter==='downloaded'?'<button onclick="markComplete(&quot;'+o.id+'&quot;)" style="background:#16a34a;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#10003; Complete</button>':((o.files&&o.files.length)?'<button onclick="downloadAllZip(&quot;'+o.id+'&quot;,&quot;'+(o.order_number||o.id)+'&quot;)" style="background:#ea580c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:12px;cursor:pointer;font-weight:600">&#8595; Download</button>':'<span style="color:#999;font-size:12px">No files</span>'))+'</td>'"""

c4 = content.count(old_col)
print(f"rJ() column anchor found {c4} time(s)")
if c4 == 1:
    content = content.replace(old_col, new_col)
    print("rJ() updated to swap Download/Complete based on curStabFilter")
else:
    print("WARNING: rJ() column anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
