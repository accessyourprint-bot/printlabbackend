from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base_class import Base  # adjust import to match your actual Base location

class ZoneFeatureFlags(Base):
    __tablename__ = "zone_feature_flags"
    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), unique=True, nullable=False)
    features = Column(JSONB, nullable=False, default=dict)