import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = ">Download<"
c = content.count(old)
print(f"'>Download<' found {c} time(s)")

if c == 1:
    content = content.replace(old, ">Action<")
    print("Header updated to Action")
elif c == 0:
    print("WARNING: no exact match for '>Download<'")
else:
    print(f"WARNING: found {c} matches - need a more specific anchor, not auto-replacing")

if c == 1:
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
