import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Modal HTML: file lines 260-274 (index 259-273) -- ends right before "<!-- ADD AGENT MODAL -->"
# JS block: file lines 689-733 (index 688-732) -- ends right before "function toggleSD()"

# Remove JS block first (later in file, so indices for modal removal stay valid)
lines = lines[:688] + lines[733:]

# Now remove modal HTML block
lines = lines[:259] + lines[274:]

with io.open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("BOTH BLOCKS REMOVED")
