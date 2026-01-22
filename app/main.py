from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import engine, Base, SessionLocal
from . import models
from .routers import auth, stations, bookings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sleeper Bus Booking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(stations.router)
app.include_router(bookings.router)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    # Check if stations exist
    if not db.query(models.Station).first():
        stations_data = [
            {"name": "Ahmedabad", "order": 1},
            {"name": "Vadodara", "order": 2},
            {"name": "Surat", "order": 3},
            {"name": "Vapi", "order": 4},
            {"name": "Valsad", "order": 5},
            {"name": "Mumbai", "order": 6},
        ]
        for s in stations_data:
            db.add(models.Station(**s))
        db.commit()
        
    # Check if bus exists
    if not db.query(models.Bus).first():
        bus = models.Bus(name="GJ-01-XX-1234", total_seats=20)
        db.add(bus)
        db.commit()
        db.refresh(bus)
        
        # Create Seats
        seats = []
        # 10 Lower (L), 10 Upper (U)
        for i in range(1, 11):
            seats.append(models.Seat(bus_id=bus.id, seat_number=f"L{i}", is_sleeper=True))
            seats.append(models.Seat(bus_id=bus.id, seat_number=f"U{i}", is_sleeper=True))
        
        db.add_all(seats)
        db.commit()
    
    db.close()

@app.get("/")
def read_root():
    return FileResponse('static/index.html')
