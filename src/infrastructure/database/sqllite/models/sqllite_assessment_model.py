from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from src.infrastructure.database.sqllite.models.sqllite_question_model import (
    QuestionEntity,
)
from src.infrastructure.database.sqllite.models.sqllite_user_model import UserEntity
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base

CROSSFIELD_QUESTION_ID = "questions.id"
CROSSFIELD_USER_ID = "users.id"
CROSSFIELD_ASSESSMENT_ID = "assessments.id"
CROSSFIELD_ANSWER_ID = "assessment_answers.id"


class AssessmentEntity(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_USER_ID), index=True
    )

    user: Mapped["UserEntity"] = relationship("UserEntity")
    answers: Mapped[List["AssessmentAnswerEntity"]] = relationship(
        "AssessmentAnswerEntity", back_populates="assessment"
    )
    questions: Mapped[List["AssessmentQuizEntity"]] = relationship(
        "AssessmentQuizEntity", back_populates="assessment"
    )
    qualifications: Mapped[List["AssessmentQualificationEntity"]] = relationship(
        "AssessmentQualificationEntity", back_populates="assessment"
    )


class AssessmentAnswerEntity(Base):
    __tablename__ = "assessment_answers"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    assessment_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_ASSESSMENT_ID), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_QUESTION_ID), index=True
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
        String, ForeignKey(CROSSFIELD_ASSESSMENT_ID), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_QUESTION_ID), index=True
    )
    rubric: Mapped["QuestionEntity"] = relationship("QuestionEntity")
    assessment: Mapped["AssessmentEntity"] = relationship(
        "AssessmentEntity", back_populates="questions"
    )


class AssessmentQualificationEntity(Base):
    __tablename__ = "assessment_qualifications"
    __table_args__ = (
        UniqueConstraint(
            "question_id",
            "user_id",
            "assessment_id",
            name="uq_assessment_qualification",
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    assessment_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_ASSESSMENT_ID), index=True
    )
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_QUESTION_ID), index=True
    )
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_USER_ID), index=True
    )
    answer_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_ANSWER_ID), index=True
    )
    score: Mapped[int] = mapped_column(Integer)
    feedback: Mapped[str] = mapped_column(String)

    question_topic: Mapped[str] = mapped_column(String)
    question_difficulty: Mapped[str] = mapped_column(String)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    assessment: Mapped["AssessmentEntity"] = relationship(
        "AssessmentEntity", back_populates="qualifications"
    )
    question: Mapped["QuestionEntity"] = relationship("QuestionEntity")
    user: Mapped["UserEntity"] = relationship("UserEntity")
    answer: Mapped["AssessmentAnswerEntity"] = relationship("AssessmentAnswerEntity")
    key_concepts: Mapped[List["AssessmentQualificationKeyConceptEntity"]] = (
        relationship(
            "AssessmentQualificationKeyConceptEntity", back_populates="qualification"
        )
    )
    misconceptions: Mapped[List["AssessmentMisconceptionEntity"]] = relationship(
        "AssessmentMisconceptionEntity", back_populates="qualification"
    )


class AssessmentQualificationKeyConceptEntity(Base):
    __tablename__ = "assessment_qualification_key_concepts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qualification_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessment_qualifications.id"), index=True
    )
    key_concept: Mapped[str] = mapped_column(String)

    qualification: Mapped["AssessmentQualificationEntity"] = relationship(
        "AssessmentQualificationEntity", back_populates="key_concepts"
    )


class AssessmentMisconceptionEntity(Base):
    __tablename__ = "assessment_misconceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    qualification_id: Mapped[str] = mapped_column(
        String, ForeignKey("assessment_qualifications.id"), index=True
    )
    misconception: Mapped[str] = mapped_column(String)

    qualification: Mapped["AssessmentQualificationEntity"] = relationship(
        "AssessmentQualificationEntity", back_populates="misconceptions"
    )


class TopicResultEntity(Base):
    __tablename__ = "topic_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey(CROSSFIELD_USER_ID), index=True
    )
    topic: Mapped[str] = mapped_column(String, index=True)
    score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    is_enabled: Mapped[bool] = mapped_column(default=True)
    user: Mapped["UserEntity"] = relationship("UserEntity")
