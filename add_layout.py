import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_wrap = """  <div style="background:#fff;border-radius:14px;max-width:420px;width:92%;padding:0">"""
new_wrap = """  <div style="background:#fff;border-radius:14px;max-width:560px;width:94%;padding:0">"""

if old_wrap not in content:
    print("WRAPPER NOT FOUND - aborting")
else:
    content = content.replace(old_wrap, new_wrap, 1)

    old_fields = """    <div style="padding:24px">
      <div class="fg"><label>Price (&#8377;)</label><input type="text" inputmode="decimal" id="fpPrice" placeholder="0.00" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <div class="fg" style="margin-top:12px"><label>GST (%)</label><input type="text" inputmode="decimal" id="fpGst" placeholder="0" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <div class="fg" style="margin-top:12px"><label>Total Cost (&#8377;)</label><input type="text" id="fpTotal" readonly style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem;background:#f7f7f7;font-weight:700"></div>
      <button class="btn-sm btn-orange" onclick="saveFeaturePrice()" style="width:100%;margin-top:16px;padding:12px">Save Price</button>
    </div>"""

    new_fields = """    <div style="padding:24px">
      <div style="display:flex;gap:12px">
        <div class="fg" style="flex:1;min-width:0"><label>Price (&#8377;)</label><input type="text" inputmode="decimal" id="fpPrice" placeholder="0.00" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 10px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.85rem;box-sizing:border-box"></div>
        <div class="fg" style="flex:1;min-width:0"><label>GST (%)</label><input type="text" inputmode="decimal" id="fpGst" placeholder="0" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 10px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.85rem;box-sizing:border-box"></div>
        <div class="fg" style="flex:1;min-width:0"><label>Total (&#8377;)</label><input type="text" id="fpTotal" readonly style="width:100%;padding:12px 10px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.85rem;background:#f7f7f7;font-weight:700;box-sizing:border-box"></div>
      </div>
      <button class="btn-sm btn-orange" onclick="saveFeaturePrice()" style="width:100%;margin-top:16px;padding:12px">Save Price</button>
    </div>"""

    if old_fields not in content:
        print("FIELDS BLOCK NOT FOUND - aborting (wrapper already patched though)")
    else:
        content = content.replace(old_fields, new_fields, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
