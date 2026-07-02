path = "static/full_control.html"
with open(path, encoding="utf-8") as f:
    content = f.read()
old = r'''onclick="delAgent(''+a.id+'')"'''
new = r'''onclick="delAgent(\''+a.id+'\')"'''
if old in content:
    content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed!")
else:
    print("Pattern not found")
