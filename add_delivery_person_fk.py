import io

path = "app/models/models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = """    delivery_distance_km = Column(Float, nullable=True)
    special_instructions = Column(Text, nullable=True)"""

new = """    delivery_distance_km = Column(Float, nullable=True)
    delivery_person_id = Column(UUID(as_uuid=True), ForeignKey("delivery_persons.id"), nullable=True)
    special_instructions = Column(Text, nullable=True)"""

c = content.count(anchor)
print(f"Anchor found {c} time(s)")
if c == 1:
    content = content.replace(anchor, new)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Order model updated with delivery_person_id")
else:
    print("WARNING: anchor not unique - manual fix needed")
