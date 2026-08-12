import io

path = "app/models/models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

anchor = '''    __table_args__ = (
        UniqueConstraint("feature_name", "shop_id", name="uq_feature_shop"),
        Index("ix_feature_flags_name_scope", "feature_name", "scope"),
    )'''

new_model = anchor + '''


class AppAppearance(Base):
    __tablename__ = "app_appearance"

    id = Column(Integer, primary_key=True, default=1)
    primary_color = Column(String(20), nullable=False, default="#ff5722")
    secondary_color = Column(String(20), nullable=False, default="#1a223e")
    font_family = Column(String(50), nullable=False, default="Inter")
    logo_url = Column(String(500), nullable=True)
    banner_text = Column(String(255), nullable=False, default="PrintLab")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())'''

count = content.count(anchor)
print(f"Found anchor {count} time(s)")
if count == 1:
    content = content.replace(anchor, new_model)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Model inserted")
else:
    print("Anchor not unique or not found - no changes written")
