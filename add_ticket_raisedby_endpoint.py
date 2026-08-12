import io

path = "app/api/v1/endpoints/tickets.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    ticket = SupportTicket(
        shop_id=current_user.shop_id,
        created_by=current_user.id,
        subject=body.subject,
        description=body.description,
        priority=body.priority,
        image_url=body.image_url,
    )"""

new = """    ticket = SupportTicket(
        shop_id=current_user.shop_id,
        created_by=current_user.id,
        subject=body.subject,
        description=body.description,
        priority=body.priority,
        image_url=body.image_url,
        raised_by=body.raised_by,
    )"""

c = content.count(old)
print(f"Endpoint anchor found {c} time(s)")
if c == 1:
    content = content.replace(old, new)
    print("raised_by wired into create_ticket")
else:
    print("WARNING: anchor not unique, aborting")
    exit()

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)
