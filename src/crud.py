"""
CRUD operations for database interactions.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.models_db import Student, Conversation, Message

class CRUDOperations:
    def __init__(self, db_session: Session):
        self.db = db_session
        
    # Student operations
    def create_student(self, username: str, email: Optional[str] = None) -> Student:
        """Create a new student."""
        student = Student(username=username, email=email)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student
        
    def get_student(self, student_id: int) -> Optional[Student]:
        """Get student by ID."""
        return self.db.query(Student).filter(Student.id == student_id).first()
        
    def update_student_login(self, student_id: int) -> bool:
        """Update student's last login time."""
        student = self.get_student(student_id)
        if student:
            student.last_login = datetime.utcnow()
            self.db.commit()
            return True
        return False
        
    # Conversation operations
    def create_conversation(self, student_id: int, title: str, chat_metadata: Dict = None) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            student_id=student_id,
            title=title,
            chat_metadata=chat_metadata or {}
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
        
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        
    def list_student_conversations(self, student_id: int) -> List[Conversation]:
        """List all conversations for a student."""
        return (self.db.query(Conversation)
                .filter(Conversation.student_id == student_id)
                .order_by(Conversation.created_at.desc())
                .all())
                
    # Message operations
    def create_message(
        self, 
        conversation_id: int, 
        sender: str, 
        content: str,
        response_time: Optional[float] = None,
        metadata: Dict = None  # Store context, sources, etc.
    ) -> Message:
        """Create a new message."""
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
            response_time=response_time,
            message_metadata=metadata or {}
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
        
    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        """Get all messages in a conversation."""
        return (self.db.query(Message)
                .filter(Message.conversation_id == conversation_id)
                .order_by(Message.created_at)
                .all())