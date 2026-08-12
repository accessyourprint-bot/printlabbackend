import re, io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix any mangled dash text from the previous run, normalize to clean text
content = re.sub(
    r'Live app .{1,6} updates as you type',
    'Live app - updates as you type',
    content
)

# Find the triple-close after the preview box paragraph, insert Feature Control panel there
anchor_pattern = re.compile(
    r'(Live app - updates as you type</p>\s*</div>\s*</div>\s*</div>\s*</div>)',
    re.DOTALL
)
m = anchor_pattern.search(content)
if not m:
    print("ANCHOR NOT FOUND - no changes written")
else:
    already_has_panel = 'id="fcFeatureList"' in content
    if already_has_panel:
        print("Feature panel already present - skipping panel insert")
    else:
        feature_panel = '''
<div class="form-panel" style="margin-top:20px">
<h3>Feature Control</h3>
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
        print("Feature panel inserted")

    js_anchor = "function doLogout(){localStorage.removeItem('pl_full');location.reload();}"
    if 'async function loadFeatureFlags' in content:
        print("JS already present - skipping")
    elif js_anchor not in content:
        print("JS ANCHOR NOT FOUND - panel HTML written but JS not inserted")
    else:
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
        content = content.replace(js_anchor, new_js, 1)
        print("JS inserted")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
