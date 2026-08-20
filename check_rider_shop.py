import asyncio
from app.db.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text(
            "SELECT dp.id, dp.name, dp.shop_id, dp.user_id, u.phone "
            "FROM delivery_persons dp JOIN users u ON u.id = dp.user_id"
        ))
        for row in r.fetchall():
            print(dict(row._mapping))

asyncio.run(main())
