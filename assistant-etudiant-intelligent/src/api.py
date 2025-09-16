"""
API for Ollama RAG System
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)

# Local imports
from .rag_engine import RAGEngine
from .vector_store import VectorStore
from .database import get_db
from .crud import CRUDOperations
from .models import QuestionType, SubjectType
from .models_db import Student, Conversation, Message

# Initialize FastAPI app
app = FastAPI(title="Ollama RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
vector_store = VectorStore(index_path="faiss_index", texts_dir="data")
rag_engine = RAGEngine(vector_store=vector_store, model_name="mistral")

# Pydantic models
class StudentCreate(BaseModel):
    """Request model for creating a student."""
    username: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)

class StudentResponse(BaseModel):
    """Response model for student data."""
    id: int
    username: str
    email: Optional[str]
    created_at: datetime

class ConversationCreate(BaseModel):
    """Request model for creating a conversation."""
    student_id: int
    title: str = Field(..., min_length=1, max_length=200)
    chat_metadata: Optional[Dict] = None

class ConversationResponse(BaseModel):
    """Response model for conversation data."""
    id: int
    title: str
    created_at: datetime
    chat_metadata: Optional[Dict]

class MessageCreate(BaseModel):
    """Request model for creating a message."""
    conversation_id: int
    content: str = Field(..., min_length=1)
    sender: str = Field(..., pattern="^(user|assistant)$")
    response_time: Optional[float] = None
    message_metadata: Optional[Dict] = None

class MessageResponse(BaseModel):
    """Response model for message data."""
    id: int
    content: str
    sender: str
    created_at: datetime
    response_time: Optional[float]
    message_metadata: Optional[Dict]

class QuestionRequest(BaseModel):
    """Request model for questions."""
    question: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[int] = None
    subject: Optional[SubjectType] = None
    question_type: Optional[QuestionType] = None
    
class QuestionResponse(BaseModel):
    """Response model for answers."""
    answer: str
    response_time: float
    sources: List[str]
    metadata: Dict[str, Any]

# API Endpoints
@app.post("/students/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """Create a new student."""
    try:
        crud = CRUDOperations(db)
        db_student = crud.create_student(
            username=student.username,
            email=student.email
        )
        return db_student
    except Exception as e:
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/conversations/", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """Create a new conversation."""
    try:
        crud = CRUDOperations(db)
        db_conversation = crud.create_conversation(
            student_id=conversation.student_id,
            title=conversation.title,
            chat_metadata=conversation.chat_metadata
        )
        return db_conversation
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/messages/", response_model=MessageResponse)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message."""
    try:
        crud = CRUDOperations(db)
        db_message = crud.create_message(
            conversation_id=message.conversation_id,
            sender=message.sender,
            content=message.content,
            response_time=message.response_time,
            metadata=message.message_metadata
        )
        return db_message
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rag/question", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):
    """Ask a question using the RAG system."""
    try:
        # Get answer from RAG engine
        response = rag_engine.answer_question(
            question=request.question,
            subject=request.subject,
            question_type=request.question_type
        )
        
        # If conversation_id provided, save the interaction
        if request.conversation_id:
            crud = CRUDOperations(db)
            
            # Save user's question
            crud.create_message(
                conversation_id=request.conversation_id,
                sender="user",
                content=request.question
            )
            
            # Save system's response
            crud.create_message(
                conversation_id=request.conversation_id,
                sender="assistant",
                content=response["answer"],
                response_time=response.get("response_time"),
                metadata={
                    "sources": response.get("sources", []),
                    "context": response.get("context", "")
                }
            )
            
        return response
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=str(e))