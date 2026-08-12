import re, io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace mock preview cards with a real iframe of the actual app
preview_pattern = re.compile(
    r'<div class="preview-box">.*?Preview updates as you type</p>\s*</div>',
    re.DOTALL
)
new_preview = ('<div class="preview-box" style="padding:0;overflow:hidden">\n'
    '<iframe id="livePreviewFrame" src="http://localhost:5173/?preview=1" '
    'style="width:100%;height:640px;border:none;display:block"></iframe>\n'
    '<p style="text-align:center;color:#aaa;font-size:.76rem;padding:8px 16px 14px">'
    'Live app \xe2\x80\x94 updates as you type</p>\n</div>').encode().decode('utf-8')

content, n1 = preview_pattern.subn(new_preview, content, count=1)
if n1 == 0:
    print("PREVIEW BLOCK NOT FOUND - aborting, no changes written")
else:
    # 2. Insert Feature Control panel after the appctrl-grid closes
    grid_pattern = re.compile(
        re.escape("Live app \u2014 updates as you type</p>") + r'(\s*</div>){3}',
        re.DOTALL
    )
    m = grid_pattern.search(content)
    if not m:
        print("GRID CLOSE MARKER NOT FOUND after preview replace - aborting")
    else:
        feature_panel = '''
<div class="form-panel" style="margin-top:20px">
<h3>&#128295; Feature Control</h3>
<div class="fg"><label>Shop</label>
<select id="fcShop" onchange="loadFeatureFlags()">
<option value="">Global (all shops)</option>
<option value="shop-001">Print Lab Koramangala</option>
</select>
</div>
<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:14px"></div>
</div>
'''
        content = content[:m.end()] + feature_panel + content[m.end():]

        # 3. Insert JS functions after doLogout definition
        js_anchor = "function doLogout(){localStorage.removeItem('pl_full');location.reload();}"
        new_js = js_anchor + '''
async function loadFeatureFlags(){
  const shopId=document.getElementById('fcShop').value;
  const url='/api/v1/features'+(shopId?('?shop_id='+shopId):'');
  const flags=await api(url);
  const list=document.getElementById('fcFeatureList');
  if(!Array.isArray(flags)){list.innerHTML='<p style="color:#c00">Failed to load features</p>';return;}
  list.innerHTML=flags.map(f=>
    '<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border:1px solid #eee;border-radius:8px">'+
    '<span style="font-size:.85rem;font-weight:600">'+f.label+'</span>'+
    '<input type="checkbox" style="width:18px;height:18px" '+(f.enabled?'checked':'')+' onchange="toggleFeatureFlag(\\''+f.feature_name+'\\', this.checked)">'+
    '</div>'
  ).join('');
}
async function toggleFeatureFlag(name, enabled){
  const shopId=document.getElementById('fcShop').value || null;
  const r=await api('/api/v1/features/toggle','POST',{feature_name:name, enabled:enabled, shop_id:shopId});
  if(!r || !r.data){alert('Failed to update feature');}
  loadFeatureFlags();
}
'''
        if js_anchor not in content:
            print("JS ANCHOR NOT FOUND - HTML changes written but JS not inserted")
        else:
            content = content.replace(js_anchor, new_js, 1)
            print("All changes applied successfully")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
