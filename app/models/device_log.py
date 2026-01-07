from sqlalchemy import (
    Column, Integer, String, Boolean, TIMESTAMP,
    ForeignKey, Enum
)
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import DeviceEventType

class DeviceLog(Base):
    __tablename__ = "device_logs"

    id = Column(Integer, primary_key=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    finger_id = Column(Integer)

    device_id = Column(String(64), nullable=False)
    event_type = Column(Enum(DeviceEventType), nullable=False)

    success = Column(Boolean)
    message = Column(String(256))

    timestamp = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
