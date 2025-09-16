"""
Test metrics service functionality.
"""

import unittest
import tempfile
from pathlib import Path
import json
import os
import shutil
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.metrics_service import MetricsService

class TestMetricsService(unittest.TestCase):
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
        
        # Create temporary directory for metrics file
        cls.temp_dir = tempfile.mkdtemp()
        cls.metrics_file = Path(cls.temp_dir) / "test_metrics.json"
        
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        cls.temp_db.close()
        os.unlink(cls.temp_db.name)
        shutil.rmtree(cls.temp_dir)
        
    def setUp(self):
        """Set up new session for each test."""
        self.db = self.TestingSessionLocal()
        self.metrics_service = MetricsService(
            db_session=self.db,
            metrics_file=str(self.metrics_file)
        )
        
        # Clear metrics file before each test
        self.metrics_service.save_metrics({
            "questions": [],
            "response_times": [],
            "confidence_scores": [],
            "subject_distribution": {},
            "daily_usage": {}
        })
        
    def tearDown(self):
        """Clean up after each test."""
        self.db.close()
        
    def test_metrics_file_creation(self):
        """Test metrics file initialization."""
        self.assertTrue(self.metrics_file.exists())
        
        with open(self.metrics_file) as f:
            data = json.load(f)
            
        self.assertIn("questions", data)
        self.assertIn("response_times", data)
        self.assertIn("confidence_scores", data)
        self.assertIn("subject_distribution", data)
        self.assertIn("daily_usage", data)
        
    def test_record_question(self):
        """Test recording question metrics."""
        # Record a question
        self.metrics_service.record_question(
            question="What is energy?",
            response_time=0.75,
            confidence=0.88,
            subject="physics",
            user_id="test_user",
            sources_used=3,
            question_type="conceptual",
            metadata={"difficulty": "medium"}
        )
        
        # Check metrics file
        with open(self.metrics_file) as f:
            data = json.load(f)
            
        # Check if question was recorded
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["questions"][0]["text"], "What is energy?")
        
        # Check subject distribution
        self.assertEqual(data["subject_distribution"]["physics"], 1)
        
        # Check performance stats
        stats = self.metrics_service.get_performance_stats()
        self.assertIsNotNone(stats["average_response_time"])
        self.assertIsNotNone(stats["average_confidence"])
        
    def test_multiple_questions(self):
        """Test recording multiple questions."""
        questions = [
            {
                "text": "What is force?",
                "subject": "physics",
                "confidence": 0.9,
                "response_time": 0.6
            },
            {
                "text": "What is a derivative?",
                "subject": "mathematics",
                "confidence": 0.85,
                "response_time": 0.8
            }
        ]
        
        for q in questions:
            self.metrics_service.record_question(
                question=q["text"],
                response_time=q["response_time"],
                confidence=q["confidence"],
                subject=q["subject"],
                user_id="test_user",
                sources_used=2
            )
            
        # Check metrics
        trends = self.metrics_service.get_usage_trends()
        
        # Check subject distribution
        self.assertEqual(trends["subject_distribution"]["physics"], 1)
        self.assertEqual(trends["subject_distribution"]["mathematics"], 1)
        
        # Check averages from file
        with open(self.metrics_file) as f:
            data = json.load(f)
            avg_response_time = sum(data["response_times"]) / len(data["response_times"])
            avg_confidence = sum(data["confidence_scores"]) / len(data["confidence_scores"])
        
        self.assertAlmostEqual(
            avg_response_time,
            (0.6 + 0.8) / 2,
            places=2
        )
        self.assertAlmostEqual(
            trends["average_confidence"],
            (0.9 + 0.85) / 2,
            places=2
        )
        
    def test_daily_usage(self):
        """Test daily usage tracking."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Record questions
        for _ in range(3):
            self.metrics_service.record_question(
                question="Test question",
                response_time=0.5,
                confidence=0.8,
                subject="test",
                user_id="test_user",
                sources_used=1
            )
            
        # Check daily usage
        trends = self.metrics_service.get_usage_trends()
        self.assertEqual(trends["daily_usage"][today], 3)
        
if __name__ == '__main__':
    unittest.main()