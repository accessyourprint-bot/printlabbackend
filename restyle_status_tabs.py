import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- Replace stab/son classes with ttab/on classes (reuse existing style) ----
old_buttons = """        <div class="ttabs" style="margin-bottom:8px">
          <button class="stab son" onclick="fs('all',this)">Order</button>
          <button class="stab" onclick="fs('in_progress',this)">Status</button>
          <button class="stab" onclick="fs('completed',this)">Completed</button>
        </div>"""

new_buttons = """        <div class="ttabs stabs" style="margin-bottom:8px">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('in_progress',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>"""

c1 = content.count(old_buttons)
print(f"Old status buttons found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_buttons, new_buttons)
    print("Buttons updated to use ttab class")
else:
    print("WARNING: anchor not found - may already be edited")

# ---- Fix fs() to target the right scope (only toggle within .stabs group, not B/W tabs) ----
old_fs = """function fs(s,el){
  document.querySelectorAll('.stab').forEach(x=>x.classList.remove('son'));
  el.classList.add('son');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='completed'));return;}
  rJ(allOrds.filter(o=>o.status!=='completed'&&o.status!=='cancelled'));
}"""

new_fs = """function fs(s,el){
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='completed'));return;}
  rJ(allOrds.filter(o=>o.status!=='completed'&&o.status!=='cancelled'));
}"""

c2 = content.count(old_fs)
print(f"fs() function found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated to use .on class scoped to .stabs")
else:
    print("WARNING: fs() anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
