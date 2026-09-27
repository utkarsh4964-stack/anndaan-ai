"""
Sustainability & Analytics Agent
-----------------------------------
Aggregates redistribution activity into the metrics institutions need for
ESG / sustainability reporting: waste prevented, meals redistributed, and
an estimated carbon-footprint saving.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import SurplusItem, RedistributionMatch, SurplusStatus

# Rough industry-average factor: kg CO2e avoided per kg of food diverted from waste
CO2E_PER_KG_FOOD = 2.5
AVG_MEAL_WEIGHT_KG = 0.4


class AnalyticsAgent:
    def __init__(self, db: Session):
        self.db = db

    def summary(self) -> dict:
        delivered_kg = (
            self.db.query(func.coalesce(func.sum(SurplusItem.quantity_kg), 0))
            .filter(SurplusItem.status == SurplusStatus.delivered)
            .scalar()
        )
        total_matches = self.db.query(func.count(RedistributionMatch.id)).scalar()

        return {
            "food_waste_prevented_kg": round(delivered_kg, 2),
            "meals_redistributed_est": round(delivered_kg / AVG_MEAL_WEIGHT_KG),
            "co2e_avoided_kg": round(delivered_kg * CO2E_PER_KG_FOOD, 2),
            "total_redistribution_matches": total_matches,
        }
