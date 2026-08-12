import io

path = "app/schemas/schemas.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = """class FeatureFlagOut(BaseModel):
    id: int
    feature_name: str
    label: str
    enabled: bool
    scope: str
    shop_id: Optional[str]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True"""

new_schemas = anchor + '''


class AppAppearanceOut(BaseModel):
    primary_color: str
    secondary_color: str
    font_family: str
    logo_url: Optional[str]
    banner_text: str
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UpdateAppAppearanceRequest(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    font_family: Optional[str] = None
    logo_url: Optional[str] = None
    banner_text: Optional[str] = None'''

count = content.count(anchor)
print(f"Found anchor {count} time(s)")
if count == 1:
    content = content.replace(anchor, new_schemas)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Schemas inserted")
else:
    print("Anchor not unique or not found - no changes written")
