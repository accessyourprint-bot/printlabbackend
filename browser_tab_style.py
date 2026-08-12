import io

path = "static/specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- Add new CSS for browser-tab style, right after existing .ttab rules ----
old_css = """.ttab.on{background:#1a1a1a;border-color:#1a1a1a;color:#fff;}"""

new_css = """.ttab.on{background:#1a1a1a;border-color:#1a1a1a;color:#fff;}

/* BROWSER-TAB STYLE FOR STATUS FILTER */
.stabs{background:#2b2b2b;padding:8px 8px 0 8px;border-radius:10px 10px 0 0;display:flex;gap:4px;}
.stabs .ttab{border:none;border-radius:8px 8px 0 0;background:#3d3d3d;color:#ccc;padding:9px 20px;font-size:.82rem;font-weight:600;margin-bottom:0;}
.stabs .ttab:hover{background:#4a4a4a;color:#fff;border-color:transparent;}
.stabs .ttab.on{background:#fff;color:#1a1a1a;position:relative;top:1px;}"""

c1 = content.count(old_css)
print(f"CSS anchor found {c1} time(s)")
if c1 == 1:
    content = content.replace(old_css, new_css)
    print("Browser-tab CSS added")
else:
    print("WARNING: CSS anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
