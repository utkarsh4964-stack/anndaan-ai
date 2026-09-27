from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..agents.demand_forecast import DemandForecastAgent

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/", response_model=schemas.DemandForecastOut)
def get_forecast(facility_id: int, item_name: str, db: Session = Depends(get_db)):
    agent = DemandForecastAgent(db)
    return agent.predict(facility_id, item_name)
