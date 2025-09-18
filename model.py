from datetime import datetime, timezone
from typing import List
import uuid
from sqlmodel import SQLModel, Field, Index, Relationship


class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    answers: List["Answer"] = Relationship(back_populates="question")


class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(foreign_key="question.id", nullable=False)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, nullable=False)
    text: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    question: Question = Relationship(back_populates="answers")
