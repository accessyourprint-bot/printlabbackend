import shutil
import time

PATH = "static/full_control.html"

print(f"Reading {PATH} ...")
with open(PATH, encoding="utf-8") as f:
    html = f.read()
print(f"Original size: {len(html)} bytes")

candidates = ['id="pg-appcontrol"', "id='pg-appcontrol'"]
page_start = -1
for c in candidates:
    idx = html.find(c)
    if idx != -1:
        page_start = idx
        break

if page_start == -1:
    idx = html.find("App Control")
    print("\nCould NOT find the App Control page div automatically (no pg-appcontrol id found).")
    print("Nothing has been changed. Context around the text 'App Control':\n")
    print(repr(html[max(0, idx - 200): idx + 500]))
    raise SystemExit(1)

tag_end = html.find(">", page_start) + 1
print(f"Found App Control page container at index {page_start}.")

backup_path = f"{PATH}.{time.strftime('%Y%m%d_%H%M%S')}.bak"
shutil.copy(PATH, backup_path)
print(f"Backup saved to {backup_path}")

new_controls_html = """
    <div class="control-grid" style="margin-bottom:20px">
      <div class="panel">
        <div class="panel-hd">&#9888; Global App Control</div>
        <div class="toggle-row"><span>App Enabled</span><label class="switch"><input type="checkbox" id="cfgAppEnabled" onchange="updateSystemConfig()"><span class="slider"></span></label></div>
        <div class="toggle-row"><span>Maintenance Mode</span><label class="switch"><input type="checkbox" id="cfgMaintenance" onchange="updateSystemConfig()"><span class="slider"></span></label></div>
        <div class="toggle-row"><span>Emergency Lock</span><label class="switch"><input type="checkbox" id="cfgEmergencyLock" onchange="updateSystemConfig()"><span class="slider"></span></label></div>
        <div class="toggle-row"><span>Login / Register</span><label class="switch"><input type="checkbox" id="cfgLoginEnabled" onchange="updateSystemConfig()"><span class="slider"></span></label></div>
      </div>
      <div class="panel">
        <div class="panel-hd">&#127919; Feature Flags</div>
        <div id="featureFlagsList"><div class="loading">Loading...</div></div>
      </div>
    </div>
"""

html = html[:tag_end] + new_controls_html + html[tag_end:]

js_block = """
// ========== GLOBAL APP CONTROL + FEATURE FLAGS (added by fix_app_control.py) ==========
const FEATURE_FLAG_NAMES = ['color_print','spiral_binding','delivery','front_back_printing','bulk_orders','payment_upi','payment_card','payment_cod','login_register'];

async function loadAppControlExtras(){
  try{
    const cfg = await api('/api/v1/admin/system-config');
    if(cfg){
      document.getElementById('cfgAppEnabled').checked = !!cfg.app_enabled;
      document.getElementById('cfgMaintenance').checked = !!cfg.maintenance_mode;
      document.getElementById('cfgEmergencyLock').checked = !!cfg.emergency_lock;
      document.getElementById('cfgLoginEnabled').checked = !!cfg.login_enabled;
    }
  }catch(e){ console.warn('system-config load failed', e); }

  try{
    const flags = await api('/api/v1/admin/feature-flags');
    renderFeatureFlags(Array.isArray(flags) ? flags : (flags && flags.data) || FEATURE_FLAG_NAMES.map(n=>({feature_name:n,enabled:true})));
  }catch(e){
    renderFeatureFlags(FEATURE_FLAG_NAMES.map(n=>({feature_name:n,enabled:true})));
  }
}

function renderFeatureFlags(flags){
  document.getElementById('featureFlagsList').innerHTML = flags.map(f => `
    <div class="toggle-row">
      <span>${(f.label || f.feature_name).replace(/_/g,' ')}</span>
      <label class="switch"><input type="checkbox" ${f.enabled?'checked':''} onchange="toggleFeatureFlag('${f.feature_name}', this.checked)"><span class="slider"></span></label>
    </div>`).join('');
}

async function updateSystemConfig(){
  const body = {
    app_enabled: document.getElementById('cfgAppEnabled').checked,
    maintenance_mode: document.getElementById('cfgMaintenance').checked,
    emergency_lock: document.getElementById('cfgEmergencyLock').checked,
    login_enabled: document.getElementById('cfgLoginEnabled').checked
  };
  try{ await api('/api/v1/admin/system-config','PUT',body); }
  catch(e){ console.warn('system-config update failed', e); alert('Could not save - the endpoint path may not match your backend yet.'); }
}

async function toggleFeatureFlag(name, enabled){
  try{ await api('/api/v1/admin/feature-flags/'+name, 'PUT', {enabled}); }
  catch(e){ console.warn('flag update failed', e); alert('Could not save flag - the endpoint path may not match your backend yet.'); }
}

if (typeof loadAppControl === 'function') {
  const _origLoadAppControl = loadAppControl;
  loadAppControl = function(){ _origLoadAppControl(); loadAppControlExtras(); };
} else {
  window.loadAppControl = loadAppControlExtras;
}
"""

last_script_close = html.rfind("</script>")
if last_script_close == -1:
    print("No <script> tag found - aborting before writing anything.")
    raise SystemExit(1)
html = html[:last_script_close] + js_block + "\n" + html[last_script_close:]

if ".switch {" not in html and ".switch{" not in html:
    css_block = """
<style>
.control-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.toggle-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #eee}
.toggle-row:last-child{border-bottom:none}
.switch{position:relative;display:inline-block;width:44px;height:24px}
.switch input{opacity:0;width:0;height:0}
.slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:24px;transition:.2s}
.slider:before{position:absolute;content:"";height:18px;width:18px;left:3px;bottom:3px;background-color:white;border-radius:50%;transition:.2s}
input:checked + .slider{background-color:#ff5722}
input:checked + .slider:before{transform:translateX(20px)}
</style>
"""
    head_close = html.find("</head>")
    html = (html[:head_close] + css_block + html[head_close:]) if head_close != -1 else (css_block + html)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDone. New size: {len(html)} bytes (backup at {backup_path})")
print("Added: Global App Control toggles + Feature Flags grid inside the existing App Control page.")
