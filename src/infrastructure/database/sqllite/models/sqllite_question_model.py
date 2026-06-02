from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class QuestionEntity(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, index=True)
    concept: Mapped[str] = mapped_column(String)
    definition: Mapped[str] = mapped_column(String)
    simple_explanation: Mapped[str] = mapped_column(String)
    correct_sample: Mapped[str] = mapped_column(String)
    wrong_sample: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    classification: Mapped[str] = mapped_column(String)
    common_misconceptions: Mapped[str] = mapped_column(
        String
    )  # Store misconceptions as a pipe-separated string
    semantic_keywords: Mapped[str] = mapped_column(
        String
    )  # Store semantic keywords as a pipe-separated string
    status: Mapped[str] = mapped_column(String)

    rubric: Mapped[List["QuestionRubricScoreEntity"]] = relationship(
        "QuestionRubricScoreEntity", back_populates="question"
    )


class QuestionRubricScoreEntity(Base):
    __tablename__ = "question_rubric_scores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey("questions.id"), index=True
    )
    score: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(String)

    question: Mapped["QuestionEntity"] = relationship(
        "QuestionEntity", back_populates="rubric"
    )
