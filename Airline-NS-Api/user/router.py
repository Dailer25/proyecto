from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse
from core import security
from . import validation
from database import db
from . import schema
from . import services

api_router = APIRouter(tags = ['User'])


@api_router.get('/User/{user_id}', response_model = schema.User)
async def get_user_by_id(user_id: int, db_session: Session = Depends(db.get_db_session)):
    user_info = await services.get_user_by_id(user_id, db_session)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Non-existent user")
    return user_info

@api_router.get('/User/', response_model = List[schema.User])
async def get_all_users(db_session: Session = Depends(db.get_db_session)):
    return await services.get_all_users(db_session)

@api_router.post('/User/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user_registration(user_in: schema.UserCreate, db_session: Session = Depends(db.get_db_session)):
    existingcorreo = await validation.verify_correo_exist(user_in.correo, db_session)
    if existingcorreo:
        raise HTTPException(status_code=400, detail="The user with this correo already exists in the system.")
    new_user = await services.new_user_register(user_in, db_session)
    return new_user

@api_router.put('/User/{user_id}', status_code = status.HTTP_201_CREATED)
async def update_user(user_id: int, user_in: schema.UserUpdate, db_session: Session = Depends(db.get_db_session),
                      current_user: schema.User = Depends(security.get_current_user)):
    existinguser = await services.get_user_by_id(user_id, db_session)
    if not existinguser:
        raise HTTPException(status_code=404, detail = "Non-existent user")
    existingcorreo = await validation.verify_correo_exist(user_in.correo, db_session)
    if existingcorreo:
        raise HTTPException(status_code=400, detail="The user with this correo already exists in the system.")
    new_user = await services.update_user(user_id, user_in, db_session)
    return new_user

@api_router.delete('/user/{user_id}', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def delete_user_by_id(user_id: int, db_session: Session = Depends(db.get_db_session),
                            current_user: schema.User = Depends(security.get_current_user)):
    existinguser = await services.get_user_by_id(user_id, db_session)
    if not existinguser:
        raise HTTPException(status_code=404, detail = "Non-existent user")
    deleted_user = await services.delete_user_by_id(user_id, db_session)
    return "THE USER AND ALL HIS BOOKINGS HAVE BEEN SUCCESSFULLY DELETED."