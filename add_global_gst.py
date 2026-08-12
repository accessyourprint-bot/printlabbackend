import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert Global GST section below the feature toggle grid
old_grid = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
</div>"""

new_grid = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
<div style="margin-top:20px;padding-top:20px;border-top:1px solid #eee">
  <h4 style="margin:0 0 4px">Global GST</h4>
  <p style="color:#888;font-size:.8rem;margin:0 0 12px">This GST % applies automatically to every feature's price</p>
  <div style="display:flex;gap:10px;max-width:320px">
    <input type="text" inputmode="decimal" id="globalGstInput" placeholder="0" style="flex:1;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem">
    <button class="btn-sm btn-orange" onclick="saveGlobalGst()" style="padding:0 20px">Save</button>
  </div>
</div>
</div>"""

if old_grid not in content:
    print("GRID BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old_grid, new_grid, 1)

    # 2. Add loadGlobalGst / saveGlobalGst functions, hook into initApp
    old_init = """function initApp(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('appWrap').classList.remove('hidden');
  loadDashSummary();
}"""

    new_init = """function initApp(){
  document.getElementById('lw').classList.add('hidden');
  document.getElementById('appWrap').classList.remove('hidden');
  loadDashSummary();
  loadGlobalGst();
}
function loadGlobalGst(){
  const v=localStorage.getItem('pl_global_gst')||'0';
  const el=document.getElementById('globalGstInput');
  if(el) el.value=v;
}
function saveGlobalGst(){
  const v=parseFloat(document.getElementById('globalGstInput').value)||0;
  localStorage.setItem('pl_global_gst', String(v));
  alert('Global GST saved. It now applies to all feature prices.');
}"""

    if old_init not in content:
        print("INITAPP NOT FOUND - aborting (grid section already patched though)")
    else:
        content = content.replace(old_init, new_init, 1)

        # 3. Make fpGst auto-fill from global GST and become readonly in the modal
        old_open = """  document.getElementById('fpPrice').value='';
  document.getElementById('fpGst').value='';
  document.getElementById('fpTotal').value='';
  curFeaturePricing=null;"""

        new_open = """  document.getElementById('fpPrice').value='';
  document.getElementById('fpGst').value=localStorage.getItem('pl_global_gst')||'0';
  document.getElementById('fpGst').readOnly=true;
  document.getElementById('fpGst').style.background='#f7f7f7';
  document.getElementById('fpTotal').value='';
  curFeaturePricing=null;"""

        if old_open not in content:
            print("OPEN FUNCTION NOT FOUND - aborting (earlier sections already patched though)")
        else:
            content = content.replace(old_open, new_open, 1)
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("PATCHED SUCCESSFULLY")
