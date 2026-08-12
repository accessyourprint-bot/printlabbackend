import re
import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "'<div><span style=\"color:#999;font-weight:600\">Owner:</span> '+(o.owner_name||'\ufffd')+'</div>'+"

new = "'<div><span style=\"color:#999;font-weight:600\">Login ID:</span> '+(o.owner_email?o.owner_email.split('@')[0]:'\ufffd')+'</div>'+" + \
      "\n      '<div><span style=\"color:#999;font-weight:600\">Owner:</span> '+(o.owner_name||'\ufffd')+'</div>'+"

count = content.count(old)
print(f"Owner line found {count} time(s)")
if count == 1:
    content = content.replace(old, new)
    print("Login ID field inserted")
else:
    print("WARNING: anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
