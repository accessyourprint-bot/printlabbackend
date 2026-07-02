import re
path = "static/full_control.html"
with open(path, encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"\(''\+([\w.]+)\+''\)")
matches = list(pattern.finditer(content))
print("Found", len(matches), "occurrences")
for m in matches:
    print("-", m.group(0))
