"""Driver Safety Scoring Module.

This module implements a rules-based safety scoring system for trips.
It analyzes trip events and sign detections to generate:
- Overall safety score (0-100)
- Risk level classification
- Personalized driving recommendations

Phase 2: Rules-based scoring (no ML model required)
Future: Can be replaced with XGBoost/LightGBM trained model
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from ml.sign_classes import SPEED_LIMIT_CLASSES, get_speed_limit_value


@dataclass
class SafetyScore:
    """Result of safety scoring for a trip."""
    score: int  # 0-100
    risk_level: str  # "low", "medium", "high"
    grade: str  # "A", "B", "C", "D", "F"
    issues: list[str]
    recommendations: list[str]
    breakdown: dict[str, float]  # Score breakdown by category


class DriverScorer:
    """
    Rules-based driver safety scorer.
    
    Scoring formula:
    - Base score: 100
    - Deductions per event type (normalized by distance)
    - Bonus for clean driving stretches
    """
    
    # Event penalties (points deducted per event per 100km)
    EVENT_PENALTIES = {
        "hard_brake": 3.0,
        "harsh_accel": 2.0,
        "overspeed": 4.0,
        "unsafe_curve": 3.5,
    }
    
    # Overspeed severity penalties (points per 1 km/h above limit)
    OVERSPEED_PENALTY_PER_KMH = 0.5
    
    # Risk level thresholds
    RISK_THRESHOLDS = {
        "low": 80,      # Score >= 80
        "medium": 60,   # Score >= 60
        "high": 0,      # Score < 60
    }
    
    # Grade thresholds
    GRADE_THRESHOLDS = {
        "A": 90,
        "B": 80,
        "C": 70,
        "D": 60,
        "F": 0,
    }
    
    def __init__(self):
        """Initialize the scorer."""
        pass
    
    def score_trip(
        self,
        trip_data: dict,
        events: list[dict],
        sign_detections: list[dict],
    ) -> SafetyScore:
        """
        Calculate safety score for a trip.
        
        Args:
            trip_data: Dict with trip info (distance_m, duration_seconds, etc.)
            events: List of TripEvent dicts
            sign_detections: List of SignDetection dicts
            
        Returns:
            SafetyScore with score, risk level, and recommendations
        """
        # Get trip distance in km (default to 1km to avoid division by zero)
        distance_km = max((trip_data.get("distance_m") or 0) / 1000, 1.0)
        duration_min = max((trip_data.get("duration_seconds") or 0) / 60, 1.0)
        
        # Initialize scoring
        base_score = 100.0
        breakdown = {
            "base": 100.0,
            "events": 0.0,
            "overspeed": 0.0,
            "sign_compliance": 0.0,
        }
        issues = []
        
        # Count events by type
        event_counts = {}
        max_overspeed_kmh = 0.0
        
        for event in events:
            event_type = event.get("event_type", "unknown")
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Track max overspeed
            if event_type == "overspeed":
                speed_ms = event.get("speed_m_s") or 0
                speed_kmh = speed_ms * 3.6
                # Estimate overspeed amount (assume 50 km/h default limit if unknown)
                overspeed_amount = max(0, speed_kmh - 50)
                max_overspeed_kmh = max(max_overspeed_kmh, overspeed_amount)
        
        # Calculate event-based deductions
        event_deduction = 0.0
        for event_type, count in event_counts.items():
            penalty = self.EVENT_PENALTIES.get(event_type, 2.0)
            # Normalize by distance (per 100km)
            normalized_count = (count / distance_km) * 100
            deduction = normalized_count * penalty
            event_deduction += deduction
            
            # Track issues
            if count > 0:
                if event_type == "hard_brake":
                    issues.append(f"Hard braking: {count} times")
                elif event_type == "harsh_accel":
                    issues.append(f"Harsh acceleration: {count} times")
                elif event_type == "overspeed":
                    issues.append(f"Over speed limit: {count} times")
                elif event_type == "unsafe_curve":
                    issues.append(f"Unsafe cornering: {count} times")
        
        breakdown["events"] = -min(event_deduction, 40)  # Cap at 40 points
        
        # Calculate overspeed severity deduction
        overspeed_deduction = max_overspeed_kmh * self.OVERSPEED_PENALTY_PER_KMH
        breakdown["overspeed"] = -min(overspeed_deduction, 20)  # Cap at 20 points
        
        if max_overspeed_kmh > 10:
            issues.append(f"Max speed exceeded limit by {max_overspeed_kmh:.0f} km/h")
        
        # Analyze sign detection compliance (if available)
        sign_compliance_bonus = 0.0
        detected_limits = []
        
        for detection in sign_detections:
            sign_class = detection.get("sign_class", "")
            confidence = detection.get("confidence", 0)
            
            # Extract class ID from sign_class string if it's like "speed_limit_60"
            if "speed_limit_" in sign_class:
                try:
                    limit = int(sign_class.split("_")[-1])
                    detected_limits.append(limit)
                except ValueError:
                    pass
        
        if detected_limits:
            # Bonus for having speed limit context
            sign_compliance_bonus = 5.0
            breakdown["sign_compliance"] = sign_compliance_bonus
        
        # Calculate final score
        final_score = base_score + breakdown["events"] + breakdown["overspeed"] + breakdown["sign_compliance"]
        final_score = max(0, min(100, final_score))  # Clamp to 0-100
        
        # Determine risk level
        risk_level = "high"
        for level, threshold in sorted(self.RISK_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if final_score >= threshold:
                risk_level = level
                break
        
        # Determine grade
        grade = "F"
        for g, threshold in sorted(self.GRADE_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
            if final_score >= threshold:
                grade = g
                break
        
        # Generate recommendations
        recommendations = self._generate_recommendations(event_counts, max_overspeed_kmh, distance_km)
        
        return SafetyScore(
            score=int(round(final_score)),
            risk_level=risk_level,
            grade=grade,
            issues=issues,
            recommendations=recommendations,
            breakdown={k: round(v, 1) for k, v in breakdown.items()},
        )
    
    def _generate_recommendations(
        self,
        event_counts: dict,
        max_overspeed_kmh: float,
        distance_km: float,
    ) -> list[str]:
        """Generate personalized driving recommendations."""
        recommendations = []
        
        # Hard braking recommendations
        hard_brakes = event_counts.get("hard_brake", 0)
        if hard_brakes > 0:
            rate = (hard_brakes / distance_km) * 100
            if rate > 5:
                recommendations.append(
                    "🚗 Maintain a larger following distance to avoid hard braking. "
                    "Try to anticipate stops 3-4 seconds ahead."
                )
            elif rate > 2:
                recommendations.append(
                    "💡 Look further ahead to anticipate traffic slowdowns and brake more gradually."
                )
        
        # Acceleration recommendations
        harsh_accels = event_counts.get("harsh_accel", 0)
        if harsh_accels > 0:
            rate = (harsh_accels / distance_km) * 100
            if rate > 3:
                recommendations.append(
                    "⚡ Smooth acceleration saves fuel and reduces wear. "
                    "Try to take 5+ seconds to reach cruising speed."
                )
        
        # Overspeed recommendations
        overspeeds = event_counts.get("overspeed", 0)
        if overspeeds > 0 or max_overspeed_kmh > 5:
            if max_overspeed_kmh > 20:
                recommendations.append(
                    "🚨 Significantly exceeding speed limits is dangerous. "
                    "Use cruise control to maintain safe speeds."
                )
            else:
                recommendations.append(
                    "⚠️ Watch your speed after passing speed limit signs. "
                    "It takes time to adjust - start slowing early."
                )
        
        # Curve recommendations
        unsafe_curves = event_counts.get("unsafe_curve", 0)
        if unsafe_curves > 0:
            recommendations.append(
                "🔄 Slow down before entering curves, not during. "
                "Reduce speed to a comfortable level before the turn."
            )
        
        # Perfect driving bonus
        if not recommendations:
            recommendations.append(
                "🌟 Excellent driving! Keep up the safe habits. "
                "Your smooth driving style is both safe and fuel-efficient."
            )
        
        return recommendations[:3]  # Max 3 recommendations


# Singleton instance
_scorer: Optional[DriverScorer] = None


def get_scorer() -> DriverScorer:
    """Get the singleton driver scorer instance."""
    global _scorer
    if _scorer is None:
        _scorer = DriverScorer()
    return _scorer


def score_trip_data(trip_data: dict, events: list[dict], sign_detections: list[dict]) -> dict:
    """
    Convenience function to score a trip and return as dict.
    
    Args:
        trip_data: Trip info dict
        events: List of event dicts
        sign_detections: List of detection dicts
        
    Returns:
        Dict with score, risk_level, grade, issues, recommendations, breakdown
    """
    scorer = get_scorer()
    result = scorer.score_trip(trip_data, events, sign_detections)
    
    return {
        "score": result.score,
        "risk_level": result.risk_level,
        "grade": result.grade,
        "issues": result.issues,
        "recommendations": result.recommendations,
        "breakdown": result.breakdown,
    }
