"""
Enum types for the RAG system.
"""

from enum import Enum

class QuestionType(str, Enum):
    """Types of questions that can be asked."""
    CONCEPTUAL = "conceptual"
    PROBLEM_SOLVING = "problem_solving"
    DEFINITION = "definition"
    EXAMPLE = "example"
    APPLICATION = "application"

class SubjectType(str, Enum):
    """Academic subjects covered by the system."""
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    MATHEMATICS = "mathematics"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ASTRONOMY = "astronomy"
    GEOLOGY = "geology"
    ELECTRONICS = "electronics"