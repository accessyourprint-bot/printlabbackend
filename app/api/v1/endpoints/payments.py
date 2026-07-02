"""
Alt Print - Payment Endpoints
Razorpay integration, UPI, QR, COD, webhooks
"""
import hashlib
import hmac
import json
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.models.models import Order, Payment, SystemConfig, User
from app.schemas.schemas import (
    APIResponse,
    CreatePaymentRequest,
    PaymentOut,
    VerifyPaymentRequest,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


async def _check_payments_enabled(db: AsyncSession) -> None:
    result = await db.execute(select(SystemConfig).where(SystemConfig.id == 1))
    config = result.scalar_one_or_none()
    if config and (not config.payments_enabled or config.emergency_lock):
        raise HTTPException(status_code=503, detail="Payments are currently disabled")


def _get_razorpay_client():
    """Get Razorpay client. Returns None if not configured."""
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return None
    try:
        import razorpay
        return razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    except ImportError:
        return None


@router.post("/create", response_model=APIResponse)
async def create_payment(
    body: CreatePaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a payment for an order"""
    await _check_payments_enabled(db)

    # Fetch order
    result = await db.execute(
        select(Order).where(Order.id == body.order_id, Order.user_id == current_user.id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status not in ("pending", "confirmed"):
        raise HTTPException(status_code=400, detail="Order not in payable state")

    # Check existing payment
    existing = await db.execute(select(Payment).where(Payment.order_id == order.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Payment already created for this order")

    razorpay_order_id = None
    response_data = {}

    if body.method in ("upi", "card", "qr"):
        # Create Razorpay order
        rz_client = _get_razorpay_client()
        if rz_client:
            try:
                rz_order = rz_client.order.create({
                    "amount": int(float(order.grand_total) * 100),  # paise
                    "currency": "INR",
                    "receipt": order.order_number,
                    "notes": {
                        "order_id": str(order.id),
                        "shop_id": order.shop_id,
                    },
                })
                razorpay_order_id = rz_order["id"]
                response_data = {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "amount": int(float(order.grand_total) * 100),
                    "currency": "INR",
                    "order_number": order.order_number,
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Payment gateway error: {str(e)}")
        else:
            # Mock for development
            razorpay_order_id = f"order_mock_{order.order_number}"
            response_data = {
                "razorpay_order_id": razorpay_order_id,
                "amount": int(float(order.grand_total) * 100),
                "currency": "INR",
                "note": "Payment gateway not configured - test mode",
            }

    elif body.method == "cod":
        response_data = {
            "message": "Cash on Delivery selected",
            "amount": float(order.grand_total),
        }

    # Save payment record
    payment = Payment(
        order_id=order.id,
        razorpay_order_id=razorpay_order_id,
        amount=order.grand_total,
        currency="INR",
        method=body.method,
        status="pending" if body.method != "cod" else "pending",
        gateway_response=response_data,
    )
    db.add(payment)

    # For COD, auto-confirm order
    if body.method == "cod":
        order.status = "confirmed"

    await db.flush()
    await db.refresh(payment)

    return APIResponse(
        message="Payment created",
        data={**PaymentOut.model_validate(payment).model_dump(), **response_data},
    )


@router.post("/verify", response_model=APIResponse)
async def verify_payment(
    body: VerifyPaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Verify Razorpay payment signature"""
    # Find payment by razorpay order ID
    result = await db.execute(
        select(Payment).where(Payment.razorpay_order_id == body.razorpay_order_id)
    )
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    order_result = await db.execute(select(Order).where(Order.id == payment.order_id))
    order = order_result.scalar_one_or_none()
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Verify signature
    generated_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode() if settings.RAZORPAY_KEY_SECRET else b"test",
        f"{body.razorpay_order_id}|{body.razorpay_payment_id}".encode(),
        hashlib.sha256,
    ).hexdigest()

    if generated_signature != body.razorpay_signature:
        payment.status = "failed"
        await db.flush()
        raise HTTPException(status_code=400, detail="Payment verification failed - invalid signature")

    # Mark payment as completed
    payment.razorpay_payment_id = body.razorpay_payment_id
    payment.razorpay_signature = body.razorpay_signature
    payment.status = "completed"
    payment.paid_at = datetime.now(timezone.utc)

    # Update order status
    order.status = "confirmed"

    await db.flush()

    return APIResponse(
        message="Payment verified successfully",
        data={"payment_id": str(payment.id), "status": "completed"},
    )


@router.post("/webhook", include_in_schema=False)
async def razorpay_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Razorpay webhook endpoint.
    Configure this URL in your Razorpay dashboard.
    """
    body_bytes = await request.body()
    webhook_signature = request.headers.get("X-Razorpay-Signature", "")

    # Verify webhook signature
    if settings.RAZORPAY_KEY_SECRET:
        expected = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            body_bytes,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, webhook_signature):
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

    event = json.loads(body_bytes)
    event_type = event.get("event", "")

    if event_type == "payment.captured":
        payment_entity = event["payload"]["payment"]["entity"]
        rz_order_id = payment_entity.get("order_id")

        if rz_order_id:
            result = await db.execute(
                select(Payment).where(Payment.razorpay_order_id == rz_order_id)
            )
            payment = result.scalar_one_or_none()
            if payment and payment.status == "pending":
                payment.status = "completed"
                payment.razorpay_payment_id = payment_entity.get("id")
                payment.paid_at = datetime.now(timezone.utc)

                order_result = await db.execute(
                    select(Order).where(Order.id == payment.order_id)
                )
                order = order_result.scalar_one_or_none()
                if order:
                    order.status = "confirmed"

                await db.flush()

    return {"status": "ok"}
