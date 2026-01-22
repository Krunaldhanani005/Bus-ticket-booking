from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class StationBase(BaseModel):
    name: str
    order: int

class Station(StationBase):
    id: int
    class Config:
        from_attributes = True

class SeatBase(BaseModel):
    seat_number: str
    is_sleeper: bool

class Seat(SeatBase):
    id: int
    bus_id: int
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    user_email: str
    source_station_id: int
    dest_station_id: int
    seat_id: int
    travel_date: date
    meal_choice: str

class Booking(BookingCreate):
    id: int
    status: str
    p_success: float
    source_station: Optional[Station] = None
    dest_station: Optional[Station] = None
    seat: Optional[Seat] = None

    class Config:
        from_attributes = True
