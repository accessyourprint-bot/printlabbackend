import io, re

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = """    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd" id="actHead">Download</th>'"""
new_line = """    +'<th style="padding:10px 12px;border-bottom:2px solid #ddd" id="actHead">'+(curStabFilter==='completed'||curStabFilter==='out_for_delivery'?'Out for Delivery':'Download')+'</th>'"""

c = content.count(old_line)
print(f"Header <th> literal found {c} time(s)")
if c == 1:
    content = content.replace(old_line, new_line)
    print("Header <th> now generates dynamic text based on curStabFilter")
else:
    print("WARNING: exact line not found, no changes made")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
