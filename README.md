# Sleeper Bus Ticket Booking System

A web-based booking system for the Ahmedabad → Mumbai sleeper bus route, featuring intermediate stations, meal selection, and an AI-driven booking confirmation simulator.

## Features

- **User Authentication**: Simple email-based login (password-less).
- **Route Handling**: Ahmedabad → Vadodara → Surat → Vapi → Valsad → Mumbai.
- **Seat Booking**: Visual seat selection (Lower/Upper decks) with availability checks.
- **Intermediate Station Logic**: Intelligent partial route booking support.
- **Meal Selection**: Options for Veg, Non-Veg, and Jain meals.
- **AI Prediction**: Simulated booking confirmation probability based on route and preferences.
- **Booking History**: View and cancel past bookings.

## Tech Stack

- **Backend**: Python (FastAPI), SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (`bus_booking.db`)

## Project Structure

```
/app
    /routers    # API Endpoints (auth, stations, bookings)
    /utils      # Helper scripts (ml_mock.py)
    main.py     # Application Entry Point
    models.py   # Database Models
    schemas.py  # Pydantic Schemas
    crud.py     # Database Operations
    database.py # DB Connection
/static
    /css        # Stylesheets
    /js         # API Helpers
    index.html  # Login Page
    ...         # Other HTML pages
```

## How to Run

### Prerequisities
- Python 3.8+
- `pip install fastapi uvicorn sqlalchemy`

### Steps
1. Navigate to the project directory:
   ```bash
   cd "e:\Projects\My Bus Ticket Booking"
   ```
2. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open the application in your browser:
   http://localhost:8000

## API Endpoints

- `POST /auth/login`: User login
- `GET /stations/`: List all stations
- `GET /bookings/seats/{bus_id}`: Get seat configuration
- `GET /bookings/availability`: Check seat availability for date/route
- `POST /bookings/`: Create a new booking
- `GET /bookings/user/{email}`: Get user history
- `POST /bookings/cancel/{id}`: Cancel a booking

## UI/UX

- **Login**: Clean, minimalist email entry.
- **Home**: Search bus by Source/Destination and viewing history.
- **Booking**: Interactive deck layout for seat selection.
- **Confirmation**: Booking details with AI probability score.
