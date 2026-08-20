import asyncio
from app.db.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as db:
        r = await db.execute(text("SELECT id, address, latitude, longitude FROM shops"))
        for row in r.fetchall():
            print(dict(row._mapping))

asyncio.run(main())
