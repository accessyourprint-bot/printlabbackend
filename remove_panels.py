import io, re

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<div class=\"panel\" style=\"margin-bottom:16px\">\n<div class=\"panel-hd\">&#9881; System Controls</div>"
end_marker = "<div class=\"appctrl-grid\">"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1:
    print("START MARKER NOT FOUND")
elif end_idx == -1:
    print("END MARKER NOT FOUND")
elif end_idx < start_idx:
    print("END BEFORE START - ABORT")
else:
    content = content[:start_idx] + content[end_idx:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Removed panels successfully")
