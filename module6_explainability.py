"""
Module 6: Explainable AI (XAI) & Score Driver Analysis (Bonus Feature)
Decomposes Student Success Scores into:
- Top Positive Drivers (Strengths boosting the score)
- Top Negative Drivers (Vulnerabilities pulling the score down)
- Prescriptive Recommendations for Faculty & Advisors
"""

from typing import Dict, Any, List

class ExplainableAIEngine:
    @staticmethod
    def explain_student_profile(features: Dict[str, Any], risks: Dict[str, Any]) -> Dict[str, Any]:
        drivers_positive = []
        drivers_negative = []

        # 1. Academic Driver
        if features["raw_cgpa"] >= 8.0:
            drivers_positive.append(f"Exemplary CGPA of {features['raw_cgpa']} (+25 pts)")
        elif features["raw_cgpa"] < 6.5:
            drivers_negative.append(f"Sub-par CGPA of {features['raw_cgpa']} (-20 pts)")

        if features["raw_backlogs"] > 0:
            drivers_negative.append(f"Active Backlogs: {features['raw_backlogs']} subjects (-30 pts)")

        # 2. Attendance Driver
        if features["raw_attendance"] >= 85.0:
            drivers_positive.append(f"High Attendance Consistency: {features['raw_attendance']}% (+12 pts)")
        elif features["raw_attendance"] < 75.0:
            drivers_negative.append(f"Attendance Shortage below 75%: {features['raw_attendance']}% (-18 pts)")

        # 3. Placement Readiness Driver
        if features["raw_coding"] >= 75.0:
            drivers_positive.append(f"Strong Coding Assessment: {features['raw_coding']}% (+18 pts)")
        elif features["raw_coding"] < 50.0:
            drivers_negative.append(f"Weak Coding Proficiency: {features['raw_coding']}% (-15 pts)")

        # 4. Engagement & LMS
        if features["f_engagement"] > 0.6:
            drivers_positive.append("Active in Hackathons, Certifications & Clubs (+10 pts)")
        elif features["f_engagement"] < 0.2:
            drivers_negative.append("Minimal Extracurricular / Hackathon Engagement (-8 pts)")

        if features["f_lms"] < 0.35:
            drivers_negative.append("Infrequent LMS Logins & Assignment Delays (-10 pts)")

        # Generate Actionable Prescriptive Advice for Advisors
        prescriptions = []
        if risks["academic_risk"]["flag"]:
            prescriptions.append("Assign 1-on-1 Faculty Subject Advisor for remedial coursework.")
        if risks["placement_risk"]["flag"]:
            prescriptions.append("Schedule 2 mandatory sessions on Data Structures and Aptitude practice.")
        if features["raw_attendance"] < 75.0:
            prescriptions.append("Send proactive automated attendance warning to student & mentor.")
        if not prescriptions:
            prescriptions.append("Maintain current trajectory; encourage participation in national hackathons.")

        return {
            "top_positive_drivers": drivers_positive[:3] or ["Stable foundational performance"],
            "top_negative_drivers": drivers_negative[:3] or ["No critical risk factors identified"],
            "recommended_interventions": prescriptions
        }