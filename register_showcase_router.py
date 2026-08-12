import io

path = r"app\main.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_import = "from app.api.v1.endpoints.projects import router as projects_router"
new_import = "from app.api.v1.endpoints.projects import router as projects_router\nfrom app.api.v1.endpoints.showcase import router as showcase_router"

old_include = "app.include_router(projects_router, prefix=API_PREFIX)"
new_include = "app.include_router(projects_router, prefix=API_PREFIX)\napp.include_router(showcase_router, prefix=API_PREFIX)"

if old_import not in content or old_include not in content:
    print("MARKERS NOT FOUND - aborting")
else:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_include, new_include, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("ROUTER REGISTERED SUCCESSFULLY")
