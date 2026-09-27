from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import FacilityType, SurplusStatus


class FacilityCreate(BaseModel):
    name: str
    type: FacilityType
    latitude: float
    longitude: float
    capacity_kg: float = 0
    contact: Optional[str] = None


class FacilityOut(FacilityCreate):
    id: int

    class Config:
        from_attributes = True


class ConsumptionLogCreate(BaseModel):
    facility_id: int
    item_name: str
    quantity_prepared_kg: float
    quantity_consumed_kg: float


class SurplusItemCreate(BaseModel):
    facility_id: int
    item_name: str
    quantity_kg: float
    quality_score: float = 1.0
    hours_to_expiry: Optional[float] = None


class SurplusItemOut(SurplusItemCreate):
    id: int
    status: SurplusStatus
    detected_at: datetime

    class Config:
        from_attributes = True


class MatchOut(BaseModel):
    id: int
    surplus_item_id: int
    recipient_facility_id: int
    distance_km: Optional[float]
    pickup_window_start: Optional[datetime]
    pickup_window_end: Optional[datetime]

    class Config:
        from_attributes = True


class DemandForecastOut(BaseModel):
    facility_id: int
    item_name: str
    predicted_demand_kg: float
    likely_surplus_kg: float
