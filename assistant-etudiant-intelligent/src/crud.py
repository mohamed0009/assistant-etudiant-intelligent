from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from .models_db import Student, Conversation, Message, QuestionMetric, UserSessionDB

# Students

def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    return db.query(Student).filter(Student.email == email).first()

def create_student(db: Session, name: str, email: str, role: str = "student") -> Student:
    student = Student(name=name, email=email, role=role)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_student(db: Session, student_id: int) -> Optional[Student]:
    return db.query(Student).filter(Student.id == student_id).first()

# Conversations

def create_conversation(db: Session, student_id: int, title: str = "Conversation") -> Conversation:
    conv = Conversation(student_id=student_id, title=title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_student_conversations(db: Session, student_id: int) -> List[Conversation]:
    return db.query(Conversation).filter(Conversation.student_id == student_id).order_by(Conversation.updated_at.desc()).all()

# Messages

def add_message(
    db: Session,
    conversation_id: int,
    sender: str,
    content: str,
    confidence: Optional[str] = None,
    response_time: Optional[str] = None,
) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        sender=sender,
        content=content,
        confidence=confidence,
        response_time=response_time,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversation_messages(db: Session, conversation_id: int) -> List[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()


# Metrics

def record_question_metric(
    db: Session,
    *,
    question: str,
    response_time: float,
    confidence: float,
    question_type: str,
    subject: Optional[str],
    user_id: str,
    sources_used: int = 0,
) -> QuestionMetric:
    metric = QuestionMetric(
        question=question,
        response_time=response_time,
        confidence=confidence,
        question_type=question_type,
        subject=subject,
        user_id=user_id,
        sources_used=sources_used,
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def list_question_metrics(db: Session, limit: Optional[int] = None) -> List[QuestionMetric]:
    q = db.query(QuestionMetric).order_by(QuestionMetric.id.asc())
    if limit:
        q = q.limit(limit)
    return q.all()

def recent_question_metrics(db: Session, limit: int = 10) -> List[QuestionMetric]:
    return (
        db.query(QuestionMetric)
        .order_by(QuestionMetric.id.desc())
        .limit(limit)
        .all()
    )

def aggregate_performance_metrics(db: Session) -> Dict:
    from datetime import datetime
    rows = db.query(QuestionMetric).all()
    if not rows:
        return {
            "total_questions": 0,
            "average_response_time": 0.0,
            "total_users": 0,
            "questions_today": 0,
            "most_asked_subjects": {},
            "response_time_trend": [],
            "confidence_trend": [],
            "documents_usage": {},
            "precomputed_vs_documents": {},
        }

    total_questions = len(rows)
    avg_rt = sum(r.response_time for r in rows) / total_questions
    users = len({r.user_id for r in rows})
    today = datetime.utcnow().date()
    questions_today = sum(1 for r in rows if (r.timestamp or datetime.utcnow()).date() == today)
    # subjects count
    subjects: Dict[str, int] = {}
    for r in rows:
        if r.subject:
            subjects[r.subject] = subjects.get(r.subject, 0) + 1
    # trends (last 10 by id)
    last10 = sorted(rows, key=lambda r: r.id)[-10:]
    response_time_trend = [r.response_time for r in last10]
    confidence_trend = [r.confidence for r in last10]
    documents_usage = {"documents_accessed": sum(1 for r in rows if (r.sources_used or 0) > 0)}
    precomp_docs: Dict[str, int] = {}
    for r in rows:
        key = r.question_type or "unknown"
        precomp_docs[key] = precomp_docs.get(key, 0) + 1

    return {
        "total_questions": total_questions,
        "average_response_time": avg_rt,
        "total_users": users,
        "questions_today": questions_today,
        "most_asked_subjects": subjects,
        "response_time_trend": response_time_trend,
        "confidence_trend": confidence_trend,
        "documents_usage": documents_usage,
        "precomputed_vs_documents": precomp_docs,
    }

# User sessions

def start_user_session(db: Session, user_id: str) -> UserSessionDB:
    session = UserSessionDB(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def end_user_session(db: Session, user_id: str) -> bool:
    from datetime import datetime
    session = (
        db.query(UserSessionDB)
        .filter(UserSessionDB.user_id == user_id, UserSessionDB.session_end.is_(None))
        .order_by(UserSessionDB.id.desc())
        .first()
    )
    if not session:
        return False
    session.session_end = datetime.utcnow()
    db.add(session)
    db.commit()
    return True

def get_user_sessions(db: Session, user_id: str) -> List[UserSessionDB]:
    return (
        db.query(UserSessionDB)
        .filter(UserSessionDB.user_id == user_id)
        .order_by(UserSessionDB.id.desc())
        .all()
    )

