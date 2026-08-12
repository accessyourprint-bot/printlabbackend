import io

path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """class TicketOut(BaseModel):
    id: UUID
    shop_id: str
    created_by: UUID
    subject: str
    description: str
    status: str
    priority: str
    admin_response: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True"""

new = """class TicketOut(BaseModel):
    id: UUID
    shop_id: str
    created_by: UUID
    subject: str
    description: str
    status: str
    priority: str
    admin_response: Optional[str] = None
    raised_by: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True"""

c = content.count(old)
print(f"TicketOut anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("raised_by and image_url added to TicketOut")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
