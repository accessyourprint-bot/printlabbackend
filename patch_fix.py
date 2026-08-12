import re

# 1. Add special_instructions to OrderOut schema
p1 = "app/schemas/schemas.py"
with open(p1, "r", encoding="utf-8") as f:
    s1 = f.read()
old1 = "    updated_at: Optional[datetime]\n\n    class Config:\n        from_attributes = True"
new1 = "    updated_at: Optional[datetime]\n    special_instructions: Optional[str] = None\n\n    class Config:\n        from_attributes = True"
if old1 in s1:
    s1 = s1.replace(old1, new1, 1)
    with open(p1, "w", encoding="utf-8") as f:
        f.write(s1)
    print("schemas.py: patched OK")
else:
    print("schemas.py: MATCH NOT FOUND -- no changes made, check manually")

# 2. Rewrite gT() and fj() in specific_control.html
p2 = "static/specific_control.html"
with open(p2, "r", encoding="utf-8") as f:
    s2 = f.read()

old_gT = """function gT(o){
  const s=JSON.stringify(o).toLowerCase();
  if(s.includes('colour')||s.includes('color'))return'Colour';
  if(s.includes('photo'))return'Photo';
  if(s.includes('tshirt')||s.includes('t-shirt'))return'Tshirt';
  if(s.includes('project'))return'Project';
  return'Bw';
}"""

new_gT = """function gT(o){
  const si=(o.special_instructions||'').toLowerCase();
  if(si.includes('bw_print'))return'Bw';
  if(si.includes('colour_print'))return'Colour';
  if(si.includes('photo_print'))return'Photo';
  if(si.includes('tshirt_print'))return'Tshirt';
  return'Bw';
}"""

old_fj = """function fj(t,el){
  document.querySelectorAll('.ttab').forEach(x=>x.classList.remove('on'));
  el.classList.add('on');
  if(t==='all'){rJ(allOrds);return;}
  const m={bw:'black_white',colour:'colour',photo:'photo',tshirt:'tshirt',project:'project'};
  rJ(allOrds.filter(o=>JSON.stringify(o).toLowerCase().includes(m[t]||t)));
}"""

new_fj = """function fj(t,el){
  document.querySelectorAll('.ttab').forEach(x=>x.classList.remove('on'));
  el.classList.add('on');
  if(t==='all'){rJ(allOrds);return;}
  const tabToType={bw:'Bw',colour:'Colour',photo:'Photo',tshirt:'Tshirt'};
  rJ(allOrds.filter(o=>gT(o)===tabToType[t]));
}"""

changed = False
if old_gT in s2:
    s2 = s2.replace(old_gT, new_gT, 1)
    changed = True
    print("specific_control.html: gT() patched OK")
else:
    print("specific_control.html: gT() MATCH NOT FOUND -- no changes made, check manually")

if old_fj in s2:
    s2 = s2.replace(old_fj, new_fj, 1)
    changed = True
    print("specific_control.html: fj() patched OK")
else:
    print("specific_control.html: fj() MATCH NOT FOUND -- no changes made, check manually")

if changed:
    with open(p2, "w", encoding="utf-8") as f:
        f.write(s2)