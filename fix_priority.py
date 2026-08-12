p = "static/specific_control.html"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old = "priority:curTK==='technical'?'high':'medium'"
new = "priority:curTK==='technical'?'high':'normal'"

if old in s:
    s = s.replace(old, new, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("Patched OK")
else:
    print("MATCH NOT FOUND")
