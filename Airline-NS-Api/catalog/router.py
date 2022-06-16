from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import PlainTextResponse
from typing import List, Optional
from core import security
from datetime import date
from database import db
from . import services
from . import validation
from . import schema
from user import schema as user_schema

api_router = APIRouter(tags = ["Catalog"])

@api_router.get("/catalog/all", response_model = List[schema.Flight])
async def get_all_flights(db_session: Session = Depends(db.get_db_session)):
    return await services.get_all_flights(db_session)

@api_router.get("/catalog/", response_model=List[schema.Flight])
async def get_flights(departureAirportCode: str, arrivalAirportCode: str, departureDate: date, db_session: Session = Depends(db.get_db_session)):
    flights = await services.get_flights(departureAirportCode,arrivalAirportCode,departureDate,db_session)
    if not flights:
        raise HTTPException(status_code=404, detail="flight(s) not found")

    return flights

@api_router.get("/catalog/{airportName}", response_model=List[schema.Flight])
async def get_flights(departureAirportName: str, arrivalAirportName: str, departureDate: str, db_session: Session = Depends(db.get_db_session)):
    flights = await services.get_flights(departureAirportName,arrivalAirportName,departureDate,db_session)
    if not flights:
        raise HTTPException(status_code=404, detail="flight(s) not found")

    return flights

@api_router.get("/catalog/{airportCode}", response_model=List[schema.Flight])
async def get_flights_by_airportcode_and_departuredate(airportCode: str, departureDate: Optional[date] = None, db_session: Session = Depends(db.get_db_session)):
    flights = await services.get_flights_by_departureairportcode_and_departuredate(airportCode,departureDate,db_session)
    if not flights:
        raise HTTPException(status_code=404, detail="flight(s) not found")

    return flights

@api_router.post("/catalog/", status_code = status.HTTP_201_CREATED, response_model=schema.Flight)
async def create_flight(flight_in: schema.FlightCreate, db_session: Session = Depends(db.get_db_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    new_flight = await services.create_new_flight(flight_in, db_session = db_session)
    return new_flight

@api_router.put('/catalog/{id}', status_code = status.HTTP_201_CREATED)
async def update_flight(id: int, flight: schema.FlightUpdate, db_session: Session = Depends(db.get_db_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    existingflight = await validation.verify_flight_exist(id, db_session)
    if not existingflight:
        raise HTTPException(status_code=404, detail="Non-existent flight")
    
    new_flight = await services.update_flight(id, flight, db_session)
    return new_flight

@api_router.delete("/catalog/{id}", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def delete_flight(id: int, db_session: Session = Depends(db.get_db_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    existingflight = await validation.verify_flight_exist(id, db_session)
    if not existingflight:
        raise HTTPException(status_code=404, detail="Non-existent flight")
    await services.delete_flight(id, db_session)

    return "THE FLIGHT AND ALL HIS BOOKINGS HAVE BEEN SUCCESSFULLY DELETED."