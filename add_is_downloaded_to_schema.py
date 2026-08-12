import io

# ---- 1. Add is_downloaded to OrderOut schema ----
path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    files: List[OrderFileOut] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================
# PAYMENT SCHEMAS"""

new = """    files: List[OrderFileOut] = []
    is_downloaded: bool = False
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================
# PAYMENT SCHEMAS"""

c = content.count(old)
print(f"Schema anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("is_downloaded added to OrderOut schema")
else:
    print("WARNING: schema anchor not found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
