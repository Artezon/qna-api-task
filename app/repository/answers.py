from sqlmodel import Session, select
from app.models.tables import Answer

class AnswerRepository:
    @staticmethod
    def get_answer(session: Session, answer_id: int) -> Answer | None:
        return session.exec(select(Answer).where(Answer.id == answer_id)).first()

    @staticmethod
    def insert_answer(session: Session, answer: Answer) -> Answer:
        session.add(answer)
        session.commit()
        session.refresh(answer)
        return answer

    @staticmethod
    def delete_answer(session: Session, answer: Answer):
        session.delete(answer)
        session.commit()
