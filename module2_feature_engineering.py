"""
Module 2: Feature Engineering & Preprocessing
Transforms raw multi-source streams into normalized (0-1.0) feature vectors:
- Normalizes CGPA (0-10 -> 0-1)
- Penalizes backlogs
- Normalizes attendance, LMS, placement, skills, and faculty ratings
"""

from typing import List, Dict, Any

class FeatureEngineeringModule:
    @staticmethod
    def flatten_and_normalize(student: Dict[str, Any]) -> Dict[str, Any]:
        acad = student["academic"]
        att = student["attendance"]
        lms = student["lms"]
        eng = student["engagement"]
        plc = student["placement"]
        skl = student["skills"]
        fdb = student["feedback"]

        # 1. Academic Normalized (Penalize heavily for backlogs)
        norm_cgpa = min(1.0, max(0.0, acad["cgpa"] / 10.0))
        backlog_penalty = max(0.0, 1.0 - (acad["backlogs"] * 0.25))
        academic_feature = max(0.0, (norm_cgpa * 0.7 + (acad["internal_marks"] / 100.0) * 0.3) * backlog_penalty)

        # 2. Attendance Normalized
        attendance_feature = min(1.0, max(0.0, att["overall_percentage"] / 100.0))

        # 3. LMS Normalized (Capped at 25 logins/week)
        lms_login_norm = min(1.0, lms["logins_per_week"] / 25.0)
        lms_feature = (lms_login_norm * 0.4) + ((lms["assignment_completion_rate"] / 100.0) * 0.6)

        # 4. Engagement Normalized
        eng_certs = min(1.0, eng["certifications_count"] / 4.0)
        eng_hack = min(1.0, eng["hackathons_count"] / 3.0)
        engagement_feature = min(1.0, (eng_certs * 0.4) + (eng_hack * 0.4) + (eng["club_leadership"] * 0.2))

        # 5. Placement Normalized
        plc_apt = plc["aptitude_score"] / 100.0
        plc_code = plc["coding_score"] / 100.0
        plc_mock = plc["mock_interview_rating"] / 5.0
        placement_feature = (plc_apt * 0.3) + (plc_code * 0.45) + (plc_mock * 0.25)

        # 6. Skills Normalized
        skills_feature = ((skl["technical_assessment"] / 100.0) * 0.6) + ((skl["soft_skills_score"] / 100.0) * 0.4)

        # 7. Feedback Normalized
        feedback_feature = ((fdb["satisfaction_index"] / 5.0) * 0.4) + ((fdb["faculty_sentiment_score"] / 100.0) * 0.6)

        return {
            "student_id": student["student_id"],
            "name": student["name"],
            "department": student["department"],
            "year": student["year"],
            # Raw figures for reporting
            "raw_cgpa": acad["cgpa"],
            "raw_backlogs": acad["backlogs"],
            "raw_attendance": att["overall_percentage"],
            "raw_coding": plc["coding_score"],
            "raw_aptitude": plc["aptitude_score"],
            # Normalized engineered features (0.0 to 1.0)
            "f_academic": round(academic_feature, 4),
            "f_attendance": round(attendance_feature, 4),
            "f_lms": round(lms_feature, 4),
            "f_engagement": round(engagement_feature, 4),
            "f_placement": round(placement_feature, 4),
            "f_skills": round(skills_feature, 4),
            "f_feedback": round(feedback_feature, 4)
        }

    def process_dataset(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.flatten_and_normalize(s) for s in raw_data]