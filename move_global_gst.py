import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the Global GST block from App Control
old_block = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
<div style="margin-top:20px;padding-top:20px;border-top:1px solid #eee">
  <h4 style="margin:0 0 4px">Global GST</h4>
  <p style="color:#888;font-size:.8rem;margin:0 0 12px">This GST % applies automatically to every feature's price</p>
  <div style="display:flex;gap:10px;max-width:320px">
    <input type="text" inputmode="decimal" id="globalGstInput" placeholder="0" style="flex:1;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem">
    <button class="btn-sm btn-orange" onclick="saveGlobalGst()" style="padding:0 20px">Save</button>
  </div>
</div>
</div>"""

new_block = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
</div>"""

if old_block not in content:
    print("OLD GLOBAL GST BLOCK NOT FOUND IN APP CONTROL - aborting")
else:
    content = content.replace(old_block, new_block, 1)

    # 2. Insert it after Save Appearance button instead
    old_save_btn = """<button class="btn-full" onclick="saveAppSettings()">&#128190; Save Appearance</button>
</div>"""

    new_save_btn = """<button class="btn-full" onclick="saveAppSettings()">&#128190; Save Appearance</button>
<div style="margin-top:20px;padding-top:20px;border-top:1px solid #eee">
  <h4 style="margin:0 0 4px">Global GST</h4>
  <p style="color:#888;font-size:.8rem;margin:0 0 12px">This GST % applies automatically to every feature's price</p>
  <div style="display:flex;gap:10px">
    <input type="text" inputmode="decimal" id="globalGstInput" placeholder="0" style="flex:1;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem">
    <button class="btn-sm btn-orange" onclick="saveGlobalGst()" style="padding:0 20px">Save</button>
  </div>
</div>
</div>"""

    if old_save_btn not in content:
        print("SAVE APPEARANCE BUTTON NOT FOUND - aborting (removal from App Control already done though)")
    else:
        content = content.replace(old_save_btn, new_save_btn, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
