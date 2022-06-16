from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from core import hashing
from booking import models as booking_models

async def get_all_users(db_session: Session) -> List[models.User]:
    users = db_session.query(models.User).all()
    return users

async def get_user_by_id(user_id: int, db_session: Session) -> Optional[models.User]:
    user_info = db_session.query(models.User).get(user_id)
    return user_info

async def new_user_register(user_in: schema.UserCreate, db_session: Session) -> models.User:
    new_user = models.User(**user_in.dict())
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

async def delete_user_by_id(user_id: int, db_session: Session):
    
    booking = db_session.query(booking_models.Booking).filter(booking_models.Booking.customer_id == user_id).all()
    if booking:
        for b in booking:
            db_session.delete(b)

    db_session.commit()
    db_session.query(models.User).filter(models.User.id == user_id).delete()
    db_session.commit()

async def update_user(user_id: int, user: schema.UserUpdate, db_session: Session):
    updated_user = models.User(**user.dict())
    db_session.query(models.User).filter(models.User.id == user_id).update(
                                            {
                                                models.User.id: user_id,
                                                models.User.fullname: updated_user.fullname,
                                                models.User.username: updated_user.username,
                                                models.User.password: updated_user.password
                                            }, synchronize_session=False)
    db_session.commit()
    return updated_user

def authenticate(*, username: str, password: str, db_session = Session) -> Optional[models.User]:
    user = db_session.query(models.User).filter(models.User.username == username).first()

    if not user:
        return None

    if not hashing.verify_password(password, user.password):
        return None
    
    return user