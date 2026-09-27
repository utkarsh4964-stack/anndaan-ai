"""
Quality & Expiry Vision Agent
-------------------------------
In production this agent runs a computer-vision freshness classifier
(e.g. a fine-tuned YOLOv8/CNN) over camera or photo feeds from kitchen
storage, plus IoT temperature/humidity readings, and outputs a quality
score (0-1) and estimated hours-to-expiry per item.

This MVP stub exposes the same interface with a deterministic heuristic
so the rest of the pipeline (matching, logistics, analytics) can be built
and demoed before the real model is trained. Replace `assess()` with a
call to your model inference service.
"""
from typing import Optional


class ExpiryDetectionAgent:
    # Rough shelf-life priors (hours) per broad item category, for the heuristic fallback
    DEFAULT_SHELF_LIFE_HOURS = {
        "cooked_grain": 6,
        "cooked_curry": 8,
        "raw_vegetable": 48,
        "dairy": 24,
        "bakery": 36,
    }

    def assess(
        self,
        item_name: str,
        category: str = "cooked_curry",
        sensor_temp_c: Optional[float] = None,
        image_freshness_hint: Optional[float] = None,
    ) -> dict:
        """
        Returns {"quality_score": float 0-1, "hours_to_expiry": float}

        image_freshness_hint: if you already have a vision-model score (0-1),
        pass it through here; otherwise the heuristic below is used.
        """
        base_hours = self.DEFAULT_SHELF_LIFE_HOURS.get(category, 12)

        # warmer storage accelerates spoilage
        if sensor_temp_c is not None and sensor_temp_c > 25:
            base_hours *= 0.6

        quality_score = image_freshness_hint if image_freshness_hint is not None else 0.8

        return {
            "quality_score": round(quality_score, 2),
            "hours_to_expiry": round(base_hours * quality_score, 1),
        }
