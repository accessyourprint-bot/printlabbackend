import re, io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = "function loadAppControl(){updatePreview();loadSysToggles();loadFeatToggles();loadOutletShops();}"
new_line = "function loadAppControl(){updatePreview();loadFeatureFlags();}"

count = content.count(old_line)
if count == 0:
    print("EXACT LINE NOT FOUND - no changes written")
else:
    content = content.replace(old_line, new_line)
    print(f"Replaced {count} occurrence(s)")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
