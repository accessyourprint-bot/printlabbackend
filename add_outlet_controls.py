import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

html_marker = '<div class="appctrl-grid">'
new_panel = """<div class="panel" style="margin-bottom:16px">
<div class="panel-hd">&#127970; Outlet-level Controls</div>
<div style="padding:20px">
<div class="fg"><label>Select Outlet</label><select id="outletSel" onchange="loadOutletFeats()" style="width:100%;padding:10px;border:1.5px solid #e0e0e0;border-radius:10px"><option value="">Loading outlets...</option></select></div>
<div id="outletFeats" style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:14px"></div>
</div>
</div>
"""

if html_marker not in content:
    print("HTML MARKER NOT FOUND")
else:
    content = content.replace(html_marker, new_panel + html_marker, 1)

    js_marker = "async function toggleFeat(name,val){await api('/api/v1/features/toggle','POST',{feature_name:name,enabled:val,scope:'global'});loadFeatToggles();}"
    new_js = js_marker + """
async function loadOutletShops(){
  const shops = await api('/api/v1/shops');
  const sel = document.getElementById('outletSel');
  if(!Array.isArray(shops) || !shops.length){ sel.innerHTML='<option value="">No outlets found</option>'; return; }
  sel.innerHTML = shops.map(function(s){return '<option value="'+s.id+'">'+s.name+'</option>';}).join('');
  loadOutletFeats();
}
async function loadOutletFeats(){
  const shopId = document.getElementById('outletSel').value;
  const box = document.getElementById('outletFeats');
  if(!shopId){ box.innerHTML=''; return; }
  box.innerHTML = '<div class="loading">Loading...</div>';
  const d = await api('/api/v1/features?shop_id='+shopId);
  if(!Array.isArray(d)){ box.innerHTML='<div class="empty">Error</div>'; return; }
  const wanted = ['black_white_print','color_print'];
  const filtered = d.filter(function(f){return wanted.indexOf(f.feature_name)!==-1;});
  var html='';
  for(var i=0;i<filtered.length;i++){
    var f=filtered[i];
    html+='<div style="background:#fff;border:1.5px solid #ebebee;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center">'+
      '<div>'+
      '<div style="font-weight:700;font-size:.88rem">'+f.label+'</div>'+
      '<div style="font-size:.75rem;color:#999;margin-top:2px">'+f.feature_name+'</div>'+
      '<div style="font-size:.75rem;margin-top:3px;color:'+(f.enabled?'#22b573':'#e74c3c')+';font-weight:600">'+(f.enabled?'ON':'OFF')+'</div>'+
      '</div>'+
      '<label style="position:relative;width:46px;height:24px;flex-shrink:0;cursor:pointer">'+
      '<input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleOutletFeat(&quot;'+f.feature_name+'&quot;,this.checked)" style="opacity:0;width:0;height:0">'+
      '<span style="position:absolute;cursor:pointer;inset:0;background:'+(f.enabled?'#22b573':'#ccc')+';border-radius:24px;transition:.2s;display:block">'+
      '<span style="position:absolute;width:18px;height:18px;left:'+(f.enabled?'25px':'3px')+';bottom:3px;background:#fff;border-radius:50%;transition:.2s;display:block"></span>'+
      '</span></label></div>';
  }
  box.innerHTML = html || '<div class="empty">No matching flags for this outlet</div>';
}
async function toggleOutletFeat(name,val){
  const shopId = document.getElementById('outletSel').value;
  await api('/api/v1/features/toggle','POST',{feature_name:name,enabled:val,shop_id:shopId});
  loadOutletFeats();
}
"""
    if js_marker not in content:
        print("JS MARKER NOT FOUND")
    else:
        content = content.replace(js_marker, new_js, 1)

        lac_marker = "function loadAppControl(){updatePreview();loadSysToggles();loadFeatToggles();}"
        lac_new = "function loadAppControl(){updatePreview();loadSysToggles();loadFeatToggles();loadOutletShops();}"
        if lac_marker not in content:
            print("LOADAPPCONTROL MARKER NOT FOUND")
        else:
            content = content.replace(lac_marker, lac_new, 1)
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("All patches applied successfully")
