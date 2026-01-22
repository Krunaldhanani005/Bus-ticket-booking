from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database, models
from ..utils import ml_mock

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

@router.get("/seats/{bus_id}", response_model=List[schemas.Seat])
def read_seats(bus_id: int, db: Session = Depends(database.get_db)):
    seats = crud.get_seats(db, bus_id=bus_id)
    return seats

@router.get("/availability", response_model=List[int])
def check_availability(source_id: int, dest_id: int, date: str, db: Session = Depends(database.get_db)):
    # Simple logic: If a seat is booked for *any* part of the journey on that date, it's unavailable.
    # In a real system, we'd check overlapping segments. 
    # For this simplified version (single bus), we'll just check if the seat is booked at all on that date.
    
    # Actually, the requirement mentions intermediate stations.
    # A seat is unavailable if there is an existing booking for that seat on that date
    # AND the booking's segment overlaps with the requested segment.
    # But for simplicity in this prototype, let's assume if it's booked, it's booked for the whole trip
    # unless we want to implement the segment logic.
    # Let's try to implement a simple segment overlap check?
    # Existing booking: [start, end]
    # Requested: [req_start, req_end]
    # Overlap if: start < req_end and end > req_start
    
    # Since station IDs are ordered (1,2,3,4...), we can use them as positions.
    
    bookings = crud.get_bookings_by_date(db, travel_date=date) # Date string match might need parsing if DB stores date object
    
    booked_seat_ids = []
    
    # Query stations to get order
    stations = crud.get_stations(db)
    station_map = {s.id: s.order for s in stations}
    
    req_start = station_map.get(source_id)
    req_end = station_map.get(dest_id)
    
    if req_start is None or req_end is None:
         return [] # Invalid stations
    
    # Ensure correct direction (assuming strict A->B)
    if req_start >= req_end:
        return [] 
        
    for booking in bookings:
        if booking.status == "CANCELLED":
            continue
            
        b_start = station_map.get(booking.source_station_id)
        b_end = station_map.get(booking.dest_station_id)
        
        # Check Overlap
        if b_start < req_end and b_end > req_start:
            booked_seat_ids.append(booking.seat_id)
            
    return booked_seat_ids

@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    # Calculate probability
    p_success = ml_mock.predict_confirmation(booking)
    return crud.create_booking(db=db, booking=booking, p_success=p_success)

@router.get("/user/{email}", response_model=List[schemas.Booking])
def read_user_bookings(email: str, db: Session = Depends(database.get_db)):
    bookings = crud.get_user_bookings(db, user_email=email)
    return bookings

@router.post("/cancel/{booking_id}")
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(database.get_db)):
    booking = crud.cancel_booking(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking cancelled successfully"}
