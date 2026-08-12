import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Part 1: add a new element for the bigger Outlet ID badge in the modal header ---
old1 = '<div><h3 id="tkT">Customer Ticket Raise</h3><p id="tkS"></p></div>'
new1 = '<div><h3 id="tkT">Customer Ticket Raise</h3><p id="tkS"></p><p id="tkOid" style="font-size:.95rem;font-weight:700;color:#3b5bfd;margin-top:4px"></p></div>'

c1 = content.count(old1)
print(f"Header block found {c1} time(s)")
if c1 == 1:
    content = content.replace(old1, new1)
else:
    print("WARNING: header anchor not found exactly once, aborting")
    exit()

# --- Part 2: remove Outlet ID from the small subtitle, put it in the new bigger line instead ---
old2 = "  document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'')+(curShop&&curShop.owner_email?' \\u2022 Outlet ID: '+curShop.owner_email.split('@')[0]:'');"
new2 = """  document.getElementById('tkS').textContent=m.s+(curShop?' for '+curShop.name:'');
  document.getElementById('tkOid').textContent=(curShop&&curShop.owner_email)?('Outlet ID: '+curShop.owner_email.split('@')[0]):'';"""

c2 = content.count(old2)
print(f"Subtitle line found {c2} time(s)")
if c2 == 1:
    content = content.replace(old2, new2)
    print("Outlet ID moved to its own bigger line")
else:
    print("WARNING: subtitle anchor not found exactly once, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
