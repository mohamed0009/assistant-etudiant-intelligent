"""
Test export service functionality.
"""

import unittest
import tempfile
import shutil
import os
from pathlib import Path
import json
import csv
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.export_service import ExportService
from src.crud import CRUDOperations

class TestExportService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Create temporary database
        cls.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        cls.db_url = f"sqlite:///{cls.temp_db.name}"
        
        # Create engine and session
        cls.engine = create_engine(cls.db_url)
        cls.TestingSessionLocal = sessionmaker(bind=cls.engine)
        
        # Create tables
        Base.metadata.create_all(bind=cls.engine)
        
        # Create temporary export directory
        cls.temp_dir = tempfile.mkdtemp()
        cls.export_dir = Path(cls.temp_dir) / "exports"
        
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        try:
            cls.temp_db.close()
            os.unlink(cls.temp_db.name)
        except:
            pass  # Ignore errors on Windows
            
        shutil.rmtree(cls.temp_dir)
        
    def setUp(self):
        """Set up new session for each test."""
        self.db = self.TestingSessionLocal()
        self.crud = CRUDOperations(self.db)
        self.export_service = ExportService(
            db_session=self.db,
            export_dir=str(self.export_dir)
        )
        
        # Create test data with unique email per test method
        test_name = self._testMethodName
        self.student = self.crud.create_student(
            username=f"test_user_{test_name}",
            email=f"test_{test_name}@example.com"
        )
        
        self.conversation = self.crud.create_conversation(
            student_id=self.student.id,
            title="Test Conversation",
            chat_metadata={"subject": "physics"}
        )
        
        # Add messages
        self.crud.create_message(
            conversation_id=self.conversation.id,
            sender="user",
            content="What is energy?",
            confidence=None
        )
        
        self.crud.create_message(
            conversation_id=self.conversation.id,
            sender="assistant",
            content="Energy is the capacity to do work...",
            confidence=0.95,
            response_time=0.5,
            metadata={"sources_used": 2}
        )
        
        # Add metrics
        self.crud.create_question_metrics(
            question="What is energy?",
            response_time=0.75,
            confidence=0.88,
            question_type="conceptual",
            subject="physics",
            user_id=str(self.student.id),
            sources_used=2
        )
        
    def tearDown(self):
        """Clean up after each test."""
        self.db.close()
        
        # Clear export directory
        if self.export_dir.exists():
            for f in self.export_dir.glob("*"):
                try:
                    f.unlink()
                except:
                    pass  # Ignore errors on Windows
                    
    def test_export_conversation_json(self):
        """Test conversation export to JSON."""
        output_file = self.export_service.export_student_conversations(
            student_id=self.student.id,
            format="json"
        )
        
        self.assertTrue(Path(output_file).exists())
        
        with open(output_file) as f:
            data = json.load(f)
            
        self.assertEqual(len(data), 1)  # One conversation
        self.assertEqual(len(data[0]["messages"]), 2)  # Two messages
        self.assertEqual(data[0]["title"], "Test Conversation")
        
    def test_export_conversation_csv(self):
        """Test conversation export to CSV."""
        output_file = self.export_service.export_student_conversations(
            student_id=self.student.id,
            format="csv"
        )
        
        self.assertTrue(Path(output_file).exists())
        
        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        self.assertEqual(len(rows), 2)  # Two messages
        self.assertEqual(rows[0]["conversation_title"], "Test Conversation")
        self.assertEqual(rows[1]["message_sender"], "assistant")
        self.assertEqual(float(rows[1]["confidence"]), 0.95)
        
    def test_export_metrics_json(self):
        """Test metrics export to JSON."""
        output_file = self.export_service.export_metrics(format="json")
        
        self.assertTrue(Path(output_file).exists())
        
        with open(output_file) as f:
            data = json.load(f)
            
        self.assertIn("average_response_time", data)
        self.assertIn("average_confidence", data)
        self.assertIn("total_questions", data)
        
    def test_export_metrics_csv(self):
        """Test metrics export to CSV."""
        output_file = self.export_service.export_metrics(format="csv")
        
        self.assertTrue(Path(output_file).exists())
        
        with open(output_file) as f:
            reader = csv.DictReader(f)
            data = next(reader)  # Only one row for metrics
            
        self.assertIn("average_response_time", data)
        self.assertIn("average_confidence", data)
        self.assertIn("total_questions", data)
        
    def test_invalid_format(self):
        """Test error handling for invalid format."""
        with self.assertRaises(ValueError):
            self.export_service.export_metrics(format="invalid")
            
        with self.assertRaises(ValueError):
            self.export_service.export_student_conversations(
                student_id=self.student.id,
                format="invalid"
            )
            
if __name__ == '__main__':
    unittest.main()