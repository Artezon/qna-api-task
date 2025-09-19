from typing import List
from pydantic import BaseModel, Field


class QuestionReadNoAnswers(BaseModel):
    id: int
    text: str
    created_at: str

    model_config = {"from_attributes": True}


class PaginatedQuestions(BaseModel):
    page: int
    count: int
    total: int
    data: List[QuestionReadNoAnswers]


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=1, description="Question text")
