from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(
    prefix="/stations",
    tags=["stations"]
)

@router.get("/", response_model=List[schemas.Station])
def read_stations(db: Session = Depends(database.get_db)):
    stations = crud.get_stations(db)
    return stations
