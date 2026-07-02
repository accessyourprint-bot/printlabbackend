import re
path = "static/full_control.html"
with open(path, encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"\(''\+([\w.]+)\+''\)")
fixed, n = pattern.subn(lambda m: "(\\'" + "'+" + m.group(1) + "+'" + "\\')", content)
print("Replaced", n, "occurrences")

with open(path, "w", encoding="utf-8") as f:
    f.write(fixed)

# verify
with open(path, encoding="utf-8") as f:
    check = f.read()
remaining = pattern.findall(check)
print("Remaining broken patterns:", remaining)
