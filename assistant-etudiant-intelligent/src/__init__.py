"""
Assistant Étudiant Intelligent - Module principal

Un système RAG complet pour aider les étudiants à naviguer dans leurs cours,
TD et examens corrigés.
"""

__version__ = "1.0.0"
__author__ = "Assistant Étudiant Intelligent"
__description__ = "Système RAG pour l'aide aux étudiants"

from .document_loader import DocumentLoader
from .vector_store import VectorStore
from .rag_engine import RAGEngine, RAGResponse

__all__ = [
    "DocumentLoader",
    "VectorStore", 
    "RAGEngine",
    "RAGResponse"
]
