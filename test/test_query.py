from sqlalchemy import select
from app.models.employee import Employee

async def test_query():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Employee))
        print(result.scalars().all())
