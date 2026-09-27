"""
Redistribution Matching Agent
-------------------------------
Given a surplus item, finds the best eligible recipient facility (NGO,
shelter, community kitchen) ranked by distance and available capacity.
"""
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.orm import Session
from ..models import Facility, FacilityType, SurplusItem

RECIPIENT_TYPES = {FacilityType.ngo, FacilityType.shelter, FacilityType.community_kitchen}


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


class RedistributionMatchingAgent:
    def __init__(self, db: Session):
        self.db = db

    def find_best_recipient(self, surplus_item: SurplusItem, max_distance_km: float = 25.0):
        source = self.db.query(Facility).get(surplus_item.facility_id)
        if source is None:
            return None

        candidates = (
            self.db.query(Facility)
            .filter(Facility.type.in_(RECIPIENT_TYPES))
            .filter(Facility.capacity_kg >= surplus_item.quantity_kg)
            .all()
        )

        ranked = []
        for c in candidates:
            dist = _haversine_km(source.latitude, source.longitude, c.latitude, c.longitude)
            if dist <= max_distance_km:
                ranked.append((dist, c))

        if not ranked:
            return None

        ranked.sort(key=lambda x: x[0])
        best_distance, best_facility = ranked[0]
        return {"facility": best_facility, "distance_km": round(best_distance, 2)}
