import asyncio
from app.core.database import engine
from app.core.database import Base

# IMPORT ALL MODELS (RẤT QUAN TRỌNG)
from app.models.employee import Employee
from app.models.salary import Salary
from app.models.fingerprint import Fingerprint
from app.models.attendance_daily import AttendanceDaily
from app.models.device_log import DeviceLog
from app.models.user import User

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")

asyncio.run(create_all())
