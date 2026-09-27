from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.post("/", response_model=schemas.FacilityOut)
def create_facility(payload: schemas.FacilityCreate, db: Session = Depends(get_db)):
    facility = models.Facility(**payload.model_dump())
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


@router.get("/", response_model=List[schemas.FacilityOut])
def list_facilities(db: Session = Depends(get_db)):
    return db.query(models.Facility).all()
