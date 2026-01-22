from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    order = Column(Integer)  # Order determines distance/sequence

class Bus(Base):
    __tablename__ = "buses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    total_seats = Column(Integer, default=20) # Simplified

class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"))
    seat_number = Column(String) # e.g., "1A", "1B"
    is_sleeper = Column(Boolean, default=True)
    
    bus = relationship("Bus")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True) # Direct email reference for simplicity
    source_station_id = Column(Integer, ForeignKey("stations.id"))
    dest_station_id = Column(Integer, ForeignKey("stations.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    booking_date = Column(Date) # Date of booking
    travel_date = Column(Date) # Date of journey
    meal_choice = Column(String) # Veg, Non-Veg, Jain, None
    status = Column(String, default="CONFIRMED") # CONFIRMED, CANCELLED
    p_success = Column(Float, default=0.0)

    source_station = relationship("Station", foreign_keys=[source_station_id])
    dest_station = relationship("Station", foreign_keys=[dest_station_id])
    seat = relationship("Seat")
