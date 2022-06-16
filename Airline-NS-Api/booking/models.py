from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from database.db import Base
from sqlalchemy.orm import relationship
from user.models import User
from catalog.models import Flight


class Booking(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "Bookings"

    id = Column(Integer, primary_key = True, autoincrement = True)
    status = Column(String(40))
    outboundFlight_id = Column(Integer, ForeignKey(Flight.id, ondelete="CASCADE"))
    paymentToken = Column(String(100), default = '')
    checkedIn = Column(Boolean, default = False)
    customer_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    createdAt = Column(DateTime, default = datetime.today())
    bookingReference = Column(String(40), unique = True)

    flight = relationship("Flight", back_populates="Booking")
    customer = relationship("User", back_populates="Booking")

