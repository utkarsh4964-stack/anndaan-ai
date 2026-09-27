from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class FacilityType(str, enum.Enum):
    kitchen = "kitchen"
    processing_unit = "processing_unit"
    ngo = "ngo"
    shelter = "shelter"
    community_kitchen = "community_kitchen"


class SurplusStatus(str, enum.Enum):
    detected = "detected"
    matched = "matched"
    in_transit = "in_transit"
    delivered = "delivered"
    expired = "expired"


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(FacilityType), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity_kg = Column(Float, default=0)  # relevant for NGOs/shelters
    contact = Column(String, nullable=True)

    surplus_items = relationship("SurplusItem", back_populates="facility")


class ConsumptionLog(Base):
    """Historical meal/production records used by the Demand Forecasting Agent."""
    __tablename__ = "consumption_logs"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    date = Column(DateTime, default=datetime.utcnow)
    item_name = Column(String, nullable=False)
    quantity_prepared_kg = Column(Float, nullable=False)
    quantity_consumed_kg = Column(Float, nullable=False)


class SurplusItem(Base):
    """A surplus/near-expiry batch flagged by the Expiry Vision Agent or logged manually."""
    __tablename__ = "surplus_items"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id"))
    item_name = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    quality_score = Column(Float, default=1.0)  # 0-1, from vision model
    hours_to_expiry = Column(Float, nullable=True)
    status = Column(Enum(SurplusStatus), default=SurplusStatus.detected)
    detected_at = Column(DateTime, default=datetime.utcnow)

    facility = relationship("Facility", back_populates="surplus_items")


class RedistributionMatch(Base):
    """Output of the Redistribution Matching Agent + Logistics Agent."""
    __tablename__ = "redistribution_matches"

    id = Column(Integer, primary_key=True, index=True)
    surplus_item_id = Column(Integer, ForeignKey("surplus_items.id"))
    recipient_facility_id = Column(Integer, ForeignKey("facilities.id"))
    distance_km = Column(Float, nullable=True)
    pickup_window_start = Column(DateTime, nullable=True)
    pickup_window_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
