"""
Test the RAG engine integration with Ollama.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import time

from src.rag_engine import ProfessionalRAGEngine, RAGResponse
from src.vector_store import EnhancedVectorStore
from langchain.docstore.document import Document

class TestRAGEngine(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.mock_vector_store = MagicMock()
        self.mock_vector_store.search_documents.return_value = [
            (Document(page_content="Test content 1", metadata={"subject": "physics"}), 0.9),
            (Document(page_content="Test content 2", metadata={"subject": "physics"}), 0.8)
        ]
        
        self.rag_engine = ProfessionalRAGEngine(
            vector_store=self.mock_vector_store,
            model_type="ollama",
            use_reranking=True
        )
        
    def test_initialization(self):
        """Test RAG engine initialization."""
        self.assertIsNotNone(self.rag_engine)
        self.assertEqual(self.rag_engine.model_type, "ollama")
        self.assertTrue(self.rag_engine.use_reranking)
        
    def test_ask_question_with_results(self):
        """Test question answering with valid results."""
        question = "What is Newton's first law?"
        
        # Mock LLM response
        self.rag_engine.llm = MagicMock()
        self.rag_engine.llm.return_value = "Newton's first law states that..."
        
        response = self.rag_engine.ask_question(question)
        
        self.assertIsInstance(response, RAGResponse)
        self.assertEqual(response.model_used, "ollama")
        self.assertGreater(response.confidence, 0.8)
        self.assertEqual(len(response.sources), 2)
        
    def test_ask_question_with_subject_filter(self):
        """Test question answering with subject filter."""
        question = "What is energy?"
        subject = "physics"
        
        # Mock LLM response
        self.rag_engine.llm = MagicMock()
        self.rag_engine.llm.return_value = "Energy is..."
        
        response = self.rag_engine.ask_question(question, subject_filter=subject)
        
        self.assertIsInstance(response, RAGResponse)
        self.assertTrue(all(
            doc.metadata.get("subject") == "physics"
            for doc in response.sources
        ))
        
    def test_fallback_mechanism(self):
        """Test fallback when LLM is not available."""
        question = "What is a transistor?"
        
        # Force fallback by setting LLM to None
        self.rag_engine.llm = None
        
        response = self.rag_engine.ask_question(question)
        
        self.assertIsInstance(response, RAGResponse)
        self.assertEqual(response.model_used, "fallback")
        self.assertEqual(response.confidence, self.rag_engine.min_confidence)
        
    def test_suggestions(self):
        """Test suggested questions functionality."""
        suggestions = self.rag_engine.get_suggested_questions()
        
        self.assertIsInstance(suggestions, list)
        self.assertTrue(all(isinstance(q, str) for q in suggestions))
        self.assertLessEqual(len(suggestions), 5)
        
        # Test with subject filter
        physics_suggestions = self.rag_engine.get_suggested_questions("physics")
        self.assertTrue(all(
            "physique" in q.lower() or "newton" in q.lower()
            for q in physics_suggestions
        ))
        
    def test_system_status(self):
        """Test system status reporting."""
        status = self.rag_engine.get_system_status()
        
        self.assertIsInstance(status, dict)
        self.assertEqual(status["llm_model"], "ollama")
        self.assertIn("llm_available", status)
        self.assertIn("use_reranking", status)
        self.assertIn("timestamp", status)
        
if __name__ == '__main__':
    unittest.main()