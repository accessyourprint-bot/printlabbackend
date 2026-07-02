"""
Alt Print - Pydantic Schemas
Request/Response validation models
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


# ============================================================
# BASE / COMMON
# ============================================================
class APIResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int


# ============================================================
# AUTH SCHEMAS
# ============================================================
class RegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{9,14}$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Email or phone required")
        return self


class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    otp: Optional[str] = None


class OTPRequest(BaseModel):
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{9,14}$")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str
    user_id: str


class RefreshRequest(BaseModel):
    refresh_token: str


# ============================================================
# USER SCHEMAS
# ============================================================
class UserOut(BaseModel):
    id: UUID
    email: Optional[str]
    phone: Optional[str]
    full_name: Optional[str]
    role: str
    shop_id: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# SYSTEM CONFIG SCHEMAS
# ============================================================
class SystemConfigOut(BaseModel):
    id: int
    app_enabled: bool
    maintenance_mode: bool
    emergency_lock: bool
    uploads_enabled: bool
    payments_enabled: bool
    delivery_enabled: bool
    printing_enabled: bool
    login_enabled: bool
    orders_enabled: bool
    updated_at: Optional[datetime]
    updated_by: Optional[str]

    class Config:
        from_attributes = True


class UpdateAppStateRequest(BaseModel):
    app_enabled: Optional[bool] = None
    maintenance_mode: Optional[bool] = None
    emergency_lock: Optional[bool] = None
    uploads_enabled: Optional[bool] = None
    payments_enabled: Optional[bool] = None
    delivery_enabled: Optional[bool] = None
    printing_enabled: Optional[bool] = None
    login_enabled: Optional[bool] = None
    orders_enabled: Optional[bool] = None


# ============================================================
# FEATURE FLAG SCHEMAS
# ============================================================
class FeatureFlagOut(BaseModel):
    id: int
    feature_name: str
    label: str
    enabled: bool
    scope: str
    shop_id: Optional[str]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ToggleFeatureRequest(BaseModel):
    feature_name: str
    enabled: bool
    shop_id: Optional[str] = None  # None = global scope


# ============================================================
# SHOP SCHEMAS
# ============================================================
class CreateShopRequest(BaseModel):
    id: Optional[str] = None  # e.g. "shop-004"; auto-generated if not provided
    name: str = Field(..., min_length=2, max_length=255)
    owner_name: Optional[str] = None
    owner_email: EmailStr
    owner_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    delivery_radius_km: float = Field(5.0, ge=0.5, le=50.0)
    admin_password: Optional[str] = Field(None, min_length=8)


class UpdateShopRequest(BaseModel):
    name: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    delivery_radius_km: Optional[float] = Field(None, ge=0.5, le=50.0)
    working_hours: Optional[Dict] = None
    is_active: Optional[bool] = None


class ShopOut(BaseModel):
    id: str
    name: str
    owner_name: Optional[str]
    owner_email: str
    owner_phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    delivery_radius_km: float
    is_active: bool
    working_hours: Optional[Dict]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class AdminUserOut(BaseModel):
    id: UUID
    email: Optional[str]
    phone: Optional[str]
    full_name: Optional[str]
    role: str
    shop_id: Optional[str]
    is_active: bool
    is_verified: bool
    failed_login_attempts: int
    locked_until: Optional[datetime]
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class AdminOverviewOut(BaseModel):
    system_config: SystemConfigOut
    totals: Dict[str, int]
    shops: List[ShopOut]


class ProjectOut(BaseModel):
    id: UUID
    original_filename: str
    page_count: int
    file_type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectPrintRequest(BaseModel):
    shop_id: str
    file_ids: List[UUID]
    file_customizations: Dict[str, "FileCustomization"] = Field(default_factory=dict)
    delivery_type: str = Field("self_pickup", pattern="^(self_pickup|home_delivery)$")
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    delivery_distance_km: Optional[float] = Field(None, ge=0)
    special_instructions: Optional[str] = None


# ============================================================
# AUDIT LOG SCHEMAS
# ============================================================
class AuditLogOut(BaseModel):
    id: int
    actor: str
    role: Optional[str]
    action: str
    target: Optional[str]
    details: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# FILE / ORDER SCHEMAS
# ============================================================
class FileCustomization(BaseModel):
    print_color: str = Field("black_white", pattern="^(black_white|color)$")
    copies: int = Field(1, ge=1, le=100)
    is_front_back: bool = False
    spiral_binding: bool = False
    colored_binding_sheet: bool = False
    custom_instructions: Optional[str] = None


class OrderFileOut(BaseModel):
    id: UUID
    original_filename: str
    page_count: int
    file_type: str
    print_color: str
    copies: int
    is_front_back: bool
    spiral_binding: bool
    colored_binding_sheet: bool
    custom_instructions: Optional[str]
    file_cost: float
    status: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class CreateOrderRequest(BaseModel):
    shop_id: str
    file_ids: List[UUID]  # Already uploaded file IDs
    file_customizations: Dict[str, FileCustomization]  # file_id -> customization
    delivery_type: str = Field("self_pickup", pattern="^(self_pickup|home_delivery)$")
    delivery_address: Optional[str] = None
    delivery_lat: Optional[float] = None
    delivery_lng: Optional[float] = None
    delivery_distance_km: Optional[float] = Field(None, ge=0)
    special_instructions: Optional[str] = None


class OrderOut(BaseModel):
    id: UUID
    order_number: str
    shop_id: str
    status: str
    delivery_type: str
    printing_cost: float
    color_cost: float
    binding_cost: float
    delivery_cost: float
    subtotal: float
    gst_amount: float
    grand_total: float
    files: List[OrderFileOut] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================
# PAYMENT SCHEMAS
# ============================================================
class CreatePaymentRequest(BaseModel):
    order_id: UUID
    method: str = Field(..., pattern="^(upi|card|cod|qr)$")


class PaymentOut(BaseModel):
    id: UUID
    order_id: UUID
    razorpay_order_id: Optional[str]
    amount: float
    currency: str
    method: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


# ============================================================
# PRICING SCHEMAS
# ============================================================
class PriceCalculationRequest(BaseModel):
    shop_id: str
    files: List[Dict]  # [{file_id, page_count, print_color, copies, is_front_back, ...}]
    delivery_type: str = "self_pickup"
    delivery_distance_km: Optional[float] = None


class PriceBreakdown(BaseModel):
    printing_cost: float
    color_cost: float
    front_back_cost: float
    binding_cost: float
    delivery_cost: float
    subtotal: float
    gst_rate: float
    gst_amount: float
    grand_total: float
    per_file_costs: List[Dict]


# ============================================================
# WEBSOCKET SCHEMAS
# ============================================================
class WSMessage(BaseModel):
    type: str
    payload: Dict
    timestamp: Optional[datetime] = None


class StockItemCreate(BaseModel):
    item_name: str
    quantity: int = 0
    unit: str = "units"
    low_stock_threshold: int = 10
    shop_id: Optional[str] = None


class StockItemUpdate(BaseModel):
    quantity: Optional[int] = None
    unit: Optional[str] = None
    low_stock_threshold: Optional[int] = None


class StockItemOut(BaseModel):
    id: UUID
    shop_id: str
    item_name: str
    quantity: int
    unit: str
    low_stock_threshold: int
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketCreate(BaseModel):
    subject: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3, max_length=2000)
    priority: str = Field("normal", pattern="^(low|normal|high|urgent)$")


class TicketUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(open|in_progress|resolved|closed)$")
    admin_response: Optional[str] = None


class TicketOut(BaseModel):
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
        from_attributes = True


class DeliveryPersonCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., min_length=10, max_length=15)
    vehicle_number: Optional[str] = None


class DeliveryPersonUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    vehicle_number: Optional[str] = None
    is_active: Optional[bool] = None
    current_status: Optional[str] = Field(None, pattern="^(available|busy|offline)$")


class DeliveryPersonOut(BaseModel):
    id: UUID
    shop_id: str
    name: str
    phone: str
    vehicle_number: Optional[str] = None
    is_active: bool
    current_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PricingCreate(BaseModel):
    print_type: str
    price_per_page: float
    shop_id: Optional[str] = None
    is_global: bool = True

class PricingOut(BaseModel):
    id: UUID
    shop_id: Optional[str] = None
    print_type: str
    price_per_page: float
    is_global: bool
    updated_at: datetime
    class Config:
        from_attributes = True

class ShopEarningsOut(BaseModel):
    shop_id: str
    total_earnings: float
    order_count: int
    jobs_done: int
