import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- FIX 1: correct the download-all URL (missing /files prefix) ----
old_url = "API+'/api/v1/orders/'+orderId+'/download-all'"
new_url = "API+'/api/v1/files/orders/'+orderId+'/download-all'"
c1 = content.count(old_url)
print(f"download-all URL found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_url, new_url)
    print("URL fixed")
else:
    print("WARNING: URL anchor not unique/found")

# ---- FIX 2: add Order / In Progress / Completed filter buttons ----
old_tabs = """        <h2>Active Jobs</h2>
        <div class="ttabs">
          <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

new_tabs = """        <h2>Active Jobs</h2>
        <div class="ttabs" style="margin-bottom:8px">
          <button class="stab son" onclick="fs('all',this)">Order</button>
          <button class="stab" onclick="fs('in_progress',this)">Status</button>
          <button class="stab" onclick="fs('completed',this)">Completed</button>
        </div>
        <div class="ttabs">
          <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

c2 = content.count(old_tabs)
print(f"Tabs anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_tabs, new_tabs)
    print("Status filter buttons added")
else:
    print("WARNING: tabs anchor not unique/found")

# ---- FIX 3: add fs() filter function next to fj() ----
old_fn = "function fj(t,el){"
new_fn = """function fs(s,el){
  document.querySelectorAll('.stab').forEach(x=>x.classList.remove('son'));
  el.classList.add('son');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='completed'));return;}
  rJ(allOrds.filter(o=>o.status!=='completed'&&o.status!=='cancelled'));
}

function fj(t,el){"""

c3 = content.count(old_fn)
print(f"fj() anchor found {c3} time(s)")
if c3 == 1:
    content = content.replace(old_fn, new_fn)
    print("fs() function added")
else:
    print("WARNING: fj() anchor not unique/found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
