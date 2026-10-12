"""
Smart Campus - Master Pipeline Runner
Orchestrates:
1. Ingestion (Module 1)
2. Feature Engineering (Module 2)
3. Success Scoring (Module 3)
4. AI Risk Detection (Module 4)
5. Student Segmentation (Module 5)
6. Explainable AI & Interventions (Module 6)
7. Interactive Web Dashboard Server (Module 7)
"""
import os

from module1_data_integration import DataIntegrationEngine
from module2_feature_engineering import FeatureEngineeringModule
from module3_success_scorer import SuccessScoringEngine
from module4_risk_detector import RiskDetectorEngine
from module5_segmentation import StudentSegmentationEngine
from module6_explainability import ExplainableAIEngine
from module7_dashboard import run_server


def build_student_success_platform():
    print("=" * 65)
    print("🎓 SMART CAMPUS: PREDICT, OPTIMIZE & IMPROVE SUCCESS")
    print("=" * 65)

    # Step 1: Data Ingestion (7 Streams)
    print("[1/6] Ingesting 7 campus data streams for 75 students...")
    raw_data = DataIntegrationEngine().generate_synthetic_campus_dataset(n_students=75)

    # Step 2: Feature Engineering & Preprocessing
    print("[2/6] Processing feature engineering & normalization...")
    engineered = FeatureEngineeringModule().process_dataset(raw_data)

    # Step 3, 4, 5, 6: AI Inference & Scoring Pipeline
    print("[3/6] Running AI Success Scoring, Risk Detection, & Segmentation...")
    final_student_profiles = []

    for student in engineered:
        # Module 3: Success Score
        score_info = SuccessScoringEngine.calculate_success_score(student)
        success_score = score_info["success_score"]

        # Module 4: Risk Detector
        risks = RiskDetectorEngine.evaluate_risks(student, success_score)

        # Module 5: Student Segmentation
        segmentation = StudentSegmentationEngine.assign_segment(student, success_score)

        # Module 6: Explainable AI & Interventions
        xai = ExplainableAIEngine.explain_student_profile(student, risks)

        # Combine into complete student profile
        unified_record = {
            **student,
            **score_info,
            "risks": risks,
            "segmentation": segmentation,
            "xai": xai
        }
        final_student_profiles.append(unified_record)

    print(f"[4/6] Successfully compiled {len(final_student_profiles)} student profiles.")
    print(f"[5/6] High-Risk Flags identified: {sum(1 for s in final_student_profiles if s['risks']['overall_risk_level'] == 'HIGH RISK')}")

    # Step 7: Launch Web Dashboard
    print("[6/6] Launching Module 7 Interactive Web Dashboard...")

    port = int(os.environ.get("PORT", 8000))
    run_server(final_student_profiles, port=port)

if __name__ == "__main__":
    build_student_success_platform()
