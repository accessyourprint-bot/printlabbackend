import io, re

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

if 'id="actHead"' not in content:
    pattern = re.compile(r'(<th[^>]*)>Download<')
    matches = pattern.findall(content)
    print(f"Header anchor found {len(matches)} time(s)")
    if len(matches) == 1:
        content = pattern.sub(r'\1 id="actHead">Download<', content, count=1)
        print("id=actHead added to header cell")
    else:
        print("WARNING: header anchor not found/ambiguous, skipping")
else:
    print("Header already has id=actHead, skipping tag step")

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
    else if(s==='downloaded') actHead.innerText = 'Download';
    else if(s==='completed') actHead.innerText = 'Out for Delivery';
    else if(s==='out_for_delivery') actHead.innerText = 'Out for Delivery';
  }
  if(s==='all'){rJ(allOrds);return;}
  if(s==='downloaded'){rJ(allOrds.filter(o=>o.is_downloaded===true));return;}
  if(s==='completed'){rJ(allOrds.filter(o=>o.status==='ready'));return;}
  if(s==='out_for_delivery'){rJ(allOrds.filter(o=>o.status==='out_for_delivery'));return;}
}"""

c2 = content.count(old_fs)
print(f"fs anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_fs, new_fs)
    print("fs updated")
elif 'actHead.innerText' in content:
    print("fs already updated, skipping")
else:
    print("WARNING: fs anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
