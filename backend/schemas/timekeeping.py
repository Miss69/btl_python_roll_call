from pydantic import BaseModel
from typing import Optional

class TimekeepingBase(BaseModel):
    id_employee: int

class TimekeepingCreate(TimekeepingBase):
    check_in: str
    date: Optional[str] = None

class TimekeepingCheckout(TimekeepingBase):
    check_out: str
    date: Optional[str] = None

class TimekeepingResponse(TimekeepingBase):
    id_timekeeping: int
    check_in: Optional[str]
    check_out: Optional[str]
    date: Optional[str]

    class Config:
        orm_mode = True
