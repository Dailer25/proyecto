from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base
from core import hashing

class User(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "Table Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    namec = Column(String(255))
    correo = Column(String(255), unique=True)
    password = Column(String(255))

    booking = relationship("Booking", back_populates="customer")

    def __init__(self, namec, correo, password, *args, **kwargs):
        self.namec = namec
        self.correo = correo
        self.password = hashing.get_password_hash(password)
    
    def check_password(self, password):
        return hashing.verify_password(self.password, password)
