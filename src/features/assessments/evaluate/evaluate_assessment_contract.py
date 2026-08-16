from abc import ABC, abstractmethod

from src.features.assessments.evaluate.evaluate_assessment_request import (
    EvaluateAssessmentRequest,
)
from src.features.assessments.evaluate.evaluate_assessment_response import (
    EvaluateAssessmentResponse,
)


class EvaluateAssessmentContract(ABC):
    @abstractmethod
    async def evaluate(
        self, request: EvaluateAssessmentRequest
    ) -> EvaluateAssessmentResponse:
        """Evaluate the answers of an assessment and return the result.

        Args:
            request (EvaluateAssessmentRequest): Assessment data to be evaluated

        Returns:
            EvaluateAssessmentResponse: The result of the evaluation, including success status, message, and qualifications if applicable.
        """
        pass
