import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove buttons from the preview panel
old_preview = """<div><div class="form-panel"><h3>&#128248; Live Preview</h3>
<div style="display:flex;gap:8px;margin-bottom:10px">
<button class="btn-sm" id="pvBtnLogin" onclick="setPreviewView('login')" style="flex:1;background:#1a223e;color:#fff;border:none">Login</button>
<button class="btn-sm" id="pvBtnDash" onclick="setPreviewView('dashboard')" style="flex:1;background:#eee;color:#1a223e;border:none">Dashboard</button>
</div>
<div class="preview-box" style="padding:0;overflow:hidden">"""

new_preview = """<div><div class="form-panel"><h3>&#128248; Live Preview</h3>
<div class="preview-box" style="padding:0;overflow:hidden">"""

if old_preview not in content:
    print("PREVIEW BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_preview, new_preview, 1)

    # 2. Insert buttons right after Global GST block (before its closing </div></div>)
    old_gst_end = """    <button class="btn-sm btn-orange" onclick="saveGlobalGst()" style="padding:0 20px">Save</button>
  </div>
</div>
</div>"""

    new_gst_end = """    <button class="btn-sm btn-orange" onclick="saveGlobalGst()" style="padding:0 20px">Save</button>
  </div>
  <div style="display:flex;gap:8px;margin-top:16px">
    <button class="btn-sm" id="pvBtnLogin" onclick="setPreviewView('login')" style="flex:1;background:#1a223e;color:#fff;border:none">Login</button>
    <button class="btn-sm" id="pvBtnDash" onclick="setPreviewView('dashboard')" style="flex:1;background:#eee;color:#1a223e;border:none">Dashboard</button>
  </div>
</div>
</div>"""

    if old_gst_end not in content:
        print("GST END BLOCK NOT FOUND - aborting (preview already patched though)")
    else:
        content = content.replace(old_gst_end, new_gst_end, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
