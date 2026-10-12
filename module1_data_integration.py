"""
Module 1: Data Integration & Ingestion Engine
Integrates 7 institutional data streams:
1. Academic (CGPA, marks, backlogs, subject scores)
2. Attendance (Overall %, subject-wise attendance)
3. LMS (Login frequency, assignment completion rate)
4. Engagement (Clubs, hackathons, certifications, events)
5. Placement (Aptitude score, coding test score, mock interview ratings)
6. Skills (Technical assessment, soft skills ratings)
7. Feedback (Student satisfaction score, faculty feedback sentiment)
"""

import json
import random
from typing import List, Dict, Any

class DataIntegrationEngine:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.departments = ["Computer Science", "Information Tech", "Data Science", "Electronics"]
        self.years = [2, 3, 4]

    def generate_synthetic_campus_dataset(self, n_students: int = 60) -> List[Dict[str, Any]]:
        """Synthesizes realistic, correlated campus data across all 7 streams."""
        dataset = []

        for i in range(1, n_students + 1):
            student_id = f"STU{1000 + i}"
            name = f"Student {i}"
            dept = random.choice(self.departments)
            year = random.choice(self.years)

            # Baseline latent student capability (-1.0 to 1.0)
            capability = random.uniform(-1.0, 1.0)

            # 1. Academic Stream
            cgpa = round(min(10.0, max(4.0, 7.5 + capability * 1.8 + random.uniform(-0.4, 0.4))), 2)
            backlogs = 0 if cgpa >= 7.5 else (random.randint(0, 1) if cgpa >= 6.0 else random.randint(1, 4))
            internal_marks = round(min(100.0, max(40.0, cgpa * 9.5 + random.uniform(-3, 3))), 1)

            # 2. Attendance Stream
            attendance_overall = round(min(100.0, max(45.0, 78.0 + capability * 15.0 + random.uniform(-8, 8))), 1)
            subject_attendance_min = round(max(30.0, attendance_overall - random.uniform(5, 20)), 1)

            # 3. LMS Stream
            lms_logins_per_week = max(1, int(14 + capability * 8 + random.uniform(-4, 4)))
            lms_assignment_completion_rate = round(min(100.0, max(30.0, 80.0 + capability * 16.0 + random.uniform(-6, 6))), 1)

            # 4. Engagement Stream
            certifications_count = max(0, int(2 + capability * 2 + random.uniform(-1, 2)))
            hackathons_participated = max(0, int(1.5 + capability * 1.5 + random.uniform(-1, 1)))
            club_leadership = 1 if (capability > 0.3 and random.random() > 0.5) else 0

            # 5. Placement Readiness Stream
            # Some students have high CGPA but weak coding/mock scores
            placement_affinity = capability + random.uniform(-0.6, 0.6)
            aptitude_score = round(min(100.0, max(30.0, 70.0 + placement_affinity * 20.0)), 1)
            coding_score = round(min(100.0, max(25.0, 68.0 + placement_affinity * 24.0)), 1)
            mock_interview_rating = round(min(5.0, max(1.0, 3.2 + placement_affinity * 1.4)), 1)

            # 6. Skills Assessment Stream
            technical_assessment = round(min(100.0, max(35.0, (coding_score * 0.6) + (cgpa * 4.0))), 1)
            soft_skills_score = round(min(100.0, max(40.0, 72.0 + capability * 14.0 + random.uniform(-10, 10))), 1)

            # 7. Student & Faculty Feedback Stream
            satisfaction_index = round(min(5.0, max(1.0, 3.8 + random.uniform(-0.8, 0.8))), 1)
            faculty_sentiment_score = round(min(100.0, max(40.0, 70.0 + (attendance_overall * 0.2) + (cgpa * 1.5) + random.uniform(-5, 5))), 1)

            student_record = {
                "student_id": student_id,
                "name": name,
                "department": dept,
                "year": year,
                # Stream 1: Academic
                "academic": {
                    "cgpa": cgpa,
                    "backlogs": backlogs,
                    "internal_marks": internal_marks
                },
                # Stream 2: Attendance
                "attendance": {
                    "overall_percentage": attendance_overall,
                    "subject_min_percentage": subject_attendance_min
                },
                # Stream 3: LMS
                "lms": {
                    "logins_per_week": lms_logins_per_week,
                    "assignment_completion_rate": lms_assignment_completion_rate
                },
                # Stream 4: Engagement
                "engagement": {
                    "certifications_count": certifications_count,
                    "hackathons_count": hackathons_participated,
                    "club_leadership": club_leadership
                },
                # Stream 5: Placement
                "placement": {
                    "aptitude_score": aptitude_score,
                    "coding_score": coding_score,
                    "mock_interview_rating": mock_interview_rating
                },
                # Stream 6: Skills
                "skills": {
                    "technical_assessment": technical_assessment,
                    "soft_skills_score": soft_skills_score
                },
                # Stream 7: Feedback
                "feedback": {
                    "satisfaction_index": satisfaction_index,
                    "faculty_sentiment_score": faculty_sentiment_score
                }
            }
            dataset.append(student_record)

        return dataset

if __name__ == "__main__":
    engine = DataIntegrationEngine()
    data = engine.generate_synthetic_campus_dataset(5)
    print(f"Generated {len(data)} sample records successfully.")
    print(json.dumps(data[0], indent=2))