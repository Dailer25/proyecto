from typing import Optional
from sqlalchemy.orm import Session
from . import models

async def verify_bookingreference_exist(bookingreference: str, db_session: Session) -> Optional[models.User]:
    return db_session.query(models.Booking).filter(models.Booking.bookingReference == bookingreference).first()