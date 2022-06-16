from typing import Optional
from sqlalchemy.orm import Session
from . import models

async def verify_correo_exist(correo: str, db_session: Session) -> Optional[models.User]:
    return db_session.query(models.User).filter(models.User.correo == correo).first()

async def verify_namec_exist(namec: str, db_session: Session) -> Optional[models.User]:
    return db_session.query(models.User).filter(models.User.namec == namec).first()

async def verify_iduser_exist(user_id: int, db_session: Session) -> Optional[models.User]:
    return db_session.query(models.User).filter(models.User.id == user_id).first()