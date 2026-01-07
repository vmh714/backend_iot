import asyncio
from app.core.database import engine

async def test():
    async with engine.begin() as conn:
        await conn.run_sync(lambda x: None)
    print("DB connection OK")

asyncio.run(test())
