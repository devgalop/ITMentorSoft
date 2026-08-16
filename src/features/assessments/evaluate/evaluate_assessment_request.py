from src.features.assessments.shared.assessment import Assessment


class EvaluateAssessmentRequest:
    def __init__(self, assessment: Assessment):
        self.assessment = assessment
