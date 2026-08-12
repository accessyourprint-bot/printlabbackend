import io

path = "app/main.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = '''@app.get("/shop", response_class=_HTMLResponse, include_in_schema=False)
async def shop_control_page():
    return (_STATIC_DIR / "specific_control.html").read_text(encoding="utf-8")'''

new = '''@app.get("/shop", response_class=_HTMLResponse, include_in_schema=False)
async def shop_control_page():
    html = (_STATIC_DIR / "specific_control.html").read_text(encoding="utf-8")
    return _HTMLResponse(content=html, headers={
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    })'''

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Cache headers added to /shop route")
else:
    print("WARNING: anchor not unique - manual fix needed")
