"""
Test database operations with SQLAlchemy models.
"""

import unittest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.crud import CRUDOperations
from src.models_db import Student, Conversation, Message

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create test database."""
        cls.db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        cls.db_url = f"sqlite:///{cls.db_file.name}"
        cls.engine = create_engine(cls.db_url)
        cls.TestingSessionLocal = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        cls.db_file.close()
        os.unlink(cls.db_file.name)

    def setUp(self):
        """Create new session for each test."""
        self.db = self.TestingSessionLocal()
        self.crud = CRUDOperations(self.db)

    def tearDown(self):
        """Close session after each test."""
        self.db.close()

    def test_create_student(self):
        """Test student creation."""
        student = self.crud.create_student(
            username="test_user",
            email="test@example.com"
        )
        self.assertIsNotNone(student.id)
        self.assertEqual(student.username, "test_user")
        self.assertEqual(student.email, "test@example.com")

    def test_create_conversation(self):
        """Test conversation creation."""
        student = self.crud.create_student(username="test_user2")
        conversation = self.crud.create_conversation(
            student_id=student.id,
            title="Test Chat",
            chat_metadata={"subject": "physics"}
        )
        self.assertIsNotNone(conversation.id)
        self.assertEqual(conversation.title, "Test Chat")
        self.assertEqual(conversation.chat_metadata["subject"], "physics")

    def test_create_message(self):
        """Test message creation."""
        student = self.crud.create_student(username="test_user3")
        conversation = self.crud.create_conversation(
            student_id=student.id,
            title="Test Chat 2"
        )
        message = self.crud.create_message(
            conversation_id=conversation.id,
            sender="user",
            content="What is energy?",
            response_time=None,
            metadata={"context": "physics chapter"}
        )
        self.assertIsNotNone(message.id)
        self.assertEqual(message.sender, "user")
        self.assertEqual(message.content, "What is energy?")
        self.assertEqual(message.message_metadata["context"], "physics chapter")

    def test_get_conversation_messages(self):
        """Test retrieving conversation messages."""
        student = self.crud.create_student(username="test_user4")
        conversation = self.crud.create_conversation(
            student_id=student.id,
            title="Test Chat 3"
        )
        
        # Add two messages
        self.crud.create_message(
            conversation_id=conversation.id,
            sender="user",
            content="Question 1"
        )
        self.crud.create_message(
            conversation_id=conversation.id,
            sender="assistant",
            content="Answer 1"
        )
        
        messages = self.crud.get_conversation_messages(conversation.id)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0].content, "Question 1")
        self.assertEqual(messages[1].content, "Answer 1")

if __name__ == '__main__':
    unittest.main()