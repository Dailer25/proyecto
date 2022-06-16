from pydantic import BaseModel, constr
from enum import Enum
from typing import Optional
from datetime import datetime
from catalog.schema import Flight
from user.schema import User

class BookingStatus(str, Enum):
    UNCONFIRMED = 'UNCONFIRMED'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'

class BookingBase(BaseModel):
    status: BookingStatus = None
    paymentToken: str
    checkedIn: bool = False
    createdAt: datetime
    bookingReference: constr(max_length=40)

class BookingCreate(BookingBase):
    pass

class BookingInDBBase(BookingBase):
    id: int
    flight: Flight
    customer: User
    class Config:
        orm_mode = True

class Booking(BookingInDBBase):
    pass

class BookingInDB(BookingInDBBase):
    pass