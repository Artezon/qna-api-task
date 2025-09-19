from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, func, select
from app.logger import logger
from app.models.api import PaginatedQuestions, QuestionCreate, QuestionReadNoAnswers, QuestionReadWithAnswers
from app.models.tables import Question
from app.db import engine

questions_api = APIRouter(prefix="/questions")


@questions_api.get("/", response_model=PaginatedQuestions)
async def get_questions(
    page: int = Query(1, ge=1, description="Page number"),
    count: int = Query(10, ge=1, le=1000, description="Number of questions per page"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'")
):
    """Get a list of questions"""
    logger.debug(f"Fetching questions: page={page}, count={count}, sort_order={sort_order}")

    offset = (page - 1) * count
    stmt = (
        select(Question)
        .order_by(Question.id if sort_order.lower() == "asc" else Question.id.desc())
        .offset(offset)
        .limit(count)
    )

    with Session(engine) as session:
        questions = session.exec(stmt).all()
        total = session.exec(select(func.count(Question.id))).one()
        logger.debug(f"Fetched {len(questions)} questions out of total {total}")

    questions = [QuestionReadNoAnswers.model_validate(q) for q in questions]

    return PaginatedQuestions(page=page, count=count, total=total, data=questions)


@questions_api.post("/", response_model=QuestionReadNoAnswers)
async def post_question(
    question_in: QuestionCreate
):
    """Post a new question"""
    logger.debug(f"Creating new question with text: {question_in.text}")

    new_question = Question(text=question_in.text)

    with Session(engine) as session:
        session.add(new_question)
        session.commit()
        session.refresh(new_question)
        logger.debug(f"Created question with ID: {new_question.id}")

    return QuestionReadNoAnswers.model_validate(new_question)


@questions_api.get("/{id}", response_model=QuestionReadWithAnswers)
async def get_question(id: int):
    """Get a question by ID with answers"""
    logger.debug(f"Fetching question with ID: {id}")
    with Session(engine) as session:
        question = session.exec(select(Question).where(Question.id == id)).first()
        if not question:
            logger.warning(f"Question with ID {id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
    
        logger.debug(f"Fetched question: {question.text}")

        return QuestionReadWithAnswers.model_validate(question)  # This will load answers to the question


@questions_api.delete("/{id}", response_model=Question)
async def delete_question(id: int):
    """Delete a question by ID and all its answers"""
    logger.debug(f"Deleting question with ID: {id}")

    with Session(engine) as session:
        question = session.exec(select(Question).where(Question.id == id)).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        session.delete(question)
        session.commit()
        logger.debug(f"Deleted question with ID: {id}")

    return None
