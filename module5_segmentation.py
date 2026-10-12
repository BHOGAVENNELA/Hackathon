"""
Module 5: Student Segmentation Engine (Bonus Feature)
Groups students into actionable institutional cohorts:
1. High Academic, Low Placement Readiness (Need mock & coding bootcamps)
2. High Potential, Disengaged (High aptitude/coding, low attendance/LMS)
3. Placement Star, Academic Vulnerable (Strong hands-on skills, struggling with theory)
4. Critical Support Required (Low across academic, attendance, placement)
5. All-Round Achievers (Candidates for leadership & peer tutoring)
"""

from typing import Dict, Any

class StudentSegmentationEngine:
    @staticmethod
    def assign_segment(features: Dict[str, Any], success_score: float) -> Dict[str, Any]:
        acad_high = features["raw_cgpa"] >= 7.5 and features["raw_backlogs"] == 0
        acad_low = features["raw_cgpa"] < 6.5 or features["raw_backlogs"] > 0
        placement_high = features["raw_coding"] >= 70.0 and features["raw_aptitude"] >= 65.0
        placement_low = features["raw_coding"] < 52.0 or features["raw_aptitude"] < 52.0
        att_low = features["raw_attendance"] < 72.0

        if acad_high and placement_low:
            segment_name = "High Academic, Low Placement Readiness"
            action = "Enroll in ByteXL Coding Accelerator & Mock Interview Bootcamps"
            tag_color = "#3b82f6"  # Blue
        elif placement_high and att_low:
            segment_name = "High Potential, Disengaged"
            action = "Faculty Mentor Counseling to resolve attendance/engagement blockers"
            tag_color = "#8b5cf6"  # Purple
        elif placement_high and acad_low:
            segment_name = "Skilled Practitioner, Academic Risk"
            action = "Remedial subject tutoring to clear backlogs before placements"
            tag_color = "#f59e0b"  # Amber
        elif acad_low and placement_low:
            segment_name = "Critical Multi-Factor Support Required"
            action = "Urgent Academic & Dean Intervention with Parent-Teacher consultation"
            tag_color = "#ef4444"  # Red
        elif acad_high and placement_high:
            segment_name = "All-Round Star Achiever"
            action = "Recommend for Top-Tier Dream Companies & Peer-Mentorship roles"
            tag_color = "#10b981"  # Emerald
        else:
            segment_name = "Steady Performer"
            action = "Standard career development and monthly progress tracking"
            tag_color = "#64748b"  # Slate

        return {
            "segment_name": segment_name,
            "targeted_action": action,
            "segment_color": tag_color
        }