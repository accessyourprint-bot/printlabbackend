import asyncio
from app.db.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name='orders'
            AND column_name IN ('accepted_at','started_at','reached_pickup_at','picked_up_at','payout_amount','payout_recorded')
        """))
        print([row[0] for row in r.fetchall()])

asyncio.run(main())
