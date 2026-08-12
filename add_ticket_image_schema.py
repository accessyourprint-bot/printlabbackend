import io

path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3, max_length=2000)
    priority: str = Field("normal", pattern="^(low|normal|high|urgent)$")"""

new = """class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3, max_length=2000)
    priority: str = Field("normal", pattern="^(low|normal|high|urgent)$")
    image_url: Optional[str] = None"""

c = content.count(old)
print(f"Schema anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("image_url added to TicketCreate")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
