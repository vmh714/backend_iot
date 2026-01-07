from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.enums import GenderEnum

class EmployeeCreate(BaseModel):
    emp_code: str
    full_name: str
    gender: Optional[GenderEnum]
    dob: Optional[date]
    phone_number: Optional[str]
    email: Optional[str]
    position: str

class EmployeeResponse(BaseModel):
    id: int
    emp_code: str
    full_name: str
    position: str
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
