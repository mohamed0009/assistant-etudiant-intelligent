"""
Test database integration and CRUD operations.
"""

import unittest
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.database import get_db, init_db
from src.models_db import Base, Student, Conversation, Message, QuestionMetrics
from src.crud import CRUDOperations

class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        """Set up test database."""
        init_db()
        
    def test_student_creation(self):
        """Test student creation and retrieval."""
        with get_db() as db:
            crud = CRUDOperations(db)
            
            # Create student
            student = crud.create_student(
                username="test_user",
                email="test@example.com"
            )
            
            # Verify student
            self.assertIsNotNone(student.id)
            self.assertEqual(student.username, "test_user")
            self.assertEqual(student.email, "test@example.com")
            
            # Test retrieval
            retrieved = crud.get_student(student.id)
            self.assertEqual(retrieved.username, student.username)
            
    def test_conversation_flow(self):
        """Test conversation and message creation."""
        with get_db() as db:
            crud = CRUDOperations(db)
            
            # Create student
            student = crud.create_student(username="chat_user")
            
            # Create conversation
            conv = crud.create_conversation(
                student_id=student.id,
                title="Test Conversation",
                metadata={"subject": "physics"}
            )
            
            # Add messages
            msg1 = crud.create_message(
                conversation_id=conv.id,
                sender="user",
                content="What is Newton's first law?",
                confidence=None
            )
            
            msg2 = crud.create_message(
                conversation_id=conv.id,
                sender="assistant",
                content="Newton's first law states that...",
                confidence=0.95,
                response_time=0.5
            )
            
            # Verify conversation
            messages = crud.get_conversation_messages(conv.id)
            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0].content, msg1.content)
            self.assertEqual(messages[1].content, msg2.content)
            
    def test_metrics_recording(self):
        """Test metrics recording and retrieval."""
        with get_db() as db:
            crud = CRUDOperations(db)
            
            # Record metrics
            metrics = crud.create_question_metrics(
                question="What is energy?",
                response_time=0.75,
                confidence=0.88,
                question_type="conceptual",
                subject="physics",
                user_id="test_user",
                sources_used=3,
                metadata={"difficulty": "medium"}
            )
            
            # Verify metrics
            self.assertIsNotNone(metrics.id)
            self.assertEqual(metrics.question_type, "conceptual")
            self.assertEqual(metrics.subject, "physics")
            
            # Get performance metrics
            performance = crud.get_performance_metrics()
            self.assertIsNotNone(performance["average_response_time"])
            self.assertIsNotNone(performance["average_confidence"])
            
if __name__ == '__main__':
    unittest.main()