from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token
from typing import Any
from database import db
from user.services import authenticate

api_router = APIRouter(tags=["Auth"])

@api_router.post("/login/")
def login(db_session: Session= Depends(db.get_db_session), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = authenticate(correo=form_data.correo, password=form_data.password, db_session=db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect correo or password")
    
    return {
        "access_token": create_access_token(sub=user.correo),
        "token_type": "Bearer",
    }