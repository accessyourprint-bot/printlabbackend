import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove topbar button
old_btn = """      <button class="tbtn" onclick="openDT()">&#128101; <span>Delivery Team</span></button>
      <button class="tbtn" onclick="openPJ()">&#128193; <span>Projects</span></button>
      <button class="tbtn" onclick="openPS()">&#128202; <span>Performance Status</span></button>"""
new_btn = """      <button class="tbtn" onclick="openDT()">&#128101; <span>Delivery Team</span></button>
      <button class="tbtn" onclick="openPS()">&#128202; <span>Performance Status</span></button>"""

if old_btn in content:
    content = content.replace(old_btn, new_btn, 1)
    print("BUTTON REMOVED")
else:
    print("BUTTON MARKER NOT FOUND")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
