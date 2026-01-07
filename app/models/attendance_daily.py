from sqlalchemy import (
    Column, BigInteger, Integer, Date, DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func
from app.core.database import Base

class AttendanceDaily(Base):
    __tablename__ = "attendance_daily"

    id = Column(BigInteger, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    work_date = Column(Date, nullable=False)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime)

    total_minutes = Column(Integer)
    ot_minutes = Column(Integer)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("employee_id", "work_date", name="uq_attendance_day"),
    )
