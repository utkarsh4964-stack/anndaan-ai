from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..agents.expiry_detection import ExpiryDetectionAgent

router = APIRouter(prefix="/surplus", tags=["surplus"])
expiry_agent = ExpiryDetectionAgent()


@router.post("/", response_model=schemas.SurplusItemOut)
def log_surplus(payload: schemas.SurplusItemCreate, db: Session = Depends(get_db)):
    """Log a surplus/near-expiry batch (manual entry or vision-agent callback)."""
    item = models.SurplusItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/", response_model=List[schemas.SurplusItemOut])
def list_surplus(db: Session = Depends(get_db)):
    return db.query(models.SurplusItem).all()


@router.post("/{item_id}/assess")
def assess_item(item_id: int, category: str = "cooked_curry", db: Session = Depends(get_db)):
    """Run the Expiry Vision Agent's heuristic against a logged item."""
    item = db.query(models.SurplusItem).get(item_id)
    if not item:
        raise HTTPException(404, "surplus item not found")

    result = expiry_agent.assess(item.item_name, category=category)
    item.quality_score = result["quality_score"]
    item.hours_to_expiry = result["hours_to_expiry"]
    db.commit()
    db.refresh(item)
    return item
