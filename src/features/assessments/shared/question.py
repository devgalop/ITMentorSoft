from enum import Enum
import uuid


class QuestionRubricScore:
    """Define the rubric to assign a score"""

    def __init__(self, score: int, explanation: str):
        self.score = score
        self.explanation = explanation


class QuestionStatus(Enum):
    """Question status

    Args:
        Enum (Enum): Enum class for question status.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class QuestionDifficulty(Enum):
    """Question difficulty

    Args:
        Enum (Enum): Enum class for question difficulty.
    """

    EASY = "básico"
    MEDIUM = "intermedio"
    HARD = "avanzado"


class Question:
    """Represents a question"""

    def __init__(
        self,
        text_to_evaluate: str,
        concept: str,
        definition: str,
        simple_explanation: str,
        correct_sample: str,
        wrong_sample: str,
        common_misconception: list[str],
        rubric: list[QuestionRubricScore],
        semantic_keywords: list[str],
        status: QuestionStatus = QuestionStatus.DRAFT,
        difficulty: QuestionDifficulty = QuestionDifficulty.EASY,
        classification: str = "",
    ):
        self.question_id = uuid.uuid4().hex
        self.text_to_evaluate = text_to_evaluate
        self.concept = concept
        self.definition = definition
        self.simple_explanation = simple_explanation
        self.correct_sample = correct_sample
        self.wrong_sample = wrong_sample
        self.common_misconception = common_misconception
        self.rubric = rubric
        self.semantic_keywords = semantic_keywords
        self.status = status
        self.difficulty = difficulty
        self.classification = classification

    def update_status(self, new_status: QuestionStatus):
        """Update the status of the question

        Args:
            new_status (QuestionStatus): The new status to be assigned to the question.
        """
        self.status = new_status

    def update_difficulty(self, new_difficulty: QuestionDifficulty):
        """Update the difficulty of the question

        Args:
            new_difficulty (QuestionDifficulty): The new difficulty to be assigned to the question.
        """
        self.difficulty = new_difficulty

    def update_classification(self, new_classification: str):
        """Update the classification of the question

        Args:
            new_classification (str): The new classification to be assigned to the question.
        """
        self.classification = new_classification

    def update_text_to_evaluate(self, new_text_to_evaluate: str):
        """Update the text to evaluate of the question

        Args:
            new_text_to_evaluate (str): The new text to evaluate to be assigned to the question.
        """
        self.text_to_evaluate = new_text_to_evaluate

    def add_rubric(self, score: int, explanation: str):
        """Add a rubric to the question

        Args:
            score (int): The score associated with the rubric.
            explanation (str): The explanation for the rubric.
        """
        self.rubric.append(QuestionRubricScore(score, explanation))

    def add_common_misconception(self, misconception: str):
        """Add a common misconception to the question

        Args:
            misconception (str): The common misconception to be added to the question.
        """
        self.common_misconception.append(misconception)

    def add_semantic_keyword(self, keyword: str):
        """Add a semantic keyword to the question

        Args:
            keyword (str): The semantic keyword to be added to the question.
        """
        self.semantic_keywords.append(keyword)

    def update_concept(self, new_concept: str):
        """Update the concept of the question

        Args:
            new_concept (str): The new concept to be assigned to the question.
        """
        self.concept = new_concept

    def update_definition(self, new_definition: str):
        """Update the definition of the question

        Args:
            new_definition (str): The new definition to be assigned to the question.
        """
        self.definition = new_definition

    def update_simple_explanation(self, new_simple_explanation: str):
        """Update the simple explanation of the question

        Args:
            new_simple_explanation (str): The new simple explanation to be assigned to the question.
        """
        self.simple_explanation = new_simple_explanation

    def update_correct_sample(self, new_correct_sample: str):
        """Update the correct sample of the question

        Args:
            new_correct_sample (str): The new correct sample to be assigned to the question.
        """
        self.correct_sample = new_correct_sample

    def update_wrong_sample(self, new_wrong_sample: str):
        """Update the wrong sample of the question

        Args:
            new_wrong_sample (str): The new wrong sample to be assigned to the question.
        """
        self.wrong_sample = new_wrong_sample

    def update_question_id(self, new_question_id: str):
        """Update the question ID of the question

        Args:
            new_question_id (str): The new question ID to be assigned to the question.
        """
        self.question_id = new_question_id


class QuestionBuilder:

    def __init__(self):
        self.question_id = None
        self._text_to_evaluate = ""
        self._concept = ""
        self._definition = ""
        self._simple_explanation = ""
        self._correct_sample = ""
        self._wrong_sample = ""
        self._common_misconception: list[str] = []
        self._rubric: list[QuestionRubricScore] = []
        self._semantic_keywords: list[str] = []
        self._status = QuestionStatus.DRAFT
        self._difficulty = QuestionDifficulty.EASY
        self._classification = ""

    def set_text_to_evaluate(self, text_to_evaluate: str) -> "QuestionBuilder":
        """Set the text to evaluate of the question

        Args:
            text_to_evaluate (str): The text to evaluate to be assigned to the question.
        """
        self._text_to_evaluate = text_to_evaluate
        return self

    def set_difficulty(self, difficulty: QuestionDifficulty) -> "QuestionBuilder":
        """Set the difficulty of the question

        Args:
            difficulty (QuestionDifficulty): The difficulty to be assigned to the question.
        """
        self._difficulty = difficulty
        return self

    def set_classification(self, classification: str) -> "QuestionBuilder":
        """Set the classification of the question

        Args:
            classification (str): The classification to be assigned to the question.
        """
        self._classification = classification
        return self

    def set_concept(self, concept: str) -> "QuestionBuilder":
        """Set the concept of the question

        Args:
            concept (str): The concept to be assigned to the question.
        """
        self._concept = concept
        return self

    def set_definition(self, definition: str) -> "QuestionBuilder":
        """Set the definition of the question

        Args:
            definition (str): The definition to be assigned to the question.
        """
        self._definition = definition
        return self

    def set_simple_explanation(self, simple_explanation: str) -> "QuestionBuilder":
        """Set the simple explanation of the question

        Args:
            simple_explanation (str): The simple explanation to be assigned to the question.
        """
        self._simple_explanation = simple_explanation
        return self

    def set_correct_sample(self, correct_sample: str) -> "QuestionBuilder":
        """Set the correct sample of the question

        Args:
            correct_sample (str): The correct sample to be assigned to the question.
        """
        self._correct_sample = correct_sample
        return self

    def set_wrong_sample(self, wrong_sample: str) -> "QuestionBuilder":
        """Set the wrong sample of the question

        Args:
            wrong_sample (str): The wrong sample to be assigned to the question.
        """
        self._wrong_sample = wrong_sample
        return self

    def add_common_misconception(self, misconception: str) -> "QuestionBuilder":
        """Add a common misconception to the question

        Args:
            misconception (str): The common misconception to be added to the question.
        """
        self._common_misconception.append(misconception)
        return self

    def add_common_misconceptions(self, misconceptions: list[str]) -> "QuestionBuilder":
        """Add common misconceptions to the question

        Args:
            misconceptions (list[str]): The common misconceptions to be added to the question.
        """
        self._common_misconception.extend(misconceptions)
        return self

    def add_rubric(self, score: int, explanation: str) -> "QuestionBuilder":
        """Add a rubric scoreto the question

        Args:
            score (int): The score associated with the rubric.
            explanation (str): The explanation for the rubric.
        """
        self._rubric.append(QuestionRubricScore(score, explanation))
        return self

    def add_rubrics(self, rubrics: list[QuestionRubricScore]) -> "QuestionBuilder":
        """Add rubrics to the question

        Args:
            rubrics (list[QuestionRubricScore]): The rubrics to be added to the question.
        """
        self._rubric.extend(rubrics)
        return self

    def add_semantic_keyword(self, keyword: str) -> "QuestionBuilder":
        """Add a semantic keyword to the question

        Args:
            keyword (str): The semantic keyword to be added to the question.
        """
        self._semantic_keywords.append(keyword)
        return self

    def add_semantic_keywords(self, keywords: list[str]) -> "QuestionBuilder":
        """Add semantic keywords to the question

        Args:
            keywords (list[str]): The semantic keywords to be added to the question.
        """
        self._semantic_keywords.extend(keywords)
        return self

    def set_question_id(self, question_id: str) -> "QuestionBuilder":
        """Set the question ID of the question

        Args:
            question_id (str): The question ID to be assigned to the question.
        """
        self.question_id = question_id
        return self

    def set_status(self, status: QuestionStatus) -> "QuestionBuilder":
        """Set the status of the question

        Args:
            status (QuestionStatus): The status to be assigned to the question.
        """
        self._status = status
        return self

    def build(self) -> Question:
        """Build the question

        Returns:
            Question: The built question.
        """
        question = Question(
            text_to_evaluate=self._text_to_evaluate,
            concept=self._concept,
            definition=self._definition,
            simple_explanation=self._simple_explanation,
            correct_sample=self._correct_sample,
            wrong_sample=self._wrong_sample,
            common_misconception=self._common_misconception,
            rubric=self._rubric,
            semantic_keywords=self._semantic_keywords,
            status=self._status,
            difficulty=self._difficulty,
            classification=self._classification,
        )
        if self.question_id:
            question.update_question_id(self.question_id)
        return question


class EvaluativeQuestion:
    """Represents the question to evaluate students"""

    def __init__(self, question_id: str, text_to_evaluate: str):
        self.question_id = question_id
        self.text_to_evaluate = text_to_evaluate
