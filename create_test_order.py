import asyncio
from app.db.database import AsyncSessionLocal
from app.models.models import Order, Shop, User
from sqlalchemy import select
import uuid
from datetime import datetime, timezone

async def main():
    async with AsyncSessionLocal() as db:
        shop = (await db.execute(select(Shop))).scalars().first()
        user = (await db.execute(select(User).where(User.role == "user"))).scalars().first()
        if not shop or not user:
            print(f"FAIL: shop={shop}, user={user} - need at least one shop and one customer user in DB")
            return

        order = Order(
            id=uuid.uuid4(),
            order_number="TEST-" + str(uuid.uuid4())[:8].upper(),
            user_id=user.id,
            shop_id=shop.id,
            status="ready",
            delivery_type="home_delivery",
            delivery_address="123 Test Street, Koramangala, Bengaluru",
            delivery_lat=12.9352,
            delivery_lng=77.6146,
            delivery_cost=45,
            grand_total=245,
        )
        db.add(order)
        await db.commit()
        print(f"SUCCESS: created test order {order.order_number} (id={order.id}) at shop {shop.id}, status=ready")

asyncio.run(main())
