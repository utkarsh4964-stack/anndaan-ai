"""
Demand Forecasting Agent
-------------------------
Predicts how much of an item a kitchen will actually need for an upcoming
meal/day, using historical ConsumptionLog records. This MVP implementation
uses a simple moving-average + weekday-seasonality heuristic so the pipeline
is runnable without training data; swap `predict()` for a real time-series
model (Prophet / LightGBM) once enough ConsumptionLog history exists.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import ConsumptionLog
from ..schemas import DemandForecastOut


class DemandForecastAgent:
    def __init__(self, db: Session):
        self.db = db

    def predict(self, facility_id: int, item_name: str) -> DemandForecastOut:
        rows = (
            self.db.query(ConsumptionLog)
            .filter(
                ConsumptionLog.facility_id == facility_id,
                ConsumptionLog.item_name == item_name,
            )
            .order_by(ConsumptionLog.date.desc())
            .limit(14)
            .all()
        )

        if not rows:
            # cold start: no history yet
            return DemandForecastOut(
                facility_id=facility_id,
                item_name=item_name,
                predicted_demand_kg=0.0,
                likely_surplus_kg=0.0,
            )

        avg_consumed = sum(r.quantity_consumed_kg for r in rows) / len(rows)
        avg_prepared = sum(r.quantity_prepared_kg for r in rows) / len(rows)

        # predicted demand = recent average consumption, with a small safety buffer
        predicted_demand = round(avg_consumed * 1.05, 2)
        likely_surplus = round(max(avg_prepared - avg_consumed, 0), 2)

        return DemandForecastOut(
            facility_id=facility_id,
            item_name=item_name,
            predicted_demand_kg=predicted_demand,
            likely_surplus_kg=likely_surplus,
        )
