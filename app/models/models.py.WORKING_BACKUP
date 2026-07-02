"""
Alt Print - Database Models
Complete SQLAlchemy models for all tables
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey,
    Integer, JSON, Numeric, String, Text, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


def utcnow():
    return datetime.now(timezone.utc)


# ============================================================
# USER MODEL
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    role = Column(
        Enum("super_admin", "shop_admin", "user", name="user_role"),
        nullable=False,
        default="user"
    )
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    orders = relationship("Order", back_populates="user", lazy="dynamic")
    refresh_tokens = relationship("RefreshToken", back_populates="user", lazy="dynamic")
    shop = relationship("Shop", foreign_keys=[shop_id], back_populates="admin_user")


# ============================================================
# SHOP MODEL
# ============================================================
class Shop(Base):
    __tablename__ = "shops"

    id = Column(String(50), primary_key=True)  # e.g. "shop-001"
    name = Column(String(255), nullable=False)
    owner_name = Column(String(255), nullable=True)
    owner_email = Column(String(255), nullable=False, index=True)
    owner_phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    delivery_radius_km = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True, nullable=False)
    # Working hours stored as JSON: {"mon": {"open": "09:00", "close": "21:00"}, ...}
    working_hours = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    orders = relationship("Order", back_populates="shop", lazy="dynamic")
    feature_flags = relationship("FeatureFlag", back_populates="shop", lazy="dynamic")
    admin_user = relationship("User", foreign_keys="User.shop_id", back_populates="shop", lazy="select")


# ============================================================
# SYSTEM CONFIG MODEL
# ============================================================
class SystemConfig(Base):
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, default=1)
    app_enabled = Column(Boolean, default=True, nullable=False)
    maintenance_mode = Column(Boolean, default=False, nullable=False)
    emergency_lock = Column(Boolean, default=False, nullable=False)
    uploads_enabled = Column(Boolean, default=True, nullable=False)
    payments_enabled = Column(Boolean, default=True, nullable=False)
    delivery_enabled = Column(Boolean, default=True, nullable=False)
    printing_enabled = Column(Boolean, default=True, nullable=False)
    login_enabled = Column(Boolean, default=True, nullable=False)
    orders_enabled = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    updated_by = Column(String(255), nullable=True)


# ============================================================
# FEATURE FLAG MODEL
# ============================================================
class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_name = Column(String(100), nullable=False, index=True)
    label = Column(String(255), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    scope = Column(
        Enum("global", "shop", name="feature_scope"),
        nullable=False,
        default="global"
    )
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    updated_by = Column(String(255), nullable=True)

    # Relationships
    shop = relationship("Shop", back_populates="feature_flags")

    __table_args__ = (
        UniqueConstraint("feature_name", "shop_id", name="uq_feature_shop"),
        Index("ix_feature_flags_name_scope", "feature_name", "scope"),
    )


# ============================================================
# AUDIT LOG MODEL
# ============================================================
class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor = Column(String(255), nullable=False, index=True)
    role = Column(String(50), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    target = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


# ============================================================
# ORDER MODEL
# ============================================================
class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(20), unique=True, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    status = Column(
        Enum(
            "pending", "confirmed", "processing",
            "ready", "out_for_delivery", "delivered",
            "cancelled", "refunded",
            name="order_status"
        ),
        default="pending",
        nullable=False
    )
    delivery_type = Column(
        Enum("self_pickup", "home_delivery", name="delivery_type"),
        nullable=False,
        default="self_pickup"
    )
    delivery_address = Column(Text, nullable=True)
    delivery_lat = Column(Float, nullable=True)
    delivery_lng = Column(Float, nullable=True)
    delivery_distance_km = Column(Float, nullable=True)
    special_instructions = Column(Text, nullable=True)

    # Pricing breakdown
    printing_cost = Column(Numeric(10, 2), default=0)
    color_cost = Column(Numeric(10, 2), default=0)
    binding_cost = Column(Numeric(10, 2), default=0)
    delivery_cost = Column(Numeric(10, 2), default=0)
    subtotal = Column(Numeric(10, 2), default=0)
    gst_amount = Column(Numeric(10, 2), default=0)
    grand_total = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    shop = relationship("Shop", back_populates="orders")
    files = relationship("OrderFile", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)


# ============================================================
# ORDER FILE MODEL
# ============================================================
class OrderFile(Base):
    __tablename__ = "order_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Storage
    storage_key = Column(String(500), nullable=False)  # Random key in S3/R2
    nonce = Column(String(100), nullable=False)         # AES-GCM nonce (hex)
    original_filename = Column(String(500), nullable=False)
    content_type = Column(String(100), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)

    # Document properties
    page_count = Column(Integer, default=1, nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, image

    # Print customization per file
    print_color = Column(
        Enum("black_white", "color", name="print_color_type"),
        default="black_white"
    )
    copies = Column(Integer, default=1, nullable=False)
    is_front_back = Column(Boolean, default=False)
    spiral_binding = Column(Boolean, default=False)
    colored_binding_sheet = Column(Boolean, default=False)
    custom_instructions = Column(Text, nullable=True)

    # Per-file cost
    file_cost = Column(Numeric(10, 2), default=0)

    # Lifecycle
    status = Column(
        Enum("uploaded", "pending_approval", "approved", "rejected", "processing", "ready", "printed", "deleted", name="file_status"),
        default="uploaded"
    )
    expires_at = Column(DateTime(timezone=True), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="files")
    user = relationship("User")


# ============================================================
# PAYMENT MODEL
# ============================================================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False, unique=True)
    razorpay_order_id = Column(String(100), nullable=True, index=True)
    razorpay_payment_id = Column(String(100), nullable=True, index=True)
    razorpay_signature = Column(String(500), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default="INR")
    method = Column(
        Enum("upi", "card", "cod", "qr", name="payment_method"),
        nullable=True
    )
    status = Column(
        Enum("pending", "completed", "failed", "refunded", name="payment_status"),
        default="pending"
    )
    gateway_response = Column(JSON, nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    order = relationship("Order", back_populates="payment")


# ============================================================
# REFRESH TOKEN MODEL
# ============================================================
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    device_info = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")


# ============================================================
# WEBSOCKET SESSION MODEL
# ============================================================
class WebSocketSession(Base):
    __tablename__ = "websocket_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    session_token = Column(String(255), nullable=False, unique=True, index=True)
    client_type = Column(String(50), nullable=True)  # android, ios, web, tablet
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    disconnected_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)



class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False, default="units")
    low_stock_threshold = Column(Integer, nullable=False, default=10)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=False)
    status = Column(String(20), nullable=False, default="open")
    priority = Column(String(20), nullable=False, default="normal")
    admin_response = Column(String(2000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class DeliveryPerson(Base):
    __tablename__ = "delivery_persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    vehicle_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    current_status = Column(String(20), nullable=False, default="available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PrintPricing(Base):
    __tablename__ = "print_pricing"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=True)
    print_type = Column(String(50), nullable=False)
    price_per_page = Column(Float, nullable=False)
    is_global = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)


class ShopEarnings(Base):
    __tablename__ = "shop_earnings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_id = Column(String(50), ForeignKey("shops.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
