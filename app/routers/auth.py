from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/login", response_model=schemas.User)
def login(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        db_user = crud.create_user(db, user=user)
    return db_user
