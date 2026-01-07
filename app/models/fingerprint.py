from sqlalchemy import (
    Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func
from app.core.database import Base

class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"))
    device_id = Column(String(64), nullable=False)
    finger_id = Column(Integer, nullable=False)

    enrolled_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("device_id", "finger_id", name="uq_device_finger"),
    )
