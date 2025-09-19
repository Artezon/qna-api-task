from sqlmodel import Session, select, func
from app.models.tables import Question

class QuestionRepository:
    @staticmethod
    def get_question(session: Session, question_id: int) -> Question | None:
        """Get a single question by ID"""
        return session.exec(select(Question).where(Question.id == question_id)).first()

    @staticmethod
    def get_questions(session: Session, offset: int = 0, limit: int = 10, sort_order: str = "asc") -> list[Question]:
        """Get paginated list of questions"""
        stmt = select(Question)
        if sort_order.lower() == "desc":
            stmt = stmt.order_by(Question.id.desc())
        else:
            stmt = stmt.order_by(Question.id)
        stmt = stmt.offset(offset).limit(limit)
        return session.exec(stmt).all()

    @staticmethod
    def count_questions(session: Session) -> int:
        """Get total number of questions"""
        return session.exec(select(func.count(Question.id))).one()

    @staticmethod
    def insert_question(session: Session, question: Question) -> Question:
        """Create a new question"""
        session.add(question)
        session.commit()
        session.refresh(question)
        return question

    @staticmethod
    def delete_question(session: Session, question: Question):
        """Delete a question (and its answers)"""
        session.delete(question)
        session.commit()
