import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: hide tByField for stock tickets too (same as technical) ---
old = """  if(type==='technical'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.add('hidden');
    document.getElementById('tSjSelectField').classList.remove('hidden');
  }else{
    document.getElementById('tByField').classList.remove('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }"""

new = """  if(type==='technical'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.add('hidden');
    document.getElementById('tSjSelectField').classList.remove('hidden');
  }else if(type==='stock'){
    document.getElementById('tByField').classList.add('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }else{
    document.getElementById('tByField').classList.remove('hidden');
    document.getElementById('tSjTextField').classList.remove('hidden');
    document.getElementById('tSjSelectField').classList.add('hidden');
  }"""

c1 = content.count(old)
print(f"openTK block found {c1} time(s)")
if c1 == 1:
    content = content.replace(old, new)
    print("Stock tickets now hide Raised By field")
else:
    print("WARNING: openTK block not found exactly once, aborting")
    exit()

# --- Part 2: auto-fill 'by' with curShop.name for stock tickets, and skip the by-required check for stock ---
old2 = """  const by=isTech?'N/A':document.getElementById('tBy').value;
  const sj=isTech?document.getElementById('tSjSelect').value:document.getElementById('tSj').value;
  const dt=(document.getElementById('tDt').value||'').trim();
  if(isTech){ if(!dt)return alert('Please explain the issue in Details'); }
  else if(!by||!sj)return alert('Fill Raised By and Subject');"""

new2 = """  const isStock=curTK==='stock';
  const by=isTech?'N/A':(isStock?(curShop?curShop.name:'Outlet'):document.getElementById('tBy').value);
  const sj=isTech?document.getElementById('tSjSelect').value:document.getElementById('tSj').value;
  const dt=(document.getElementById('tDt').value||'').trim();
  if(isTech){ if(!dt)return alert('Please explain the issue in Details'); }
  else if(isStock){ if(!sj)return alert('Fill Subject'); }
  else if(!by||!sj)return alert('Fill Raised By and Subject');"""

c2 = content.count(old2)
print(f"subTK block found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
    print("Stock tickets now auto-fill Raised By from outlet name")
else:
    print("WARNING: subTK block not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
