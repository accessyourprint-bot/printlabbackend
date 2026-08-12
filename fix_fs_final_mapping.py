import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_fs = """function fs(s,el){
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='completed'));return;}
  rJ(allOrds.filter(o=>o.status!=='completed'&&o.status!=='cancelled'));
}"""

new_fs = """function fs(s,el){
  document.querySelectorAll('.stabs .ttab').forEach(x=>x.classList.remove('son','on'));
  el.classList.add('on');
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
}"""

c1 = content.count(old_fs)
print(f"fs() anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs() updated: Status=is_downloaded, Completed=status ready")
else:
    print("WARNING: fs() anchor not found")

# Also fix the button call so Status passes 'downloaded' instead of 'in_progress'
old_btn = """<button class="ttab" onclick="fs('in_progress',this)">Status</button>"""
new_btn = """<button class="ttab" onclick="fs('downloaded',this)">Status</button>"""

c2 = content.count(old_btn)
print(f"Status button anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_btn, new_btn)
    print("Status button now calls fs('downloaded', this)")
else:
    print("WARNING: button anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
