from typing import Optional
from sqlalchemy.orm import Session
from . import models

async def verify_flight_exist(flight_id: int, db_session: Session) -> Optional[models.Flight]:
    return db_session.query(models.Flight).filter(models.Flight.id == flight_id).first()