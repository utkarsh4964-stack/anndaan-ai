from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..agents.redistribution_matcher import RedistributionMatchingAgent
from ..agents.logistics_optimizer import LogisticsOptimizationAgent

router = APIRouter(prefix="/redistribution", tags=["redistribution"])
logistics_agent = LogisticsOptimizationAgent()


@router.post("/match/{surplus_item_id}", response_model=schemas.MatchOut)
def match_surplus_item(surplus_item_id: int, db: Session = Depends(get_db)):
    """Run the Redistribution Matching Agent + Logistics Agent for one surplus item."""
    item = db.query(models.SurplusItem).get(surplus_item_id)
    if not item:
        raise HTTPException(404, "surplus item not found")

    matcher = RedistributionMatchingAgent(db)
    match = matcher.find_best_recipient(item)
    if not match:
        raise HTTPException(422, "no eligible recipient found within range")

    pickup = logistics_agent.plan_pickup(match["distance_km"], item.hours_to_expiry)

    record = models.RedistributionMatch(
        surplus_item_id=item.id,
        recipient_facility_id=match["facility"].id,
        distance_km=match["distance_km"],
        pickup_window_start=pickup["pickup_window_start"],
        pickup_window_end=pickup["pickup_window_end"],
    )
    item.status = models.SurplusStatus.matched
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/matches", response_model=List[schemas.MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(models.RedistributionMatch).all()
