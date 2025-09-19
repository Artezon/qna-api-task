from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, func, select
from app.logger import logger
from app.models.api import PaginatedQuestions, QuestionCreate, QuestionReadNoAnswers, QuestionReadWithAnswers
from app.models.tables import Question
from app.db import engine
from app.repository.questions import QuestionRepository

questions_api = APIRouter(prefix="/questions")


@questions_api.get("/", response_model=PaginatedQuestions)
def get_questions(
    page: int = Query(1, ge=1, description="Page number"),
    count: int = Query(10, ge=1, le=1000, description="Number of questions per page"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'")
):
    """Get a list of questions"""
    logger.debug(f"Fetching questions: page={page}, count={count}, sort_order={sort_order}")

    offset = (page - 1) * count

    with Session(engine) as session:
        questions = QuestionRepository.get_questions(session, offset, count, sort_order)
        total = QuestionRepository.count_questions(session)
        logger.debug(f"Fetched {len(questions)} questions out of total {total}")

    questions = [QuestionReadNoAnswers.model_validate(q) for q in questions]

    return PaginatedQuestions(page=page, count=len(questions), total=total, data=questions)


@questions_api.post("/", response_model=QuestionReadNoAnswers)
def post_question(
    question_in: QuestionCreate
):
    """Post a new question"""
    logger.debug(f"Creating new question with text: {question_in.text}")

    new_question = Question(text=question_in.text)

    with Session(engine) as session:
        QuestionRepository.insert_question(session, new_question)
        logger.debug(f"Created question with ID: {new_question.id}")

    return QuestionReadNoAnswers.model_validate(new_question)


@questions_api.get("/{id}", response_model=QuestionReadWithAnswers)
def get_question(id: int):
    """Get a question by ID with answers"""
    logger.debug(f"Fetching question with ID: {id}")
    with Session(engine) as session:
        question = QuestionRepository.get_question(session, id)
        if not question:
            logger.warning(f"Question with ID {id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
    
        logger.debug(f"Fetched question: {question.text}")

        return QuestionReadWithAnswers.model_validate(question)  # This will load answers to the question


@questions_api.delete("/{id}")
def delete_question(id: int):
    """Delete a question by ID and all its answers"""
    logger.debug(f"Deleting question with ID: {id}")

    with Session(engine) as session:
        question = QuestionRepository.get_question(session, id)
        if not question:
            logger.debug(f"Question with ID {id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
        
        QuestionRepository.delete_question(session, question)
        logger.debug(f"Deleted question with ID: {id}")

    return None
