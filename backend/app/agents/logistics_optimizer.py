"""
Logistics Optimization Agent
-------------------------------
Turns a matched (surplus item -> recipient) pair into a concrete pickup
window, sized to the item's remaining shelf life and travel distance.
Swap `plan_pickup()` for OR-Tools/mapping-API based multi-stop routing
once you're batching multiple pickups per vehicle.
"""
from datetime import datetime, timedelta

AVERAGE_SPEED_KMPH = 25  # urban logistics assumption


class LogisticsOptimizationAgent:
    def plan_pickup(self, distance_km: float, hours_to_expiry: float | None):
        travel_hours = distance_km / AVERAGE_SPEED_KMPH
        now = datetime.utcnow()

        start = now + timedelta(minutes=15)  # prep buffer
        end = start + timedelta(hours=max(travel_hours * 1.5, 0.5))

        if hours_to_expiry is not None:
            hard_deadline = now + timedelta(hours=hours_to_expiry)
            if end > hard_deadline:
                end = hard_deadline

        return {"pickup_window_start": start, "pickup_window_end": end}
