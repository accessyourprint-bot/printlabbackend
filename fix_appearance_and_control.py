import re, io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

changes = []

# 1. Remove the dead first loadAppControl (line ~858) - keep only the one with loadFeatureFlags
dead_loadappcontrol = "function loadAppControl(){console.log(\"LOADAPPCONTROL CALLED\");updatePreview();loadFeatureFlags();}"
# find the OTHER (dead) one - the plain updatePreview-only version
plain_loadappcontrol = "function loadAppControl(){updatePreview();}"
c = content.count(plain_loadappcontrol)
if c >= 1:
    content = content.replace(plain_loadappcontrol, "", 1)
    changes.append(f"Removed {c} dead loadAppControl stub(s)")
else:
    changes.append("No dead loadAppControl stub found")

# 2. Remove debug console.log marker now that we've confirmed it fires
content = content.replace('console.log("LOADAPPCONTROL CALLED");', '')
changes.append("Removed debug marker")

# 3. Replace the dead saveAppSettings (first def, posts to admin/app-settings) - remove it entirely
dead_save_pattern = re.compile(
    r"async function saveAppSettings\(\)\{\s*const settings=\{primary_color:.*?catch\(e\)\{alert\('Saved locally - connect /api/v1/admin/app-settings endpoint'\);\}\s*\}",
    re.DOTALL
)
content, n = dead_save_pattern.subn("", content, count=1)
changes.append(f"Removed dead saveAppSettings: {n} occurrence(s)")

# 4. Replace the real saveAppSettings to hit /api/v1/appearance instead of /api/v1/system/config
old_save = """async function saveAppSettings(){
  const font=document.querySelector('#acFonts .font-btn.on')?.textContent||'Inter';
  const s={primary_color:document.getElementById('acPrim').value,secondary_color:document.getElementById('acSec').value,font_family:font,logo_url:document.getElementById('acLogo').value,banner_text:document.getElementById('acBanner').value};
  const r=await api('/api/v1/system/config','PUT',s);
  if(r)alert('Appearance saved!');else alert('Error saving');
}"""
new_save = """async function saveAppSettings(){
  const font=document.querySelector('#acFonts .font-btn.on')?.textContent||'Inter';
  const s={primary_color:document.getElementById('acPrim').value,secondary_color:document.getElementById('acSec').value,font_family:font,logo_url:document.getElementById('acLogo').value,banner_text:document.getElementById('acBanner').value};
  const r=await api('/api/v1/appearance','PUT',s);
  if(r&&r.data)alert('Appearance saved!');else alert('Error saving - check console');
}"""
c2 = content.count(old_save)
if c2 == 1:
    content = content.replace(old_save, new_save)
    changes.append("Rewired saveAppSettings to /api/v1/appearance")
else:
    changes.append(f"WARNING: real saveAppSettings anchor matched {c2} times (expected 1) - not replaced")

# 5. Make loadAppControl also load saved appearance on page open (so App Appearance panel shows saved values, not just defaults)
old_loadappcontrol2 = "function loadAppControl(){updatePreview();loadFeatureFlags();}"
new_loadappcontrol2 = """function loadAppControl(){loadSavedAppearance();loadFeatureFlags();}
async function loadSavedAppearance(){
  const a=await api('/api/v1/appearance');
  if(!a||a.detail)return;
  document.getElementById('acPrim').value=a.primary_color;
  document.getElementById('acPrimSw').style.background=a.primary_color;
  document.getElementById('acSec').value=a.secondary_color;
  document.getElementById('acSecSw').style.background=a.secondary_color;
  document.getElementById('acLogo').value=a.logo_url||'';
  document.getElementById('acBanner').value=a.banner_text;
  document.querySelectorAll('#acFonts .font-btn').forEach(b=>b.classList.toggle('on', b.textContent===a.font_family));
  updatePreview();
}"""
c3 = content.count(old_loadappcontrol2)
if c3 == 1:
    content = content.replace(old_loadappcontrol2, new_loadappcontrol2)
    changes.append("Added loadSavedAppearance, wired into loadAppControl")
else:
    changes.append(f"WARNING: loadAppControl anchor matched {c3} times (expected 1) - not replaced")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("\\n".join(changes))
