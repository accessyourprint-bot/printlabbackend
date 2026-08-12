import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """  overlay.innerHTML=
    '<div style="background:#fff;border-radius:12px;padding:24px;width:340px;max-width:90vw">'+
      '<h3 style="margin:0 0 16px">Reset Outlet Password</h3>'+"""

new = """  const _o = (typeof allOutlets!=='undefined' ? allOutlets.find(x=>x.id===id) : null);
  const _label = _o ? (_o.name||'Outlet')+' &bull; Login ID: '+(_o.owner_email||id) : ('Outlet ID: '+id);
  overlay.innerHTML=
    '<div style="background:#fff;border-radius:12px;padding:24px;width:340px;max-width:90vw">'+
      '<h3 style="margin:0 0 4px">Reset Outlet Password</h3>'+
      '<p style="margin:0 0 16px;color:#888;font-size:.78rem">'+_label+'</p>'+"""

if old not in content:
    print("MARKER NOT FOUND - aborting")
else:
    content = content.replace(old, new, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("PATCHED SUCCESSFULLY")
