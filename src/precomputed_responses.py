"""
Precomputed responses system for common questions and fallback scenarios.
"""

import json
from typing import Dict, Optional, List, Tuple
from pathlib import Path
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class PrecomputedResponses:
    def __init__(
        self,
        responses_file: str = "data/precomputed_responses.json",
        similarity_threshold: float = 0.8
    ):
        self.responses_file = Path(responses_file)
        self.similarity_threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer()
        self.responses = self.load_responses()
        self.initialize_vectorizer()
        
    def load_responses(self) -> Dict:
        """Load precomputed responses from file."""
        if not self.responses_file.exists():
            self.initialize_responses()
        try:
            with open(self.responses_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading responses: {e}")
            return self.get_default_responses()
            
    def initialize_responses(self):
        """Initialize responses file with defaults."""
        self.responses_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.responses_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_default_responses(), f, indent=2, ensure_ascii=False)
            
    def get_default_responses(self) -> Dict:
        """Get default precomputed responses."""
        return {
            "general": {
                "greeting": {
                    "patterns": [
                        "bonjour",
                        "salut",
                        "hello",
                        "hi",
                        "hey"
                    ],
                    "response": "Bonjour! Je suis votre assistant étudiant. Comment puis-je vous aider aujourd'hui?",
                    "metadata": {
                        "confidence": 1.0,
                        "category": "greeting"
                    }
                },
                "farewell": {
                    "patterns": [
                        "au revoir",
                        "bye",
                        "à bientôt",
                        "à plus tard"
                    ],
                    "response": "Au revoir! N'hésitez pas à revenir si vous avez d'autres questions.",
                    "metadata": {
                        "confidence": 1.0,
                        "category": "farewell"
                    }
                }
            },
            "fallback": {
                "unclear_question": {
                    "response": "Je ne suis pas sûr de comprendre votre question. Pourriez-vous la reformuler différemment?",
                    "metadata": {
                        "confidence": 0.3,
                        "category": "clarification"
                    }
                },
                "no_context": {
                    "response": "Je ne trouve pas assez de contexte pour répondre à cette question. Pourriez-vous fournir plus de détails?",
                    "metadata": {
                        "confidence": 0.3,
                        "category": "clarification"
                    }
                }
            }
        }
        
    def initialize_vectorizer(self):
        """Initialize TF-IDF vectorizer with all patterns."""
        patterns = []
        for category in self.responses.values():
            if isinstance(category, dict):
                for item in category.values():
                    if isinstance(item, dict) and "patterns" in item:
                        patterns.extend(item["patterns"])
                        
        if patterns:
            self.vectorizer.fit(patterns)
            
    def find_best_match(
        self,
        query: str,
        category: Optional[str] = None
    ) -> Tuple[Optional[str], Optional[Dict], float]:
        """Find best matching precomputed response."""
        if not query:
            return None, None, 0.0
            
        try:
            query_vector = self.vectorizer.transform([query])
            
            best_score = 0.0
            best_response = None
            best_metadata = None
            
            search_space = (
                {category: self.responses[category]}
                if category and category in self.responses
                else self.responses
            )
            
            for cat_name, cat_content in search_space.items():
                if isinstance(cat_content, dict):
                    for item in cat_content.values():
                        if isinstance(item, dict) and "patterns" in item:
                            patterns_vector = self.vectorizer.transform(item["patterns"])
                            similarity = cosine_similarity(query_vector, patterns_vector)
                            max_similarity = np.max(similarity)
                            
                            if max_similarity > best_score:
                                best_score = max_similarity
                                best_response = item["response"]
                                best_metadata = item.get("metadata", {})
                                
            if best_score >= self.similarity_threshold:
                return best_response, best_metadata, best_score
                
        except Exception as e:
            logger.error(f"Error finding match: {e}")
            
        return None, None, 0.0
        
    def add_response(
        self,
        category: str,
        key: str,
        patterns: List[str],
        response: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Add a new precomputed response."""
        try:
            if category not in self.responses:
                self.responses[category] = {}
                
            self.responses[category][key] = {
                "patterns": patterns,
                "response": response,
                "metadata": metadata or {}
            }
            
            # Update vectorizer
            self.vectorizer = TfidfVectorizer()
            self.initialize_vectorizer()
            
            # Save to file
            with open(self.responses_file, 'w', encoding='utf-8') as f:
                json.dump(self.responses, f, indent=2, ensure_ascii=False)
                
            return True
            
        except Exception as e:
            logger.error(f"Error adding response: {e}")
            return False
            
    def get_fallback_response(self) -> Tuple[str, Dict]:
        """Get a general fallback response."""
        fallback = self.responses.get("fallback", {}).get("unclear_question", {})
        return (
            fallback.get("response", "Je ne peux pas répondre à cette question pour le moment."),
            fallback.get("metadata", {"confidence": 0.3, "category": "fallback"})
        )