"""
Module 3: Student Success Scoring Engine
Implements the Student Success Score (0-100 scale).
Combines multi-stream indicators with calibrated weights:
- Academic: 30%
- Placement: 20%
- Attendance: 15%
- Skills: 15%
- LMS: 10%
- Engagement & Feedback: 10%
"""

from typing import Dict, Any

class SuccessScoringEngine:
    WEIGHTS = {
        "f_academic": 0.30,
        "f_placement": 0.20,
        "f_attendance": 0.15,
        "f_skills": 0.15,
        "f_lms": 0.10,
        "f_engagement": 0.05,
        "f_feedback": 0.05
    }

    @classmethod
    def calculate_success_score(cls, features: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates 0-100 score and tier classification."""
        score = sum(features[key] * weight for key, weight in cls.WEIGHTS.items()) * 100.0
        score = round(max(0.0, min(100.0, score)), 1)

        # Performance Tiering
        if score >= 80.0:
            tier = "High Achiever"
            badge_color = "success"
        elif score >= 60.0:
            tier = "Good Standing"
            badge_color = "primary"
        elif score >= 45.0:
            tier = "Moderate / At-Risk Warning"
            badge_color = "warning"
        else:
            tier = "Critical Support Required"
            badge_color = "danger"

        return {
            "success_score": score,
            "performance_tier": tier,
            "badge_color": badge_color,
            "score_breakdown": {
                "academic_points": round(features["f_academic"] * cls.WEIGHTS["f_academic"] * 100, 1),
                "placement_points": round(features["f_placement"] * cls.WEIGHTS["f_placement"] * 100, 1),
                "attendance_points": round(features["f_attendance"] * cls.WEIGHTS["f_attendance"] * 100, 1),
                "skills_points": round(features["f_skills"] * cls.WEIGHTS["f_skills"] * 100, 1),
                "lms_points": round(features["f_lms"] * cls.WEIGHTS["f_lms"] * 100, 1),
                "engagement_points": round(features["f_engagement"] * cls.WEIGHTS["f_engagement"] * 100, 1),
                "feedback_points": round(features["f_feedback"] * cls.WEIGHTS["f_feedback"] * 100, 1),
            }
        }