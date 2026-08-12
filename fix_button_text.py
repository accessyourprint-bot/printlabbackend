import io, re

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r'(<button onclick="markOutForDelivery\([^)]*\)"[^>]*>)([^<]*)(</button>)')
matches = pattern.findall(content)
print(f"markOutForDelivery button found {len(matches)} time(s)")
if len(matches) == 1:
    content = pattern.sub(r'\1&#10003; Completed\3', content, count=1)
    print("Button text changed to 'Completed'")
else:
    print("WARNING: button anchor not found or ambiguous, no changes made")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
