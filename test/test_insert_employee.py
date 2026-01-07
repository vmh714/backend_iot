import asyncio
from app.core.database import AsyncSessionLocal
from app.models.employee import Employee

async def test_insert():
    async with AsyncSessionLocal() as session:
        emp = Employee(
            emp_code="NV001",
            full_name="Nguyen Van A",
            position="Engineer"
        )
        session.add(emp)
        await session.commit()
        print("Insert OK")

asyncio.run(test_insert())
