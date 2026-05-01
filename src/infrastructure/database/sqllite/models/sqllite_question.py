from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from src.infrastructure.database.sqllite.shared.sqllite_database_session import Base


class QuestionEntity(Base):
    __tablename__ = "questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, index=True)
    options: Mapped[str] = mapped_column(
        String
    )  # Store options as a pipe-separated string
    correct_answer: Mapped[str] = mapped_column(String)

    skill_metadata: Mapped[Optional["QuestionSkillMetadataEntity"]] = relationship(
        "QuestionSkillMetadataEntity", back_populates="question", uselist=False
    )
    diagnostic_metadata: Mapped[Optional["QuestionDiagnosticMetadataEntity"]] = (
        relationship(
            "QuestionDiagnosticMetadataEntity", back_populates="question", uselist=False
        )
    )


class QuestionSkillMetadataEntity(Base):
    __tablename__ = "question_skill_metadata"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey("questions.id"), unique=True, index=True
    )
    main_competency: Mapped[str] = mapped_column(String)
    sub_competency: Mapped[str] = mapped_column(String)
    taxanomic_level: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    stimated_time: Mapped[int] = mapped_column(String)

    question: Mapped["QuestionEntity"] = relationship(
        "QuestionEntity", back_populates="skill_metadata"
    )


class QuestionDiagnosticMetadataEntity(Base):
    __tablename__ = "question_diagnostic_metadata"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    question_id: Mapped[str] = mapped_column(
        String, ForeignKey("questions.id"), unique=True, index=True
    )
    explanation: Mapped[str] = mapped_column(String)

    question: Mapped["QuestionEntity"] = relationship(
        "QuestionEntity", back_populates="diagnostic_metadata"
    )
    misconceptions: Mapped[List["QuestionMisconceptionDiagnosticMetadataEntity"]] = (
        relationship(
            "QuestionMisconceptionDiagnosticMetadataEntity",
            back_populates="diagnostic_metadata",
        )
    )


class QuestionMisconceptionDiagnosticMetadataEntity(Base):
    __tablename__ = "question_misconception_diagnostic_metadata"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    diagnostic_metadata_id: Mapped[str] = mapped_column(
        String, ForeignKey("question_diagnostic_metadata.id"), index=True
    )
    misconception: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    feedback: Mapped[str] = mapped_column(String)

    diagnostic_metadata: Mapped["QuestionDiagnosticMetadataEntity"] = relationship(
        "QuestionDiagnosticMetadataEntity", back_populates="misconceptions"
    )
