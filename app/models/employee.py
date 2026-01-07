from sqlalchemy import (
    Column, Integer, String, Date, Boolean, TIMESTAMP, Enum
)
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.enums import GenderEnum

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    emp_code = Column(String(32), unique=True, index=True)
    full_name = Column(String(128), nullable=False)

    gender = Column(Enum(GenderEnum, name="gender_enum"))
    dob = Column(Date)

    phone_number = Column(String(20))
    email = Column(String(128))

    start_date = Column(Date)
    position = Column(String(64))

    active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
