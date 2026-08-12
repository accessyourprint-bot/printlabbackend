import io

path = "static/full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "function loadAppControl(){updatePreview();loadFeatureFlags();}"
new = "function loadAppControl(){console.log(\"LOADAPPCONTROL CALLED\");updatePreview();loadFeatureFlags();}"

count = content.count(old)
print(f"Found {count} occurrence(s)")
content = content.replace(old, new)

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
