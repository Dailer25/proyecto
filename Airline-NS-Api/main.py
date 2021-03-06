from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from catalog import router as flight_router
from booking import router as booking_router
from database import models
from user import router as user_router
from auth import router as auth_router

app = FastAPI(title = "Airline North South", version = "0.0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router.api_router)
app.include_router(user_router.api_router)
app.include_router(flight_router.api_router)
app.include_router(booking_router.api_router)
