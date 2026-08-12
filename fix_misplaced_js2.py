import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Lines are 0-indexed in the list; file line 37 = index 36, file line 88 = index 87
# Extract the misplaced block (lines 37 to 88 inclusive)
misplaced_block = lines[36:88]  # index 36 through 87 inclusive = file lines 37-88

# Remove it from its current position
remaining = lines[:36] + lines[88:]

# Find the toggleSD line in the remaining list
toggle_idx = None
for i, line in enumerate(remaining):
    if "function toggleSD()" in line:
        toggle_idx = i
        break

if toggle_idx is None:
    print("toggleSD line not found after removal - aborting, restoring original")
else:
    new_lines = remaining[:toggle_idx] + misplaced_block + ["\n"] + remaining[toggle_idx:]
    with io.open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("MOVED SUCCESSFULLY")
