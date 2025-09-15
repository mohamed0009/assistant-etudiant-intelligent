"""
Professional RAG Engine for Enhanced AI System
Advanced RAG implementation with multiple model support and optimizations.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime
import time

from langchain.docstore.document import Document
from langchain_community.llms import HuggingFacePipeline, Ollama
from langchain.prompts import PromptTemplate
from transformers import pipeline

@dataclass
class RAGResponse:
    """Enhanced RAG response with detailed information."""
    answer: str
    confidence: float
    sources: List[Document]
    processing_time: float
    query: str
    model_used: str
    source_scores: List[float]
    metadata: Dict[str, Any]

class EnhancedFallbackLLM:
    """Fallback LLM with educational precomputed responses."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_response(self, query: str) -> str:
        """Get response from precomputed knowledge base."""
        # Basic keyword matching for educational content
        query_lower = query.lower()
        
        if "ohm" in query_lower:
            return self._get_ohm_law_response()
        elif "thévenin" in query_lower:
            return self._get_thevenin_response()
        elif "transistor" in query_lower:
            return self._get_transistor_response()
        elif "dérivée" in query_lower:
            return self._get_derivative_response()
        else:
            return self._get_general_response(query)
    
    def _get_ohm_law_response(self) -> str:
        return """La loi d'Ohm est une loi fondamentale en électricité qui décrit la relation entre la tension (U), le courant (I) et la résistance (R) dans un circuit électrique.

**Formule**: U = R × I

Où:
- U est la tension en volts (V)
- R est la résistance en ohms (Ω)
- I est l'intensité du courant en ampères (A)

**Exemple pratique**:
Si une résistance de 100Ω est traversée par un courant de 0.5A,
la tension à ses bornes sera: U = 100Ω × 0.5A = 50V"""

    def _get_thevenin_response(self) -> str:
        return """Le théorème de Thévenin permet de simplifier un circuit électrique complexe en un circuit équivalent simple.

**Principe**: 
Tout circuit linéaire peut être remplacé par:
1. Une source de tension (Eth)
2. Une résistance en série (Rth)

**Étapes de calcul**:
1. Calculer Eth en circuit ouvert
2. Calculer Rth en court-circuitant les sources
3. Le circuit équivalent donne les mêmes résultats"""
    
    def _get_transistor_response(self) -> str:
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
    
    def _get_derivative_response(self) -> str:
        return """La dérivée mesure le taux de variation instantané d'une fonction.

**Règles principales**:
1. Dérivée d'une constante = 0
2. Dérivée de x^n = n×x^(n-1)
3. Règle du produit: (u×v)' = u'×v + u×v'
4. Règle de la chaîne: (f∘g)' = (f'∘g)×g'

**Exemple**:
Pour f(x) = x², f'(x) = 2x
Pour g(x) = sin(x), g'(x) = cos(x)"""
    
    def _get_general_response(self, query: str) -> str:
        return f"""Je peux vous aider à comprendre ce concept. Voici une approche structurée :

1. **Définition de base**
2. **Principes fondamentaux**
3. **Applications pratiques**

Pour une réponse plus précise sur "{query}", ajoutez des documents dans le dossier 'data/'."""

class ProfessionalRAGEngine:
    """Enhanced RAG engine with professional features."""
    
    def __init__(
        self,
        vector_store: Any,
        model_type: str = "auto",
        use_reranking: bool = True,
        max_sources: int = 5,
        min_confidence: float = 0.3
    ):
        self.vector_store = vector_store
        self.model_type = model_type
        self.use_reranking = use_reranking
        self.max_sources = max_sources
        self.min_confidence = min_confidence
        
        # Initialize components
        self.logger = logging.getLogger(__name__)
        self.llm = self._initialize_llm()
        self.fallback_llm = EnhancedFallbackLLM()
        
        # Create enhanced prompt template
        self.prompt_template = PromptTemplate(
            template="""En tant qu'Assistant Étudiant IA professionnel, utilisez les sources suivantes pour répondre à la question de manière pédagogique et structurée.

Sources:
{sources}

Question: {question}

Instructions:
1. Analysez attentivement les sources fournies
2. Structurez votre réponse de manière claire
3. Utilisez des exemples si approprié
4. Citez les concepts importants
5. Restez factuel et précis

Réponse:""",
            input_variables=["sources", "question"]
        )
    
    def _initialize_llm(self) -> Any:
        """Initialize LLM based on configuration."""
        try:
            if self.model_type == "ollama":
                return self._setup_ollama()
            elif self.model_type == "huggingface":
                return self._setup_huggingface()
            else:  # auto
                return self._setup_auto()
                
        except Exception as e:
            self.logger.error(f"❌ Error initializing LLM: {e}")
            return None
    
    def _setup_ollama(self) -> Ollama:
        """Setup Ollama LLM."""
        try:
            return Ollama(model="llama2")
        except:
            self.logger.warning("⚠️ Ollama not available")
            return None
    
    def _setup_huggingface(self) -> HuggingFacePipeline:
        """Setup HuggingFace pipeline."""
        try:
            pipe = pipeline(
                "text-generation",
                model="google/flan-t5-base",
                max_length=512
            )
            return HuggingFacePipeline(pipeline=pipe)
        except:
            self.logger.warning("⚠️ HuggingFace model not available")
            return None
    
    def _setup_auto(self) -> Any:
        """Try different LLMs in order of preference."""
        llm = self._setup_ollama()
        if llm:
            return llm
        
        llm = self._setup_huggingface()
        if llm:
            return llm
        
        self.logger.warning("⚠️ No LLM available, using fallback")
        return None
    
    def ask_question(
        self,
        question: str,
        subject_filter: Optional[str] = None
    ) -> RAGResponse:
        """Process question and generate enhanced response."""
        start_time = time.time()
        
        try:
            # Search for relevant documents
            results = self.vector_store.search_documents(
                question,
                k=self.max_sources,
                use_reranking=self.use_reranking
            )
            
            # Filter by subject if specified
            if subject_filter:
                results = [
                    (doc, score) for doc, score in results
                    if doc.metadata.get("subject", "").lower() == subject_filter.lower()
                ]
            
            # Prepare sources text
            sources_text = "\n\n".join([
                f"Source {i+1}:\n{doc.page_content}"
                for i, (doc, _) in enumerate(results)
            ])
            
            # Generate response
            if self.llm and results:
                # Use RAG with LLM
                prompt = self.prompt_template.format(
                    sources=sources_text,
                    question=question
                )
                answer = self.llm(prompt)
                model_used = self.model_type
                confidence = max(s for _, s in results)
            else:
                # Use fallback
                answer = self.fallback_llm.get_response(question)
                model_used = "fallback"
                confidence = self.min_confidence
            
            # Create response
            processing_time = time.time() - start_time
            
            return RAGResponse(
                answer=answer,
                confidence=confidence,
                sources=[doc for doc, _ in results],
                processing_time=processing_time,
                query=question,
                model_used=model_used,
                source_scores=[float(score) for _, score in results],
                metadata={
                    "subject_filter": subject_filter,
                    "use_reranking": self.use_reranking,
                    "total_sources": len(results),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error processing question: {e}")
            
            # Return fallback response
            return RAGResponse(
                answer=self.fallback_llm.get_response(question),
                confidence=self.min_confidence,
                sources=[],
                processing_time=time.time() - start_time,
                query=question,
                model_used="fallback",
                source_scores=[],
                metadata={"error": str(e)}
            )
    
    def get_suggested_questions(self, subject: Optional[str] = None) -> List[str]:
        """Get suggested questions based on available documents."""
        try:
            suggestions = [
                "Explique-moi la loi d'Ohm avec un exemple pratique.",
                "Qu'est-ce que le théorème de Thévenin et comment l'appliquer ?",
                "Comment calculer la puissance électrique dans un circuit ?",
                "Explique-moi les dérivées en mathématiques étape par étape.",
                "Qu'est-ce que le pH et comment le calculer ?",
                "Comment fonctionne un transistor en électronique ?",
                "Quelles sont les lois de Newton en physique ?",
                "Comment résoudre une intégrale mathématique ?"
            ]
            
            if subject:
                subject_lower = subject.lower()
                return [q for q in suggestions if subject_lower in q.lower()]
            
            return suggestions[:5]  # Return top 5 by default
            
        except Exception as e:
            self.logger.error(f"Error getting suggestions: {e}")
            return []
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get detailed system status."""
        return {
            "llm_model": self.model_type,
            "llm_available": self.llm is not None,
            "use_reranking": self.use_reranking,
            "max_sources": self.max_sources,
            "min_confidence": self.min_confidence,
            "device": "cpu",  # Update if GPU is used
            "timestamp": datetime.now().isoformat()
        }

def create_professional_rag_engine(
    vector_store: Any,
    model_type: str = "auto",
    use_reranking: bool = True
) -> ProfessionalRAGEngine:
    """Create an instance of the professional RAG engine."""
    return ProfessionalRAGEngine(
        vector_store=vector_store,
        model_type=model_type,
        use_reranking=use_reranking
    )
