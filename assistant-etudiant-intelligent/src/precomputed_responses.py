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
            
    def get_ohm_law_response(self) -> str:
        """Get precomputed response for Ohm's Law."""
        return """La loi d'Ohm est une loi fondamentale en électricité qui décrit la relation entre la tension (U), le courant (I) et la résistance (R) dans un circuit électrique.

**Formule**: U = R × I

Où:
- U est la tension en volts (V)
- R est la résistance en ohms (Ω)
- I est l'intensité du courant en ampères (A)

**Exemple pratique**:
Si une résistance de 100Ω est traversée par un courant de 0.5A,
la tension à ses bornes sera: U = 100Ω × 0.5A = 50V"""

    def get_thevenin_response(self) -> str:
        """Get precomputed response for Thévenin's theorem."""
        return """Le théorème de Thévenin permet de simplifier un circuit électrique complexe en un circuit équivalent simple.

**Principe**: 
Tout circuit linéaire peut être remplacé par:
1. Une source de tension (Eth)
2. Une résistance en série (Rth)

**Étapes de calcul**:
1. Calculer Eth en circuit ouvert
2. Calculer Rth en court-circuitant les sources
3. Le circuit équivalent donne les mêmes résultats"""

    def get_transistor_response(self) -> str:
        """Get precomputed response for transistors."""
        return """Un transistor est un composant électronique semi-conducteur utilisé pour amplifier ou commuter des signaux électriques.

**Principaux types**:
1. Bipolaire (BJT)
   - NPN et PNP
   - Utilisé pour l'amplification
   
2. Effet de champ (FET)
   - MOSFET, JFET
   - Utilisé pour la commutation

**Paramètres clés**:
- Gain en courant (β)
- Tension collecteur-émetteur (Vce)
- Courant collecteur (Ic)"""

    def get_derivative_response(self) -> str:
        """Get precomputed response for derivatives."""
        return """La dérivée mesure le taux de variation instantané d'une fonction.

**Règles principales**:
1. Dérivée d'une constante = 0
2. Dérivée de x^n = n×x^(n-1)
3. Règle du produit: (u×v)' = u'×v + u×v'
4. Règle de la chaîne: (f∘g)' = (f'∘g)×g'

**Exemple**:
Pour f(x) = x², f'(x) = 2x
Pour g(x) = sin(x), g'(x) = cos(x)"""

    def get_integral_response(self) -> str:
        """Get precomputed response for integrals."""
        return """L'intégrale calcule l'aire sous une courbe ou l'accumulation d'une quantité.

**Règles principales**:
1. Intégrale d'une constante: ∫a dx = ax + C
2. Intégrale de x^n: ∫x^n dx = x^(n+1)/(n+1) + C (n ≠ -1)
3. Intégrale de 1/x: ∫1/x dx = ln|x| + C
4. Intégrale de fonctions trigonométriques: ∫sin(x) dx = -cos(x) + C

**Exemple**:
∫(3x² + 2x) dx = x³ + x² + C"""

    def get_ph_response(self) -> str:
        """Get precomputed response for pH."""
        return """Le pH mesure l'acidité ou la basicité d'une solution.

**Définition**: pH = -log[H⁺]

**Échelle**:
- pH < 7: solution acide
- pH = 7: solution neutre
- pH > 7: solution basique

**Calcul**:
Pour une solution avec [H⁺] = 10⁻³ mol/L, pH = -log(10⁻³) = 3

**Applications**:
- Chimie analytique
- Biologie
- Industrie alimentaire"""

    def get_fallback_response(self) -> Tuple[str, Dict]:
        """Get a general fallback response."""
        fallback = self.responses.get("fallback", {}).get("unclear_question", {})
        return (
            fallback.get("response", "Je ne peux pas répondre à cette question pour le moment."),
            fallback.get("metadata", {"confidence": 0.3, "category": "fallback"})
        )