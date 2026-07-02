import re
html = open("static/full_control.html", encoding="utf-8").read()
print("File size:", len(html))

print("--- id=\"pg-...\" matches ---")
for m in re.finditer(r'id="pg-[a-zA-Z0-9_-]+"', html):
    print(m.group())

print("--- openPage( calls ---")
for m in re.finditer(r"openPage\([^)]*\)", html):
    print(m.group())

print("--- function names defined ---")
for m in re.finditer(r"function\s+(\w+)\s*\(", html):
    print(m.group(1))

print("--- snippet around 'appcontrol' ---")
idx = html.lower().find("appcontrol")
if idx != -1:
    print(repr(html[max(0, idx - 100): idx + 200]))
else:
    print("no occurrence of 'appcontrol' found anywhere")
