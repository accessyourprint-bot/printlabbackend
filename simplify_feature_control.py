import re, io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the Feature Control panel HTML - remove shop dropdown, better styling
old_panel_pattern = re.compile(
    r'<div class="form-panel" style="margin-top:20px">\s*<h3>Feature Control</h3>.*?<div id="fcFeatureList"[^>]*></div>\s*</div>',
    re.DOTALL
)
new_panel = '''<div class="form-panel" style="margin-top:20px">
<h3>&#128274; App Control</h3>
<p style="color:#888;font-size:.82rem;margin:-6px 0 16px">Lock or unlock features across the entire PrintLab app</p>
<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
</div>'''

content, n1 = old_panel_pattern.subn(new_panel, content, count=1)
if n1 == 0:
    print("PANEL NOT FOUND - aborting")
else:
    # 2. Replace loadFeatureFlags + toggleFeatureFlag with global-only, nicer-styled versions
    old_js_pattern = re.compile(
        r'async function loadFeatureFlags\(\).*?async function toggleFeatureFlag\(name, enabled\)\{.*?\n\}',
        re.DOTALL
    )
    new_js = '''async function loadFeatureFlags(){
  const flags=await api('/api/v1/features');
  const list=document.getElementById('fcFeatureList');
  if(!Array.isArray(flags)){list.innerHTML='<p style="color:#c00">Failed to load features</p>';return;}
  list.innerHTML=flags.map(f=>
    '<label style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border:1px solid #ececf1;border-radius:10px;cursor:pointer;background:'+(f.enabled?'#fff':'#faf7f5')+'">'+
    '<span style="font-size:.86rem;font-weight:600;color:'+(f.enabled?'#1a223e':'#aaa')+'">'+f.label+'</span>'+
    '<span class="switch"><input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleFeatureFlag(\\''+f.feature_name+'\\', this.checked)"><span class="slider"></span></span>'+
    '</label>'
  ).join('');
}
async function toggleFeatureFlag(name, enabled){
  const r=await api('/api/v1/features/toggle','POST',{feature_name:name, enabled:enabled, shop_id:null});
  if(!r || !r.data){alert('Failed to update feature');}
  loadFeatureFlags();
}'''
    content, n2 = old_js_pattern.subn(new_js, content, count=1)
    if n2 == 0:
        print("JS NOT FOUND - panel updated but JS not replaced")
    else:
        print("Panel and JS updated successfully")

# 3. Add toggle switch CSS if not present
if '.switch{' not in content and 'class="switch"' in content:
    style_close = content.find('</style>')
    if style_close != -1:
        switch_css = '''
.switch{position:relative;display:inline-block;width:40px;height:22px;flex-shrink:0}
.switch input{opacity:0;width:0;height:0}
.switch .slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#ddd;border-radius:22px;transition:.2s}
.switch .slider:before{position:absolute;content:"";height:16px;width:16px;left:3px;bottom:3px;background:white;border-radius:50%;transition:.2s}
.switch input:checked + .slider{background:#ff5722}
.switch input:checked + .slider:before{transform:translateX(18px)}
'''
        content = content[:style_close] + switch_css + content[style_close:]
        print("Switch CSS added")
    else:
        print("No </style> tag found - CSS not added, checkboxes will look plain")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
