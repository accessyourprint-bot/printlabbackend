import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    if(s==='all') actHead.innerText = 'Download';
    else if(s==='downloaded') actHead.innerText = 'Download';
    else if(s==='completed') actHead.innerText = 'Out for Delivery';
    else if(s==='out_for_delivery') actHead.innerText = 'Out for Delivery';"""

new = """    if(s==='all') actHead.innerText = 'Download';
    else if(s==='downloaded') actHead.innerText = 'Download';
    else if(s==='completed') actHead.innerText = 'Download';
    else if(s==='out_for_delivery') actHead.innerText = 'Out for Delivery';"""

c = content.count(old)
print(f"fs() header block found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Leftover 'completed' -> 'Out for Delivery' text corrected to 'Download'")
else:
    print("WARNING: block not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
