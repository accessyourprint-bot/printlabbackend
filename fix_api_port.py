path = "static/full_control.html"
with open(path, encoding="utf-8") as f:
    content = f.read()

old = "const API='http://127.0.0.1:8000';"
new = "const API='http://127.0.0.1:8001';"

if old in content:
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed! API now points to port 8001")
else:
    print("Pattern not found - check exact text")
