import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Remove the button from the .stabs row ----
old_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
          <button class="ttab" style="margin-left:auto" onclick="showDelivery(this)">&#128666; Out for Delivery</button>
        </div>"""

new_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>"""

c1 = content.count(old_stabs)
print(f"Stabs row anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_stabs, new_stabs)
    print("Button removed from stabs row")
else:
    print("WARNING: stabs anchor not found")

# ---- 2. Add it (hidden by default) to the top-right of the header, next to the B/W tabs group ----
old_header = """          <div style="display:flex;align-items:center;gap:10px">
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

new_header = """          <div style="display:flex;align-items:center;gap:10px">
            <button id="odBtn" style="display:none;background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer" onclick="showDelivery(this)">&#128666; Out for Delivery</button>
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

c2 = content.count(old_header)
print(f"Header anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_header, new_header)
    print("Hidden Out for Delivery button added to header")
else:
    print("WARNING: header anchor not found")

# ---- 3. Update fs() to show/hide #odBtn based on selected tab ----
old_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}"""

new_fs = """function fs(s,el){
  curStabFilter = s;
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  const odBtn = document.getElementById('odBtn');
  if(odBtn) odBtn.style.display = (s==='completed') ? 'inline-block' : 'none';
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}"""

c3 = content.count(old_fs)
print(f"fs() anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated to toggle odBtn visibility")
else:
    print("WARNING: fs() anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
