from collections import defaultdict

from src.features.assessments.shared.assessment import Assessment
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.qualifier_service import (
    QualifierPrompt,
    QualifierResult,
    QualifierService,
    TopicResult,
)
from src.features.assessments.shared.questions_repository import QuestionRepository

EVALUATION_MODE = "normal"


class EvaluateAssessmentService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        qualifier_service: QualifierService,
        question_repository: QuestionRepository,
    ):
        self.assessment_repository = assessment_repository
        self.qualifier_service = qualifier_service
        self.question_repository = question_repository

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

        Args:
            assessment (Assessment): The assessment containing the answers to be evaluated.

        Returns:
            list[QualifierResult]: A list of results from the qualifier service, including scores, feedback, key concepts detected, and misconceptions detected for each answer.
        """
        evaluation_results: list[QualifierResult] = []

        # Pre-fetch all rubrics in a single query
        question_ids = [answer.question_id for answer in assessment.answers]
        if not question_ids:
            return evaluation_results

        rubrics_dict = await self.question_repository.get_question_rubrics_bulk(
            question_ids
        )

        for answer in assessment.answers:
            rubric = rubrics_dict.get(answer.question_id)
            if not rubric:
                continue
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
            results (list[QualifierResult]): A list of results from the qualifier service, including scores, feedback, key concepts detected, and misconceptions detected for each answer.
        """
        for result in results:
            await self.assessment_repository.save_assessment_qualification(result)

    def get_knowledge_profile(
        self, user_id: str, results: list[QualifierResult]
    ) -> list[TopicResult]:
        """Generate a knowledge profile for the user based on the results of the assessment evaluation.

        Args:
            user_id (str): The ID of the user for whom the knowledge profile is being generated.
            results (list[QualifierResult]): A list of results from the qualifier service, including scores, feedback, key concepts detected, and misconceptions detected for each answer.

        Returns:
            list[TopicResult]: A list of topic results, including the user's score for each topic.
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
        """Save the knowledge profile for the user to the assessment repository.

        Args:
            topic_results (list[TopicResult]): A list of topic results, including the user's score for each topic.
        """
        for topic_result in topic_results:
            await self.assessment_repository.save_topic_result(topic_result)
