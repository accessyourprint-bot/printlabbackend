import io

path = "app/models/models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)"""

new = """    is_downloaded = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)"""

c = content.count(old)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("is_downloaded column added to Order model")
else:
    print("WARNING: anchor not unique/found")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
