from sqlalchemy.orm import Session
from . import models, schemas
import random

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.email + "notreallyhashed"
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_stations(db: Session):
    return db.query(models.Station).order_by(models.Station.order).all()

def get_seats(db: Session, bus_id: int):
    return db.query(models.Seat).filter(models.Seat.bus_id == bus_id).all()

def get_bookings_by_date(db: Session, travel_date):
    return db.query(models.Booking).filter(models.Booking.travel_date == travel_date).all()

def get_user_bookings(db: Session, user_email: str):
    return db.query(models.Booking).filter(models.Booking.user_email == user_email).order_by(models.Booking.id.desc()).all()

def cancel_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if booking:
        booking.status = "CANCELLED"
        db.commit()
    return booking

def create_booking(db: Session, booking: schemas.BookingCreate, p_success: float):
    db_booking = models.Booking(
        user_email=booking.user_email,
        source_station_id=booking.source_station_id,
        dest_station_id=booking.dest_station_id,
        seat_id=booking.seat_id,
        booking_date=booking.travel_date, # simplified to use travel date as booking date for now if not passed
        travel_date=booking.travel_date,
        meal_choice=booking.meal_choice,
        p_success=p_success,
        status="CONFIRMED"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
