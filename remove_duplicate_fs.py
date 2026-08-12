import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find all line indices where "function fs(s,el){" starts
starts = [i for i, l in enumerate(lines) if l.strip() == "function fs(s,el){"]
print(f"Found {len(starts)} occurrence(s) of fs() at lines: {[i+1 for i in starts]}")

if len(starts) == 2:
    # Each fs() block is exactly 7 lines long (from the pasted output)
    first_start = starts[0]
    first_end = first_start + 7  # exclusive end, 7 lines: def line + 5 body + closing brace
    print("Removing lines:", first_start+1, "to", first_end)
    print("Content being removed:")
    print("".join(lines[first_start:first_end]))
    del lines[first_start:first_end]
    with io.open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Duplicate removed")
else:
    print("WARNING: expected exactly 2 occurrences, found", len(starts), "-- not modifying, paste this output back")
