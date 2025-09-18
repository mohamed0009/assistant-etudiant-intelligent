"""
SQLAlchemy database models for the Ollama RAG system.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Student(Base):
    """Student model for user management."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default='student')
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="student")
    
    def __repr__(self):
        return f"<Student {self.name}>"

class Conversation(Base):
    """Conversation model for chat history."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    title = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    chat_metadata = Column(JSON)
    
    # Relationships
    student = relationship("Student", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation {self.id} - {self.title}>"

class Message(Base):
    """Message model for individual chat messages."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender = Column(String(50))  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    response_time = Column(Float)  # Time taken by Ollama to generate response
    message_metadata = Column(JSON)  # Store context, sources, etc.
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.id} - {self.sender}>"