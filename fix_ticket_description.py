import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "const r = await api('/api/v1/tickets','POST',{subject:sj,description:document.getElementById('tDt').value,priority:curTK==='technical'?'high':'normal',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});"

new = "const dtVal=(document.getElementById('tDt').value||'').trim();const r = await api('/api/v1/tickets','POST',{subject:sj,description:dtVal.length>=3?dtVal:sj,priority:curTK==='technical'?'high':'normal',category:curTK,raised_by:by,shop_id:curShop?curShop.id:null});"

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Ticket submission fixed - description now always meets 3-char minimum")
else:
    print("WARNING: anchor not unique - manual fix needed")
