from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, func, select
from app.logger import logger
from app.models.api import AnswerCreate, AnswerRead, PaginatedQuestions, QuestionCreate, QuestionReadNoAnswers, QuestionReadWithAnswers
from app.models.tables import Answer, Question
from app.db import engine
from app.routes.questions import questions_api
from app.repository.answers import AnswerRepository
from app.repository.questions import QuestionRepository

answers_api = APIRouter(prefix="/answers")

@questions_api.post("/{question_id}/answers", response_model=AnswerRead)
async def post_answer(
    question_id: int,
    answer_in: AnswerCreate
):
    """Post a new answer"""
    new_answer = Answer(question_id=question_id, user_id=answer_in.user_id, text=answer_in.text)

    logger.debug(f"Creating new answer for question ID={question_id} from user ID={new_answer.user_id} with text: {new_answer.text}")

    with Session(engine) as session:
        question = QuestionRepository.get_question(session, question_id)
        if not question:
            logger.debug(f"Question ID={question_id} not found")
            raise HTTPException(status_code=404, detail="Question not found")

        AnswerRepository.insert_answer(session, new_answer)
        logger.debug(f"Created answer for question ID={question_id} from user ID={new_answer.user_id} with ID: {new_answer.id}")

    return AnswerRead.model_validate(new_answer)


@answers_api.get("/{id}", response_model=AnswerRead)
async def get_answer(id: int):
    """Get an answer by ID"""
    logger.debug(f"Fetching answer with ID: {id}")
    with Session(engine) as session:
        answer = AnswerRepository.get_answer(session, id)
        if not answer:
            logger.warning(f"Answer with ID {id} not found")
            raise HTTPException(status_code=404, detail="Answer not found")
    
        logger.debug(f"Fetched answer: {answer.text}")

        return AnswerRead.model_validate(answer)


@answers_api.delete("/{id}")
async def delete_answer(id: int):
    """Delete an answer by ID"""
    logger.debug(f"Deleting answer with ID: {id}")

    with Session(engine) as session:
        answer = AnswerRepository.get_answer(session, id)
        if not answer:
            logger.warning(f"Answer with ID {id} not found")
            raise HTTPException(status_code=404, detail="Answer not found")
        
        answer = AnswerRepository.delete_answer(session, answer)
        logger.debug(f"Deleted answer with ID: {id}")

    return None
