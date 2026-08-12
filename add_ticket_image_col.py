import io

path = "app/models/models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    admin_response = Column(String(2000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class DeliveryPerson(Base):"""

new = """    admin_response = Column(String(2000), nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class DeliveryPerson(Base):"""

c = content.count(old)
print(f"Model anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("image_url column added to SupportTicket model")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
