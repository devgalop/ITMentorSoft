from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class AssessmentEntity(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)

    user: Mapped["UserEntity"] = relationship("UserEntity")
    answers: Mapped[List["AssessmentAnswerEntity"]] = relationship(
        "AssessmentAnswerEntity", back_populates="assessment"
    )
    questions: Mapped[List["AssessmentQuizEntity"]] = relationship(
        "AssessmentQuizEntity", back_populates="assessment"
    )


class AssessmentAnswerEntity(Base):
    __tablename__ = "assessment_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessments.id"), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey("questions.id"), index=True
    )
    answer: Mapped[str] = mapped_column(String)
    time_taken_seconds: Mapped[int] = mapped_column(Integer)

    assessment: Mapped["AssessmentEntity"] = relationship(
        "AssessmentEntity", back_populates="answers"
    )
    question: Mapped["QuestionEntity"] = relationship("QuestionEntity")


class AssessmentQuizEntity(Base):
    __tablename__ = "assessment_quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    assessment_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessments.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey("questions.id"), index=True
    )
    rubric: Mapped["QuestionEntity"] = relationship("QuestionEntity")
    assessment: Mapped["AssessmentEntity"] = relationship(
        "AssessmentEntity", back_populates="questions"
    )
