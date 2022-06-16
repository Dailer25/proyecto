from typing import List
from sqlalchemy.orm import Session
from . import models
from . import schema
from sqlalchemy import func
from booking import models as booking_models
from fastapi import HTTPException
from datetime import date

async def get_all_flights(db_session: Session) -> List[models.Flight]:
    flights = db_session.query(models.Flight).all()
    return flights

async def get_flights(departureAirportCode: str, arrivalAirportCode: str, departureDate: date, db_session: Session) -> List[models.Flight]:
    dac = db_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode).all()
    if not dac: 
        raise HTTPException(status_code=404, detail="Departure airport code not found")   
    aac = db_session.query(models.Flight).filter(models.Flight.arrivalAirportCode == arrivalAirportCode).all()
    if not aac: 
        raise HTTPException(status_code=404, detail="Arrival airport code not found")

    flights = db_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode, 
                                                     models.Flight.arrivalAirportCode == arrivalAirportCode,
                                                     func.date(models.Flight.departureDate) == departureDate).all()
    return flights                                 

async def get_flights_by_departureairportcode_and_departuredate(departureAirportCode: str, departureDate: date, db_session: Session) -> List[models.Flight]:
    dac = db_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode).all()
    if not dac: 
        raise HTTPException(status_code=404, detail="Departure airport code not found")

    if departureDate:
        flights = db_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode, 
                                                     func.date(models.Flight.departureDate) == departureDate).all()
    else:
        flights = dac
    
    return flights

async def create_new_flight(flight: schema.FlightCreate, db_session: Session) -> models.Flight:
    new_flight = models.Flight(**flight.dict())
    db_session.add(new_flight)
    db_session.commit()
    db_session.refresh(new_flight)

    return new_flight

async def update_flight(flight_id: int, flight: schema.FlightUpdate, db_session: Session):
    updated_flight = models.Flight(**flight.dict())
    db_session.query(models.Flight).filter(models.Flight.id == flight_id).update(
                                           {
                                               models.Flight.id: flight_id,
                                               models.Flight.departureDate: updated_flight.departureDate,
                                               models.Flight.departureAirportCode: updated_flight.departureAirportCode,
                                               models.Flight.departureAirportName: updated_flight.departureAirportName,
                                               models.Flight.departureCity: updated_flight.departureCity,
                                               models.Flight.departureLocale: updated_flight.departureLocale,
                                               models.Flight.arrivalDate: updated_flight.arrivalDate,
                                               models.Flight.arrivalAirportCode: updated_flight.arrivalAirportCode,
                                               models.Flight.arrivalAirportName: updated_flight.arrivalAirportName,
                                               models.Flight.arrivalCity: updated_flight.arrivalCity,
                                               models.Flight.arrivalLocale: updated_flight.arrivalLocale,
                                               models.Flight.ticketPrice: updated_flight.ticketPrice,
                                               models.Flight.ticketCurrency: updated_flight.ticketCurrency,
                                               models.Flight.flightNumber: updated_flight.flightNumber,
                                               models.Flight.seatCapacity: updated_flight.seatCapacity 
                                           }, synchronize_session=False)
    db_session.commit()
    return updated_flight

async def delete_flight(flight_id: int, db_session: Session):
    # NOTA: Para este método se decidió borrar también todas las reservas (bookings) 
    # del vuelo (flight)
    booking = db_session.query(booking_models.Booking).filter(booking_models.Booking.outboundFlight_id == flight_id).all()
    if booking:
        for b in booking:
            db_session.delete(b)
    db_session.commit()
    db_session.query(models.Flight).filter(models.Flight.id == flight_id).delete()
    db_session.commit()