import logging
import os
from collections import defaultdict
from dotenv import load_dotenv

from src.features.assessments.shared.assessment import Assessment
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.qualifier_service import (
    BatchQualificationError,
    BatchQualifierPrompt,
    QualifierPrompt,
    QualifierResult,
    QualifierService,
    TopicResult,
)
from src.features.assessments.shared.questions_repository import QuestionRepository

logger = logging.getLogger(__name__)

EVALUATION_MODE = "normal"


def _validate_chunk_size(raw_value: str | None) -> int:
    """Validate and return the chunk size from an environment variable value.

    Args:
        raw_value: The raw string value from the environment variable, or None.

    Returns:
        The validated chunk size as a positive integer.

    Raises:
        ValueError: If the value is not a positive integer.
    """
    if raw_value is None:
        return 10
    try:
        value = int(raw_value)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise ValueError(
            f"ASSESSMENT_QUALIFICATION_CHUNK_SIZE must be a positive integer, got: {raw_value}"
        )


load_dotenv()
_raw_chunk_size = os.getenv("ASSESSMENT_QUALIFICATION_CHUNK_SIZE")
ASSESSMENT_QUALIFICATION_CHUNK_SIZE = _validate_chunk_size(_raw_chunk_size)


class EvaluateAssessmentService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        qualifier_service: QualifierService,
        question_repository: QuestionRepository,
        chunk_size: int | None = None,
    ):
        self.assessment_repository = assessment_repository
        self.qualifier_service = qualifier_service
        self.question_repository = question_repository
        self.chunk_size = (
            chunk_size
            if chunk_size is not None
            else ASSESSMENT_QUALIFICATION_CHUNK_SIZE
        )

    async def evaluate_answers(self, assessment: Assessment):
        evaluation_results: list[QualifierResult] = await self.qualify_assessment(
            assessment
        )
        await self.save_assessment_results(evaluation_results)
        topic_results: list[TopicResult] = self.get_knowledge_profile(
            assessment.user_id, evaluation_results
        )
        await self.save_knowledge_profile(topic_results)

    async def qualify_assessment(self, assessment: Assessment) -> list[QualifierResult]:
        """Send the assessment answers to the qualifier service for evaluation.

        Uses batch qualification with chunking. Falls back to per-item qualify
        if a batch call fails.

        Args:
            assessment (Assessment): The assessment containing the answers to be evaluated.

        Returns:
            list[QualifierResult]: A list of results from the qualifier service.
        """
        evaluation_results: list[QualifierResult] = []

        # Pre-fetch all rubrics in a single query
        question_ids = [answer.question_id for answer in assessment.answers]
        if not question_ids:
            return evaluation_results

        rubrics_dict = await self.question_repository.get_question_rubrics_bulk(
            question_ids
        )

        # Build (answer, rubric) pairs, skipping answers without rubrics
        pairs = [
            (answer, rubrics_dict[answer.question_id])
            for answer in assessment.answers
            if answer.question_id in rubrics_dict
        ]

        # Chunk the pairs
        chunks = [
            pairs[i : i + self.chunk_size]
            for i in range(0, len(pairs), self.chunk_size)
        ]

        # Process each chunk
        for chunk in chunks:
            chunk_rubrics = [rubric for _, rubric in chunk]
            chunk_answers = [answer for answer, _ in chunk]

            try:
                batch_prompt = BatchQualifierPrompt(
                    rubrics=chunk_rubrics,
                    answers=chunk_answers,
                    qualifier_mode=EVALUATION_MODE,
                    user_id=assessment.user_id,
                    assessment_id=assessment.assessment_id,
                )
                batch_results = await self.qualifier_service.qualify_batch(batch_prompt)
                evaluation_results.extend(batch_results)
            except BatchQualificationError:
                logger.warning(
                    "Batch qualification failed for chunk of %d answers, "
                    "falling back to per-item qualify",
                    len(chunk_answers),
                )
                for answer, rubric in chunk:
                    evaluation_results.append(
                        await self.qualifier_service.qualify(
                            QualifierPrompt(
                                rubric=rubric,
                                qualifier_mode=EVALUATION_MODE,
                                user_id=assessment.user_id,
                                user_answer=answer.answer,
                                assessment_id=assessment.assessment_id,
                                answer_id=answer.answer_id,
                            )
                        )
                    )

        return evaluation_results

    async def save_assessment_results(self, results: list[QualifierResult]):
        """Save the results of the assessment evaluation to the assessment repository.

        Args:
            results (list[QualifierResult]): A list of results from the qualifier service.
        """
        for result in results:
            await self.assessment_repository.save_assessment_qualification(result)

    def get_knowledge_profile(
        self, user_id: str, results: list[QualifierResult]
    ) -> list[TopicResult]:
        """Generate a knowledge profile for the user based on the results.

        Args:
            user_id (str): The ID of the user.
            results (list[QualifierResult]): Results from the qualifier service.

        Returns:
            list[TopicResult]: Topic results with averaged scores.
        """
        topic_scores: defaultdict[str, list[int]] = defaultdict(list)
        for result in results:
            topic_scores[result.question_topic].append(result.score)

        topic_results: list[TopicResult] = [
            TopicResult(
                user_id=user_id,
                topic=topic,
                score=round(sum(scores) / len(scores)),
            )
            for topic, scores in topic_scores.items()
        ]
        return topic_results

    async def save_knowledge_profile(self, topic_results: list[TopicResult]):
        """Save the knowledge profile for the user.

        Args:
            topic_results (list[TopicResult]): Topic results to save.
        """
        for topic_result in topic_results:
            await self.assessment_repository.save_topic_result(topic_result)
