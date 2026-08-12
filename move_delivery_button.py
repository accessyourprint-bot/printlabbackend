import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Remove the button from the header (next to B/W tabs) ----
old_header = """        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2>Active Jobs</h2>
          <div style="display:flex;align-items:center;gap:10px">
            <button onclick="window.open('/static/delivery_tracking.html','_blank')" style="background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer">&#128666; Out for Delivery</button>
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

new_header = """        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2>Active Jobs</h2>
          <div style="display:flex;align-items:center;gap:10px">
            <div class="ttabs">
              <button class="ttab on" onclick="fj('bw',this)">B/W</button>"""

c1 = content.count(old_header)
print(f"Header anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_header, new_header)
    print("Button removed from header")
else:
    print("WARNING: header anchor not found")

# ---- 2. Add it into the .stabs row, right after Completed ----
old_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>"""

new_stabs = """        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('downloaded',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
          <button onclick="window.open('/static/delivery_tracking.html','_blank')" style="margin-left:auto;background:#1a1a1a;color:#fff;border:none;border-radius:20px;padding:7px 16px;font-size:.82rem;font-weight:600;cursor:pointer">&#128666; Out for Delivery</button>
        </div>"""

c2 = content.count(old_stabs)
print(f"Stabs row anchor found {c2} time(s)")
if c2 == 1:
    content = content.replace(old_stabs, new_stabs)
    print("Button added to stabs row")
else:
    print("WARNING: stabs anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
