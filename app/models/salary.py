from sqlalchemy import Column, String, Numeric
from app.core.database import Base

class Salary(Base):
    __tablename__ = "salary"

    position = Column(String(64), primary_key=True)
    monthly_salary = Column(Numeric(12, 2))
    bonus_salary = Column(Numeric(12, 2))
