import io

path = r"app\models\models.py"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

marker = "class OrderFile(Base):"
idx = content.find(marker)
if idx == -1:
    print("MARKER NOT FOUND - aborting")
else:
    # find the end of the OrderFile class by locating the next "class " after marker
    next_class_idx = content.find("\nclass ", idx + len(marker))
    if next_class_idx == -1:
        print("COULD NOT FIND END OF ORDERFILE CLASS - aborting")
    else:
        new_model = '''

class ShopShowcase(Base):
    __tablename__ = "shop_showcase"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    title = Column(String(255), nullable=False)
    storage_key = Column(String(500), nullable=False)
    nonce = Column(String(100), nullable=False)
    original_filename = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
'''
        content = content[:next_class_idx] + new_model + content[next_class_idx:]
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("MODEL ADDED SUCCESSFULLY")
