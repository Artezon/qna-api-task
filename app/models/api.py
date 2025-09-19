from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, Field


class QuestionReadNoAnswers(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}   # for model_validate() in endpoints, to copy needed fields from DB model


class QuestionReadWithAnswers(BaseModel):
    id: int
    text: str
    created_at: datetime
    answers: List["AnswerRead"]

    model_config = {"from_attributes": True}


class PaginatedQuestions(BaseModel):
    page: int
    count: int
    total: int
    data: List[QuestionReadNoAnswers]


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, description="Question text")


class AnswerRead(BaseModel):
    id: int
    question_id: int
    user_id: uuid.UUID
    text: str
    created_at: datetime

    model_config = {"from_attributes": True}
