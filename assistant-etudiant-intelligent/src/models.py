"""
Modèles de données pour les métriques et analytics
"""

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class QuestionType(str, Enum):
    PRECOMPUTED = "precomputed"
    DOCUMENT_BASED = "document_based"
    MIXED = "mixed"

class SubjectType(str, Enum):
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    ELECTRONICS = "electronics"
    BIOLOGY = "biology"
    GEOLOGY = "geology"
    ASTRONOMY = "astronomy"
    PSYCHOLOGY = "psychology"
    COMPUTER_SCIENCE = "computer_science"

class QuestionMetrics(BaseModel):
    question: str
    response_time: float
    confidence: float
    question_type: QuestionType
    subject: Optional[SubjectType]
    timestamp: datetime
    user_id: str
    sources_used: int

class PerformanceMetrics(BaseModel):
    total_questions: int
    average_response_time: float
    total_users: int
    questions_today: int
    most_asked_subjects: Dict[str, int]
    response_time_trend: List[float]
    confidence_trend: List[float]
    documents_usage: Dict[str, int]
    precomputed_vs_documents: Dict[str, int]

class UserSession(BaseModel):
    user_id: str
    session_start: datetime
    session_end: Optional[datetime]
    questions_count: int
    total_time: float
    subjects_covered: List[str]

class ExportData(BaseModel):
    conversations: List[Dict]
    metrics: PerformanceMetrics
    export_date: datetime
    format: str  # "pdf", "json", "csv"

class AdminStats(BaseModel):
    system_health: str
    documents_count: int
    active_users: int
    error_rate: float
    uptime: float
    last_backup: Optional[datetime]

