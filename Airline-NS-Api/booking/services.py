from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schema
from user import models as user_models
from . import models

#from app.user import schema as user_schema, validation as user_validation
#from app.catalog import schema as catalog_schema, validation as catalog_validation

async def get_booking_by_id(booking_id: int, db_session: Session) -> models.Booking:
    booking_info = db_session.query(models.Booking).get(booking_id)
    return booking_info

async def get_bookings_by_idflight(flight_id: int, db_session: Session) -> List[models.Booking]:
    bookings = db_session.query(models.Booking).filter(models.Booking.outboundFlight_id == flight_id).all()
    return bookings

async def get_bookings_by_status_and_customername(status: schema.BookingStatus, customername: str, db_session: Session) -> List[models.Booking]:
    if status and customername:
        user = db_session.query(user_models.User).filter(user_models.User.fullname == customername).first()
        bookings = db_session.query(models.Booking).filter(models.Booking.status == status, 
                                                           models.Booking.customer_id == user.id).all()
    elif not status and customername:
        user = db_session.query(user_models.User).filter(user_models.User.fullname == customername).first()
        bookings = db_session.query(models.Booking).filter(models.Booking.customer_id == user.id).all()
    elif status and not customername:
        bookings = db_session.query(models.Booking).filter(models.Booking.status == status).all()
    else:
        bookings = db_session.query(models.Booking).all()
    return bookings

async def create_new_booking(flight_id: int, user_id: int, booking: schema.BookingCreate, db_session: Session) -> models.Booking:
    new_booking = models.Booking(outboundFlight_id=flight_id,
                                 customer_id=user_id,
                                 **booking.dict())
    db_session.add(new_booking)
    db_session.commit()
    db_session.refresh(new_booking)
    return new_booking

async def delete_booking_by_id(booking_id: int, db_session: Session):
    db_session.query(models.Booking).filter(models.Booking.id == booking_id).delete()
    db_session.commit()
