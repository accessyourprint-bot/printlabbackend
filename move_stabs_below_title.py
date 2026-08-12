import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """      <div class="jhd">
        <h2>Active Jobs</h2>
        <div class="ttabs stabs" style="margin-bottom:8px">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('in_progress',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>
        <div class="ttabs">
          <button class="ttab on" onclick="fj('bw',this)">B/W</button>
          <button class="ttab" onclick="fj('colour',this)">Colour</button>
          <button class="ttab" onclick="fj('photo',this)">Photo</button>
          <button class="ttab" onclick="fj('tshirt',this)">T-Shirt</button>
          <button class="ttab" onclick="fj('project',this)">Project</button>
        </div>
      </div>"""

new = """      <div class="jhd" style="flex-direction:column;align-items:stretch;gap:10px">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2>Active Jobs</h2>
          <div class="ttabs">
            <button class="ttab on" onclick="fj('bw',this)">B/W</button>
            <button class="ttab" onclick="fj('colour',this)">Colour</button>
            <button class="ttab" onclick="fj('photo',this)">Photo</button>
            <button class="ttab" onclick="fj('tshirt',this)">T-Shirt</button>
            <button class="ttab" onclick="fj('project',this)">Project</button>
          </div>
        </div>
        <div class="ttabs stabs">
          <button class="ttab son" onclick="fs('all',this)">Order</button>
          <button class="ttab" onclick="fs('in_progress',this)">Status</button>
          <button class="ttab" onclick="fs('completed',this)">Completed</button>
        </div>
      </div>"""

c = content.count(old)
print(f"Header block found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("Header restructured - stabs now on own row below title")
else:
    print("WARNING: anchor not found exactly - paste this output back")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
