import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_modal = """<div id="fpMo" class="mo hidden">
  <div class="mb">
    <div class="mh">
      <div><h3 id="fpTitle">Feature Price</h3><p>Set the price for this feature.</p></div>
      <button class="mx" onclick="cMo('fpMo')">&#10005;</button>
    </div>
    <div class="mbody">
      <div class="fg"><label>Price (&#8377; per page/item)</label><input type="number" id="fpPrice" step="0.01" min="0" placeholder="0.00" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
    </div>
    <div class="mfoot"><button class="bsb" onclick="saveFeaturePrice()" style="width:100%">Save Price</button></div>
  </div>
</div>"""

new_modal = """<div id="fpMo" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999;align-items:center;justify-content:center">
  <div style="background:#fff;border-radius:14px;max-width:420px;width:92%;padding:0">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:20px 24px;border-bottom:1px solid #eee">
      <div><h3 id="fpTitle" style="margin:0">Feature Price</h3><p style="margin:4px 0 0;color:#888;font-size:.82rem">Set the price for this feature.</p></div>
      <button onclick="document.getElementById('fpMo').style.display='none'" style="background:none;border:none;font-size:1.3rem;cursor:pointer">&#10005;</button>
    </div>
    <div style="padding:24px">
      <div class="fg"><label>Price (&#8377; per page/item)</label><input type="number" id="fpPrice" step="0.01" min="0" placeholder="0.00" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <button class="btn-sm btn-orange" onclick="saveFeaturePrice()" style="width:100%;margin-top:16px;padding:12px">Save Price</button>
    </div>
  </div>
</div>"""

old_open = "async function openFeaturePrice(featureName,label){\n  oMo('fpMo');"
new_open = "async function openFeaturePrice(featureName,label){\n  document.getElementById('fpMo').style.display='flex';"

old_close = "    cMo('fpMo');\n    alert('Price saved');"
new_close = "    document.getElementById('fpMo').style.display='none';\n    alert('Price saved');"

ok = True
if old_modal not in content:
    print("MODAL BLOCK NOT FOUND"); ok = False
if old_open not in content:
    print("OPEN CALL NOT FOUND"); ok = False
if old_close not in content:
    print("CLOSE CALL NOT FOUND"); ok = False

if ok:
    content = content.replace(old_modal, new_modal, 1)
    content = content.replace(old_open, new_open, 1)
    content = content.replace(old_close, new_close, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED SUCCESSFULLY")
