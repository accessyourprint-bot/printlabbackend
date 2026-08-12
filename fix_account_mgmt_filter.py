import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "const users=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='customer'||!u.role);"
new = "const users=(Array.isArray(d)?d:(d?.data||[])).filter(u=>u.role==='user'||u.role==='customer');"

count = content.count(old)
print(f"Filter line found {count} time(s)")
if count == 1:
    content = content.replace(old, new)
    print("Filter fixed to match role='user'")
else:
    print("WARNING: anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
