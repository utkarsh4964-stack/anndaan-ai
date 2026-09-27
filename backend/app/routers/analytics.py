from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..agents.analytics import AnalyticsAgent

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return AnalyticsAgent(db).summary()
