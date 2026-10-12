"""
Module 4: At-Risk Predictive AI Engine
Detects:
1. Academic Risk (Risk of poor CGPA, backlogs, course failure)
2. Placement Risk (Risk of failing campus recruitment drives)
Assigns Risk Flags: High Risk, Medium Risk, Low Risk.
"""

from typing import Dict, Any

class RiskDetectorEngine:
    @staticmethod
    def evaluate_risks(features: Dict[str, Any], success_score: float) -> Dict[str, Any]:
        # --- Academic Risk Evaluation ---
        # Driven by low CGPA, active backlogs, low attendance, poor LMS assignment rate
        acad_risk_score = 0
        acad_reasons = []

        if features["raw_backlogs"] > 0:
            acad_risk_score += 40 + (features["raw_backlogs"] * 15)
            acad_reasons.append(f"{features['raw_backlogs']} Active Backlogs")
        if features["raw_cgpa"] < 6.0:
            acad_risk_score += 35
            acad_reasons.append(f"Low CGPA ({features['raw_cgpa']})")
        elif features["raw_cgpa"] < 6.8:
            acad_risk_score += 15

        if features["raw_attendance"] < 75.0:
            acad_risk_score += 25
            acad_reasons.append(f"Shortage of Attendance ({features['raw_attendance']}%)")

        if features["f_lms"] < 0.4:
            acad_risk_score += 15
            acad_reasons.append("Low LMS Activity")

        # --- Placement Risk Evaluation ---
        # Driven by coding score, aptitude, mock interview & backlogs
        placement_risk_score = 0
        placement_reasons = []

        if features["raw_coding"] < 50.0:
            placement_risk_score += 35
            placement_reasons.append(f"Low Coding Score ({features['raw_coding']}%)")
        if features["raw_aptitude"] < 50.0:
            placement_risk_score += 25
            placement_reasons.append(f"Low Aptitude Score ({features['raw_aptitude']}%)")
        if features["raw_backlogs"] > 0:
            placement_risk_score += 25
            placement_reasons.append("Backlog Ineligibility for Drives")
        if features["f_skills"] < 0.45:
            placement_risk_score += 15
            placement_reasons.append("Low Technical/Soft Skills")

        # Determine Primary Flags
        is_academic_risk = acad_risk_score >= 40
        is_placement_risk = placement_risk_score >= 40

        # Overall Campus Risk Level
        if success_score < 50.0 or acad_risk_score >= 60 or placement_risk_score >= 60:
            overall_risk = "HIGH RISK"
            badge = "danger"
        elif success_score < 68.0 or acad_risk_score >= 35 or placement_risk_score >= 35:
            overall_risk = "MEDIUM RISK"
            badge = "warning"
        else:
            overall_risk = "LOW RISK"
            badge = "success"

        return {
            "overall_risk_level": overall_risk,
            "overall_badge": badge,
            "academic_risk": {
                "flag": is_academic_risk,
                "score": min(100, acad_risk_score),
                "reasons": acad_reasons or ["Consistent Academic Progress"]
            },
            "placement_risk": {
                "flag": is_placement_risk,
                "score": min(100, placement_risk_score),
                "reasons": placement_reasons or ["Good Placement Readiness"]
            }
        }