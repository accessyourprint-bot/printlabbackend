import io

path = "app/main.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

import_anchor = "from app.api.v1.endpoints.appearance import router as appearance_router"
new_import = import_anchor + "\nfrom app.api.v1.endpoints.tracking import router as tracking_router"

route_anchor = "app.include_router(appearance_router, prefix=API_PREFIX)"
new_route = route_anchor + "\napp.include_router(tracking_router, prefix=API_PREFIX)"

c1 = content.count(import_anchor)
c2 = content.count(route_anchor)
print(f"Import anchor found {c1}, route anchor found {c2}")

if c1 == 1 and c2 == 1:
    content = content.replace(import_anchor, new_import)
    content = content.replace(route_anchor, new_route)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Tracking router wired successfully")
else:
    print("Anchors not unique - no changes written")
