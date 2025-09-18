"""
Ollama RAG Engine - Professional Implementation
Core RAG engine specifically optimized for Ollama integration.
"""

import asyncio
import httpx
import json
import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class OllamaResponse:
    """Response from Ollama RAG processing."""
    answer: str
    confidence: float
    sources: List[Dict[str, Any]]
    processing_time: float
    query: str
    model_used: str
    ollama_response_time: float
    tokens_generated: int
    source_scores: List[float]
    metadata: Dict[str, Any]
    quality_assessment: str
    fallback_used: bool

class OllamaModelManager:
    """Manages Ollama models and connections."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        self._available_models = []
        self._connection_tested = False
        
    async def test_connection(self) -> bool:
        """Test connection to Ollama server."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            self._connection_tested = response.status_code == 200
            if self._connection_tested:
                data = response.json()
                self._available_models = [model['name'] for model in data.get('models', [])]
            return self._connection_tested
        except Exception as e:
            logger.error(f"Ollama connection test failed: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to Ollama."""
        return self._connection_tested
    
    async def list_models(self) -> List[str]:
        """List available models."""
        if not await self.test_connection():
            return []
        return self._available_models
    
    async def list_models_detailed(self) -> List[Dict[str, Any]]:
        """List models with detailed information."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get('models', [])
            return []
        except Exception as e:
            logger.error(f"Error listing detailed models: {e}")
            return []
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
    
    async def delete_model(self, model_name: str) -> bool:
        """Delete a model."""
        try:
            response = await self.client.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name}
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error deleting model {model_name}: {e}")
            return False
    
    async def generate_response(
        self, 
        model: str, 
        prompt: str, 
        temperature: float = 0.1,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """Generate response using Ollama."""
        try:
            start_time = time.time()
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                response_time = time.time() - start_time
                
                return {
                    "success": True,
                    "response": data.get("response", ""),
                    "model": model,
                    "response_time": response_time,
                    "tokens": len(data.get("response", "").split()),
                    "done": data.get("done", False)
                }
            else:
                return {
                    "success": False,
                    "error": f"Ollama API error: {response.status_code}",
                    "model": model
                }
                
        except Exception as e:
            logger.error(f"Error generating response with {model}: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": model
            }
    
    async def update_config(self, config: Dict[str, Any]):
        """Update Ollama configuration."""
        if "base_url" in config:
            self.base_url = config["base_url"].rstrip('/')
            self.client = httpx.AsyncClient(timeout=config.get("timeout", 30))
            self._connection_tested = False
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get Ollama-specific metrics."""
        return {
            "connected": self._connection_tested,
            "available_models": len(self._available_models),
            "models": self._available_models,
            "base_url": self.base_url
        }

class OllamaRAGEngine:
    """Professional RAG engine with Ollama integration."""
    
    def __init__(
        self, 
        vector_store,
        ollama_manager: OllamaModelManager,
        config: Dict[str, Any] = None
    ):
        self.vector_store = vector_store
        self.ollama_manager = ollama_manager
        self.config = config or {}
        
        # Configuration
        self.primary_model = self.config.get("primary_model", "llama2")
        self.fallback_models = self.config.get("fallback_models", ["mistral", "codellama"])
        self.temperature = self.config.get("temperature", 0.1)
        self.max_tokens = self.config.get("max_tokens", 1000)
        self.max_sources = self.config.get("max_sources", 5)
        self.use_reranking = self.config.get("use_reranking", True)
        
        # Precomputed responses for educational content
        self.precomputed_responses = self._load_precomputed_responses()
        
    def _load_precomputed_responses(self) -> Dict[str, str]:
        """Load precomputed educational responses."""
        return {
            "ohm": """**LOI D'OHM - EXPLICATION COMPLÈTE**

**Formule fondamentale :** U = R × I

**Où :**
- U = tension (Volts)
- R = résistance (Ohms) 
- I = intensité (Ampères)

**Exemple pratique :**
Une résistance de 100Ω traversée par 0.5A :
U = 100 × 0.5 = 50V

**Applications :**
- Calcul de circuits électriques
- Dimensionnement de composants
- Analyse de puissance (P = U×I)""",
            
            "transistor": """**TRANSISTOR - FONCTIONNEMENT**

**Types principaux :**
- NPN et PNP (bipolaires)
- MOSFET (effet de champ)

**Principe :**
Composant à 3 bornes contrôlant le courant :
- Base/Grille : contrôle
- Collecteur/Drain : sortie
- Émetteur/Source : référence

**Applications :**
- Amplification de signaux
- Commutation ON/OFF
- Circuits logiques""",
            
            "derivee": """**DÉRIVÉES - CALCUL DIFFÉRENTIEL**

**Définition :**
f'(x) = lim(h→0) [f(x+h) - f(x)] / h

**Règles de base :**
- (x^n)' = n×x^(n-1)
- (sin x)' = cos x
- (e^x)' = e^x
- (ln x)' = 1/x

**Exemple :**
f(x) = x³ + 2x² - 5x + 1
f'(x) = 3x² + 4x - 5""",
            
            "ph": """**pH - ACIDITÉ ET BASICITÉ**

**Formule :** pH = -log[H⁺]

**Échelle :**
- pH < 7 : acide
- pH = 7 : neutre
- pH > 7 : basique

**Calcul :**
[H⁺] = 10^(-pH)

**Exemple :**
Si [H⁺] = 10⁻³ M, alors pH = 3"""
        }
    
    async def initialize(self):
        """Initialize the RAG engine."""
        try:
            # Test Ollama connection
            if not await self.ollama_manager.test_connection():
                logger.warning("Ollama not available, using fallback responses")
            
            # Verify models are available
            available_models = await self.ollama_manager.list_models()
            if self.primary_model not in available_models:
                logger.warning(f"Primary model {self.primary_model} not available")
                
                # Try fallback models
                for model in self.fallback_models:
                    if model in available_models:
                        self.primary_model = model
                        logger.info(f"Using fallback model: {model}")
                        break
                else:
                    logger.warning("No suitable models found, using template responses")
            
            logger.info("✅ Ollama RAG engine initialized")
            
        except Exception as e:
            logger.error(f"Error initializing RAG engine: {e}")
    
    async def ask_question_async(
        self,
        question: str,
        subject_filter: Optional[str] = None,
        model_preference: Optional[str] = None,
        max_sources: Optional[int] = None,
        temperature: Optional[float] = None,
        use_reranking: Optional[bool] = None
    ) -> OllamaResponse:
        """Process question with Ollama RAG pipeline."""
        start_time = time.time()
        
        # Use provided parameters or defaults
        model_to_use = model_preference or self.primary_model
        sources_count = max_sources or self.max_sources
        temp = temperature or self.temperature
        rerank = use_reranking if use_reranking is not None else self.use_reranking
        
        try:
            # Step 1: Check for precomputed responses
            quick_response = self._get_precomputed_response(question)
            if quick_response:
                return OllamaResponse(
                    answer=quick_response,
                    confidence=0.9,
                    sources=[],
                    processing_time=time.time() - start_time,
                    query=question,
                    model_used="precomputed",
                    ollama_response_time=0.0,
                    tokens_generated=len(quick_response.split()),
                    source_scores=[],
                    metadata={"response_type": "precomputed"},
                    quality_assessment="high",
                    fallback_used=False
                )
            
            # Step 2: Retrieve relevant documents
            relevant_docs = await self._retrieve_documents(question, subject_filter, sources_count)
            
            # Step 3: Rerank documents if enabled
            if rerank and relevant_docs:
                relevant_docs = await self._rerank_documents(question, relevant_docs)
            
            # Step 4: Generate response with Ollama
            response_data = await self._generate_ollama_response(
                question, relevant_docs, model_to_use, temp
            )
            
            # Step 5: Calculate confidence and quality
            confidence = self._calculate_confidence(relevant_docs, response_data)
            quality = self._assess_quality(response_data, relevant_docs)
            
            total_time = time.time() - start_time
            
            return OllamaResponse(
                answer=response_data["answer"],
                confidence=confidence,
                sources=self._format_sources(relevant_docs),
                processing_time=total_time,
                query=question,
                model_used=response_data["model_used"],
                ollama_response_time=response_data["ollama_time"],
                tokens_generated=response_data["tokens"],
                source_scores=[doc.get("score", 0.0) for doc in relevant_docs],
                metadata={
                    "sources_count": len(relevant_docs),
                    "reranking_used": rerank,
                    "temperature": temp
                },
                quality_assessment=quality,
                fallback_used=response_data["fallback_used"]
            )
            
        except Exception as e:
            logger.error(f"Error in RAG processing: {e}")
            # Return fallback response
            return await self._generate_error_fallback(question, str(e), start_time)
    
    def _get_precomputed_response(self, question: str) -> Optional[str]:
        """Get precomputed response for common educational questions."""
        question_lower = question.lower()
        
        # Check for keyword matches
        for keyword, response in self.precomputed_responses.items():
            if keyword in question_lower:
                return response
        
        return None
    
    async def _retrieve_documents(
        self, 
        question: str, 
        subject_filter: Optional[str], 
        max_docs: int
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents from vector store."""
        try:
            if not self.vector_store:
                return []
            
            # Search for similar documents
            documents = await self.vector_store.search_similar_async(
                query=question,
                k=max_docs,
                subject_filter=subject_filter
            )
            
            # Format documents with metadata
            formatted_docs = []
            for i, doc in enumerate(documents):
                formatted_docs.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": 1.0 - (i * 0.1),  # Simple scoring
                    "index": i
                })
            
            return formatted_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    async def _rerank_documents(
        self, 
        question: str, 
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Rerank documents based on semantic similarity."""
        try:
            # Simple reranking based on keyword overlap
            question_words = set(question.lower().split())
            
            for doc in documents:
                content_words = set(doc["content"].lower().split())
                overlap = len(question_words.intersection(content_words))
                # Boost score based on keyword overlap
                doc["score"] = doc["score"] + (overlap * 0.05)
            
            # Sort by score
            documents.sort(key=lambda x: x["score"], reverse=True)
            return documents
            
        except Exception as e:
            logger.error(f"Error reranking documents: {e}")
            return documents
    
    async def _generate_ollama_response(
        self, 
        question: str, 
        documents: List[Dict[str, Any]], 
        model: str, 
        temperature: float
    ) -> Dict[str, Any]:
        """Generate response using Ollama."""
        try:
            # Build context from documents
            context = self._build_context(documents)
            
            # Create educational prompt
            prompt = self._create_educational_prompt(question, context)
            
            # Try primary model first
            ollama_start = time.time()
            response = await self.ollama_manager.generate_response(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=self.max_tokens
            )
            ollama_time = time.time() - ollama_start
            
            if response["success"]:
                return {
                    "answer": self._clean_response(response["response"]),
                    "model_used": model,
                    "ollama_time": ollama_time,
                    "tokens": response.get("tokens", 0),
                    "fallback_used": False
                }
            else:
                # Try fallback models
                for fallback_model in self.fallback_models:
                    try:
                        fallback_response = await self.ollama_manager.generate_response(
                            model=fallback_model,
                            prompt=prompt,
                            temperature=temperature,
                            max_tokens=self.max_tokens
                        )
                        if fallback_response["success"]:
                            return {
                                "answer": self._clean_response(fallback_response["response"]),
                                "model_used": fallback_model,
                                "ollama_time": fallback_response.get("response_time", 0),
                                "tokens": fallback_response.get("tokens", 0),
                                "fallback_used": True
                            }
                    except Exception:
                        continue
                
                # All models failed, use template response
                return self._generate_template_response(question, context)
                
        except Exception as e:
            logger.error(f"Error generating Ollama response: {e}")
            return self._generate_template_response(question, context)
    
    def _build_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build context string from documents."""
        if not documents:
            return ""
        
        context_parts = []
        for i, doc in enumerate(documents[:3]):  # Limit to top 3 documents
            source = doc["metadata"].get("source", f"Document {i+1}")
            content = doc["content"][:500]  # Limit content length
            context_parts.append(f"[Source: {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _create_educational_prompt(self, question: str, context: str) -> str:
        """Create educational prompt for Ollama."""
        if context:
            return f"""Tu es un professeur expérimenté et bienveillant. Un étudiant te pose une question et tu as accès à des documents de cours.

DOCUMENTS DE COURS :
{context}

QUESTION DE L'ÉTUDIANT :
{question}

INSTRUCTIONS :
- Réponds de manière claire et pédagogique
- Utilise les informations des documents fournis
- Donne des exemples concrets quand c'est possible
- Structure ta réponse avec des titres si nécessaire
- Reste précis et factuel
- Adapte le niveau à un étudiant universitaire

RÉPONSE COMPLÈTE :"""
        else:
            return f"""Tu es un professeur expérimenté. Un étudiant te pose une question.

QUESTION :
{question}

Réponds de manière claire, pédagogique et complète. Donne des exemples pratiques.

RÉPONSE :"""
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the AI response."""
        # Remove common artifacts
        response = response.strip()
        
        # Ensure proper formatting
        if not response.startswith("**") and len(response) > 100:
            # Add structure if missing
            lines = response.split('\n')
            if len(lines) > 2:
                response = f"**EXPLICATION**\n\n{response}"
        
        return response
    
    def _generate_template_response(self, question: str, context: str) -> Dict[str, Any]:
        """Generate template response when Ollama fails."""
        if context:
            answer = f"""**RÉPONSE BASÉE SUR VOS DOCUMENTS**

**Question :** {question}

**Explication :**
D'après les documents disponibles, voici les éléments clés pour répondre à votre question.

**Contenu pertinent :**
{context[:300]}...

**Points importants :**
- Consultez les documents complets pour plus de détails
- Les concepts sont expliqués avec des exemples pratiques
- N'hésitez pas à poser des questions plus spécifiques

Cette réponse est basée sur vos documents de cours."""
        else:
            answer = f"""**ASSISTANT ÉDUCATIF**

**Question :** {question}

Je peux vous aider avec de nombreux concepts éducatifs. Pour une réponse plus précise :

1. Ajoutez vos documents de cours au système
2. Précisez le contexte de votre question
3. Indiquez le niveau d'études souhaité

**Domaines disponibles :**
- Mathématiques (algèbre, calcul, géométrie)
- Sciences (physique, chimie, biologie)
- Ingénierie (électricité, électronique)
- Informatique (algorithmes, programmation)

Je reste à votre disposition pour vous accompagner dans vos études."""
        
        return {
            "answer": answer,
            "model_used": "template",
            "ollama_time": 0.0,
            "tokens": len(answer.split()),
            "fallback_used": True
        }
    
    def _calculate_confidence(
        self, 
        documents: List[Dict[str, Any]], 
        response_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the response."""
        base_confidence = 0.5
        
        # Boost confidence based on sources
        if documents:
            source_boost = min(0.3, len(documents) * 0.1)
            base_confidence += source_boost
        
        # Boost for successful Ollama response
        if not response_data["fallback_used"]:
            base_confidence += 0.2
        
        # Boost for longer, detailed responses
        token_count = response_data.get("tokens", 0)
        if token_count > 100:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _assess_quality(
        self, 
        response_data: Dict[str, Any], 
        documents: List[Dict[str, Any]]
    ) -> str:
        """Assess response quality."""
        if response_data["fallback_used"]:
            return "basic"
        elif documents and response_data.get("tokens", 0) > 150:
            return "high"
        elif documents:
            return "good"
        else:
            return "fair"
    
    def _format_sources(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format source documents for response."""
        formatted = []
        for doc in documents:
            formatted.append({
                "content": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                "source": doc["metadata"].get("source", "Unknown"),
                "subject": doc["metadata"].get("subject", "General"),
                "file_type": doc["metadata"].get("file_type", "unknown"),
                "score": doc.get("score", 0.0)
            })
        return formatted
    
    async def _generate_error_fallback(
        self, 
        question: str, 
        error: str, 
        start_time: float
    ) -> OllamaResponse:
        """Generate fallback response for errors."""
        answer = f"""**ASSISTANT ÉDUCATIF - MODE DÉGRADÉ**

Je rencontre actuellement des difficultés techniques, mais je peux quand même vous aider.

**Votre question :** {question}

**Suggestion :** Reformulez votre question de manière plus spécifique, ou consultez vos documents de cours pour des informations détaillées.

**Assistance disponible :**
- Concepts fondamentaux en mathématiques, physique, chimie
- Explications d'électricité et électronique
- Aide en informatique et programmation

Je reste à votre disposition pour vous accompagner dans vos études."""
        
        return OllamaResponse(
            answer=answer,
            confidence=0.3,
            sources=[],
            processing_time=time.time() - start_time,
            query=question,
            model_used="error_fallback",
            ollama_response_time=0.0,
            tokens_generated=len(answer.split()),
            source_scores=[],
            metadata={"error": error, "mode": "fallback"},
            quality_assessment="basic",
            fallback_used=True
        )
    
    async def refresh_vector_store(self, new_vector_store):
        """Refresh the vector store reference."""
        self.vector_store = new_vector_store
        logger.info("Vector store refreshed in RAG engine")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get RAG engine status."""
        return {
            "llm_model": self.primary_model,
            "fallback_models": self.fallback_models,
            "max_sources": self.max_sources,
            "temperature": self.temperature,
            "use_reranking": self.use_reranking,
            "vector_store_ready": self.vector_store is not None,
            "ollama_connected": self.ollama_manager.is_connected()
        }
    
    def get_suggested_questions(self, subject: Optional[str] = None) -> List[str]:
        """Get suggested questions based on available content."""
        base_suggestions = [
            "Explique-moi la loi d'Ohm avec un exemple pratique",
            "Comment fonctionne un transistor en électronique ?",
            "Qu'est-ce qu'une dérivée en mathématiques ?",
            "Comment calculer le pH d'une solution ?",
            "Quelles sont les lois de Newton en physique ?",
            "Explique le principe de la thermodynamique",
            "Comment résoudre une équation du second degré ?",
            "Qu'est-ce que la force électromotrice ?"
        ]
        
        if subject:
            subject_suggestions = {
                "Électricité": [
                    "Explique la loi d'Ohm",
                    "Comment calculer la puissance électrique ?",
                    "Qu'est-ce que le théorème de Thévenin ?"
                ],
                "Mathématiques": [
                    "Comment calculer une dérivée ?",
                    "Qu'est-ce qu'une intégrale ?",
                    "Comment résoudre une équation ?"
                ],
                "Physique": [
                    "Explique les lois de Newton",
                    "Qu'est-ce que l'énergie cinétique ?",
                    "Comment fonctionne la thermodynamique ?"
                ]
            }
            return subject_suggestions.get(subject, base_suggestions[:3])
        
        return base_suggestions

# Factory function for easy initialization
def create_professional_rag_engine(
    vector_store,
    model_type: str = "auto",
    use_reranking: bool = True
) -> OllamaRAGEngine:
    """Create professional RAG engine with optimal configuration."""
    # Initialize Ollama manager
    ollama_manager = OllamaModelManager()
    
    # Configuration
    config = {
        "primary_model": "llama2",
        "fallback_models": ["mistral", "codellama"],
        "temperature": 0.1,
        "max_tokens": 1000,
        "max_sources": 5,
        "use_reranking": use_reranking
    }
    
    return OllamaRAGEngine(vector_store, ollama_manager, config)
