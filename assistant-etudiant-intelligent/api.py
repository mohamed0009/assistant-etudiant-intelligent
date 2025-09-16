"""
API for Ollama RAG System
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)

# Import local modules
from src.rag_engine import RAGEngine
from src.vector_store import VectorStore
from src.database import get_db
from src.crud import CRUDOperations
from src.models import QuestionType, SubjectType

# Initialize FastAPI app
app = FastAPI(title="Ollama RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
vector_store = VectorStore(index_path="faiss_index", texts_dir="data")
rag_engine = RAGEngine(vector_store=vector_store, model_name="mistral")

# Pydantic models
class QuestionRequest(BaseModel):
    """Request model for questions."""
    question: str = Field(..., min_length=1, max_length=1000)
    subject: Optional[SubjectType] = None
    question_type: Optional[QuestionType] = None
    student_id: Optional[int] = None
    conversation_id: Optional[int] = None

class StudentCreate(BaseModel):
    """Request model for creating a student."""
    username: str
    email: Optional[str] = None

class ConversationCreate(BaseModel):
    """Request model for creating a conversation."""
    student_id: int
    title: str
    chat_metadata: Optional[Dict] = None
    processing_time: float
    query: str
    model_used: str
    source_scores: List[float]
    metadata: Dict[str, Any]
    conversation_id: Optional[int] = None
    user_message_id: Optional[int] = None
    assistant_message_id: Optional[int] = None

class SystemStatus(BaseModel):
    documents_loaded: bool
    total_vectors: int
    total_documents: int
    model_type: str
    device: str
    embedding_model: str
    index_type: str
    rag_engine_ready: bool
    last_updated: str
    performance_metrics: Dict[str, Any]

class DocumentProcessingConfig(BaseModel):
    chunk_size: int = Field(1000, ge=200, le=2000)
    chunk_overlap: int = Field(200, ge=0, le=500)
    enable_cache: bool = True
    use_enhanced_extraction: bool = True

class ModelConfig(BaseModel):
    model_type: str = Field("auto", regex="^(auto|ollama|huggingface)$")
    use_reranking: bool = True
    max_sources: int = Field(5, ge=1, le=10)
    min_confidence: float = Field(0.3, ge=0.0, le=1.0)

# FastAPI app with lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    logger.info("🚀 Starting Enhanced RAG System...")
    await startup_event()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Enhanced RAG System...")
    await shutdown_event()

app = FastAPI(
    title="Enhanced Student AI Assistant API",
    description="Professional RAG-based AI assistant with advanced features",
    version="2.0.0",
    lifespan=lifespan
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def startup_event():
    """Enhanced startup with better initialization."""
    global rag_engine, vector_store, document_loader, documents_loaded
    
    try:
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")
        
        # Initialize enhanced components
        document_loader = EnhancedDocumentLoader(
            data_dir="data",
            chunk_size=1000,
            chunk_overlap=200,
            enable_cache=True
        )
        logger.info("✅ Enhanced document loader initialized")
        
        vector_store = EnhancedVectorStore(
            embeddings_model="all-MiniLM-L6-v2",
            index_type="flat"
        )
        logger.info("✅ Enhanced vector store initialized")
        
        # Try to load existing vector store
        if vector_store.load_vector_store():
            logger.info("✅ Existing vector store loaded")
            rag_engine = create_professional_rag_engine(
                vector_store,
                model_type="auto",
                use_reranking=True
            )
            documents_loaded = True
            logger.info("✅ RAG engine initialized from existing data")
        else:
            # Load documents automatically
            logger.info("🔄 Loading documents...")
            success = await load_documents_enhanced()
            if success:
                logger.info("✅ Documents loaded and RAG engine initialized")
            else:
                logger.warning("⚠️ No documents found, running in knowledge-only mode")
        
        logger.info("🎉 Enhanced RAG System started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        logger.info("🔄 Starting in fallback mode...")

async def shutdown_event():
    """Cleanup on shutdown."""
    global vector_store
    
    try:
        if vector_store and documents_loaded:
            vector_store.save_vector_store()
            logger.info("✅ Vector store saved")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

async def load_documents_enhanced():
    """Enhanced document loading with better error handling."""
    global rag_engine, vector_store, document_loader, documents_loaded
    
    try:
        # Load documents with enhanced loader
        logger.info("📚 Loading documents with enhanced processing...")
        documents = document_loader.load_documents()
        
        if not documents:
            logger.warning("No documents found")
            return False
        
        # Generate processing report
        report = document_loader.get_processing_report(documents)
        logger.info(f"Document processing report:\n{report}")
        
        # Split documents with optimized settings
        logger.info("✂️ Splitting documents...")
        chunks = document_loader.split_documents(documents)
        
        if not chunks:
            logger.error("No chunks created")
            return False
        
        logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
        
        # Create enhanced vector store
        logger.info("🔍 Creating enhanced vector store...")
        success = vector_store.create_vector_store(chunks)
        
        if not success:
            logger.error("Failed to create vector store")
            return False
        
        # Optimize index
        vector_store.optimize_index()
        
        # Save vector store
        vector_store.save_vector_store()
        
        # Initialize professional RAG engine
        logger.info("🤖 Initializing professional RAG engine...")
        rag_engine = create_professional_rag_engine(
            vector_store,
            model_type="auto",
            use_reranking=True
        )
        
        documents_loaded = True
        logger.info("✅ Enhanced document loading completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error in enhanced document loading: {e}")
        return False

# Enhanced API endpoints
@app.get("/")
async def root():
    """API root with enhanced information."""
    return {
        "message": "Enhanced Student AI Assistant API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Professional RAG Engine",
            "Enhanced Document Processing", 
            "Advanced Vector Store",
            "Multiple Model Support",
            "Document Reranking",
            "Performance Optimization"
        ],
        "documentation": "/docs"
    }

@app.get("/api/status", response_model=SystemStatus)
async def get_enhanced_status() -> SystemStatus:
    """Get comprehensive system status."""
    global documents_loaded, vector_store, rag_engine, document_loader
    
    # Get vector store info
    vector_info = vector_store.get_vector_store_info() if vector_store else {}
    
    # Get RAG engine status
    rag_status = rag_engine.get_system_status() if rag_engine else {}
    
    # Performance metrics
    perf_metrics = {
        "avg_response_time": 0.0,
        "total_queries": 0,
        "cache_hit_rate": 0.0
    }
    
    if documents_loaded and rag_engine:
        try:
            # Quick performance test
            start_time = time.time()
            test_response = rag_engine.ask_question("test performance")
            test_time = time.time() - start_time
            perf_metrics["avg_response_time"] = test_time
        except:
            pass
    
    return SystemStatus(
        documents_loaded=documents_loaded,
        total_vectors=vector_info.get('total_vectors', 0),
        total_documents=vector_info.get('total_documents', 0),
        model_type=rag_status.get('llm_model', 'unknown'),
        device=rag_status.get('device', 'unknown'),
        embedding_model=vector_info.get('embeddings_model', 'unknown'),
        index_type=vector_info.get('index_type', 'unknown'),
        rag_engine_ready=rag_engine is not None,
        last_updated=datetime.now().isoformat(),
        performance_metrics=perf_metrics
    )

@app.post("/api/ask", response_model=EnhancedQuestionResponse)
async def ask_enhanced_question(
    request: EnhancedQuestionRequest, 
    db: Session = Depends(get_db)
) -> EnhancedQuestionResponse:
    """Enhanced question processing with professional RAG."""
    global rag_engine, documents_loaded, metrics_service
    
    start_time = time.time()
    
    # Validate request
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Handle case when no documents are loaded
        if not documents_loaded or not rag_engine:
            response = await _generate_fallback_response(request.question, start_time)
        else:
            # Use professional RAG engine
            rag_response = rag_engine.ask_question(
                question=request.question,
                subject_filter=request.subject_filter
            )
            
            # Convert to API response format
            response = EnhancedQuestionResponse(
                answer=rag_response.answer,
                confidence=rag_response.confidence,
                sources=[
                    {
                        "content": source.page_content[:300] + "..." if len(source.page_content) > 300 else source.page_content,
                        "source": source.metadata.get("source", "Unknown"),
                        "subject": source.metadata.get("subject", "General"),
                        "file_type": source.metadata.get("file_type", "unknown"),
                        "chunk_id": source.metadata.get("chunk_id", 0)
                    }
                    for source in rag_response.sources
                ],
                processing_time=rag_response.processing_time,
                query=rag_response.query,
                model_used=rag_response.model_used,
                source_scores=rag_response.source_scores,
                metadata=rag_response.metadata
            )
        
        # Record metrics
        processing_time = time.time() - start_time
        subject = metrics_service.detect_subject(request.question)
        question_type = QuestionType.DOCUMENT_BASED if response.sources else QuestionType.PRECOMPUTED
        
        metrics_service.record_question(
            question=request.question,
            response_time=processing_time,
            confidence=response.confidence,
            question_type=question_type,
            subject=subject,
            user_id=str(request.student_id) if request.student_id else "anonymous",
            sources_used=len(response.sources),
            db=db
        )
        
        # Save conversation if requested
        if request.save and request.student_id:
            conv_id, user_msg_id, assistant_msg_id = await _save_conversation(
                db, request, response
            )
            response.conversation_id = conv_id
            response.user_message_id = user_msg_id
            response.assistant_message_id = assistant_msg_id
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

async def _generate_fallback_response(question: str, start_time: float) -> EnhancedQuestionResponse:
    """Generate fallback response when RAG is not available."""
    from src.precomputed_responses import PrecomputedResponses
    
    # Try to get a precomputed response
    precomputed = PrecomputedResponses()
    
    # Basic keyword matching for fallback
    question_lower = question.lower()
    
    if "ohm" in question_lower:
        answer = precomputed.get_ohm_law_response()
    elif "thévenin" in question_lower:
        answer = precomputed.get_thevenin_response()
    elif "transistor" in question_lower:
        answer = precomputed.get_transistor_response()
    elif "dérivée" in question_lower:
        answer = precomputed.get_derivative_response()
    elif "intégrale" in question_lower:
        answer = precomputed.get_integral_response()
    elif "ph" in question_lower:
        answer = precomputed.get_ph_response()
    else:
        answer = f"""**ASSISTANT IA UNIVERSITAIRE**

Bonjour ! Je suis votre assistant IA spécialisé dans l'aide aux étudiants.

**Votre question :** {question}

**Réponse :** Je peux vous aider avec de nombreux concepts universitaires. Actuellement, je n'ai pas de documents spécifiques chargés, mais je peux expliquer les concepts fondamentaux dans plusieurs matières :

- **Mathématiques** : dérivées, intégrales, limites, fonctions
- **Physique** : lois de Newton, énergie, mouvement
- **Électricité** : loi d'Ohm, théorème de Thévenin, puissance
- **Électronique** : transistors, amplificateurs, circuits
- **Chimie** : pH, acides-bases, réactions
- **Et plus encore...**

**Pour une réponse plus précise :**
1. Reformulez votre question avec des termes spécifiques
2. Ajoutez vos documents de cours dans le dossier 'data/'
3. Rechargez le système pour une analyse complète

Je suis là pour vous aider à réussir vos études !"""
    
    processing_time = time.time() - start_time
    
    return EnhancedQuestionResponse(
        answer=answer,
        confidence=0.7,
        sources=[],
        processing_time=processing_time,
        query=question,
        model_used="fallback",
        source_scores=[],
        metadata={"mode": "fallback", "precomputed": True}
    )

async def _save_conversation(
    db: Session, 
    request: EnhancedQuestionRequest, 
    response: EnhancedQuestionResponse
) -> tuple:
    """Save conversation to database."""
    try:
        conv_id = request.conversation_id
        
        # Create conversation if needed
        if not conv_id and request.create_conversation:
            conv = crud.create_conversation(
                db, 
                student_id=request.student_id, 
                title=request.title or "Conversation"
            )
            conv_id = conv.id
        
        user_msg_id = None
        assistant_msg_id = None
        
        if conv_id:
            # Save user message
            user_msg = crud.add_message(
                db,
                conversation_id=conv_id,
                sender="user",
                content=request.question
            )
            user_msg_id = user_msg.id
            
            # Save assistant message
            assistant_msg = crud.add_message(
                db,
                conversation_id=conv_id,
                sender="assistant",
                content=response.answer,
                confidence=str(response.confidence),
                response_time=str(response.processing_time)
            )
            assistant_msg_id = assistant_msg.id
        
        return conv_id, user_msg_id, assistant_msg_id
        
    except Exception as e:
        logger.error(f"Error saving conversation: {e}")
        return None, None, None

# Document and configuration endpoints
@app.post("/api/configure")
async def configure_system(config: ModelConfig):
    """Configure RAG system parameters."""
    global rag_engine, vector_store
    
    try:
        if rag_engine and vector_store:
            # Recreate RAG engine with new configuration
            rag_engine = create_professional_rag_engine(
                vector_store,
                model_type=config.model_type,
                use_reranking=config.use_reranking
            )
            
            # Update internal config
            rag_engine.max_sources = config.max_sources
            rag_engine.min_confidence = config.min_confidence
            
            logger.info(f"System reconfigured: {config}")
            
            return {
                "message": "System configuration updated successfully",
                "config": config.dict(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="RAG system not initialized")
            
    except Exception as e:
        logger.error(f"Error configuring system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """Enhanced document upload with batch processing."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    uploaded_files = []
    errors = []
    
    try:
        for file in files:
            if file.filename:
                # Validate file type
                file_ext = Path(file.filename).suffix.lower()
                supported_exts = ['.pdf', '.docx', '.doc', '.txt', '.md', '.json']
                
                if file_ext not in supported_exts:
                    errors.append(f"{file.filename}: Unsupported file type")
                    continue
                
                # Save file
                file_path = data_dir / file.filename
                content = await file.read()
                
                with open(file_path, "wb") as f:
                    f.write(content)
                
                uploaded_files.append({
                    "filename": file.filename,
                    "size": len(content),
                    "type": file_ext
                })
                
                logger.info(f"Uploaded: {file.filename} ({len(content)} bytes)")
        
        # Trigger document reloading in background
        if uploaded_files and background_tasks:
            background_tasks.add_task(load_documents_enhanced)
        
        return {
            "message": f"Successfully uploaded {len(uploaded_files)} files",
            "uploaded_files": uploaded_files,
            "errors": errors,
            "reload_triggered": len(uploaded_files) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error uploading documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/validate")
async def validate_documents():
    """Validate document quality and completeness."""
    global document_loader
    
    try:
        if not document_loader:
            raise HTTPException(status_code=400, detail="Document loader not initialized")
        
        # Load documents for validation
        documents = document_loader.load_documents()
        
        if not documents:
            return {"message": "No documents found for validation"}
        
        # Perform validation
        validation_results = document_loader.validate_documents(documents)
        
        # Generate report
        report = document_loader.get_processing_report(documents)
        
        return {
            "validation_results": validation_results,
            "processing_report": report,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error validating documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/stats")
async def get_document_statistics():
    """Get comprehensive document statistics."""
    global document_loader, vector_store
    
    try:
        if not document_loader or not documents_loaded:
            return {"message": "No documents loaded"}
        
        # Get vector store statistics
        vector_stats = vector_store.get_statistics() if vector_store else {}
        
        # Get processing statistics
        data_dir = Path("data")
        file_count = len(list(data_dir.glob("**/*"))) if data_dir.exists() else 0
        
        return {
            "vector_store_stats": vector_stats,
            "file_count": file_count,
            "data_directory": str(data_dir),
            "cache_enabled": document_loader.enable_cache,
            "chunk_size": document_loader.chunk_size,
            "chunk_overlap": document_loader.chunk_overlap,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting document stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cache/clear")
async def clear_document_cache():
    """Clear document processing cache."""
    global document_loader
    
    try:
        if document_loader:
            document_loader.clear_cache()
            return {
                "message": "Document cache cleared successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail="Document loader not initialized")
            
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Performance and monitoring endpoints
@app.get("/api/health")
async def enhanced_health_check():
    """Comprehensive health check."""
    global rag_engine, vector_store, document_loader, documents_loaded
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "database": False,
            "document_loader": document_loader is not None,
            "vector_store": vector_store is not None,
            "rag_engine": rag_engine is not None,
            "documents_loaded": documents_loaded
        },
        "performance": {},
        "errors": []
    }
    
    try:
        # Test database connection
        with next(get_db()) as db:
            db.execute("SELECT 1")
            health_status["components"]["database"] = True
    except Exception as e:
        health_status["errors"].append(f"Database error: {e}")
    
    # Test RAG engine performance
    if rag_engine and documents_loaded:
        try:
            start_time = time.time()
            test_response = rag_engine.ask_question("test")
            response_time = time.time() - start_time
            health_status["performance"]["avg_response_time"] = response_time
            health_status["performance"]["rag_functional"] = True
        except Exception as e:
            health_status["errors"].append(f"RAG engine error: {e}")
            health_status["performance"]["rag_functional"] = False
    
    # Overall status
    if health_status["errors"]:
        health_status["status"] = "degraded"
    
    all_components_healthy = all(health_status["components"].values())
    if not all_components_healthy:
        health_status["status"] = "unhealthy"
    
    return health_status

@app.get("/api/performance/benchmark")
async def run_performance_benchmark():
    """Run performance benchmark tests."""
    global rag_engine, documents_loaded
    
    if not documents_loaded or not rag_engine:
        raise HTTPException(status_code=400, detail="RAG system not ready for benchmarking")
    
    benchmark_questions = [
        "Explique-moi la loi d'Ohm",
        "Qu'est-ce qu'un transistor ?",
        "Comment calculer une dérivée ?",
        "Qu'est-ce que le pH ?",
        "Explique les lois de Newton"
    ]
    
    results = {
        "total_questions": len(benchmark_questions),
        "results": [],
        "summary": {},
        "timestamp": datetime.now().isoformat()
    }
    
    response_times = []
    confidences = []
    
    try:
        for i, question in enumerate(benchmark_questions):
            start_time = time.time()
            response = rag_engine.ask_question(question)
            response_time = time.time() - start_time
            
            response_times.append(response_time)
            confidences.append(response.confidence)
            
            results["results"].append({
                "question_id": i + 1,
                "question": question,
                "response_time": response_time,
                "confidence": response.confidence,
                "model_used": response.model_used,
                "sources_count": len(response.sources)
            })
        
        # Calculate summary statistics
        results["summary"] = {
            "avg_response_time": sum(response_times) / len(response_times),
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "avg_confidence": sum(confidences) / len(confidences),
            "fast_responses": sum(1 for t in response_times if t < 0.5),
            "slow_responses": sum(1 for t in response_times if t > 2.0)
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Error running benchmark: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
async def get_performance_metrics(db: Session = Depends(get_db)):
    """Get performance metrics with enhanced data."""
    try:
        metrics = metrics_service.get_performance_metrics(db)
        
        # Add system metrics
        system_metrics = {
            "documents_loaded": documents_loaded,
            "rag_engine_ready": rag_engine is not None,
            "vector_store_ready": vector_store is not None,
            "timestamp": datetime.now().isoformat()
        }
        
        result = metrics.dict()
        result.update(system_metrics)
        
        return result
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/suggestions")
async def get_enhanced_suggestions(subject: Optional[str] = None) -> List[str]:
    """Get enhanced question suggestions."""
    global rag_engine, documents_loaded
    
    try:
        if documents_loaded and rag_engine:
            suggestions = rag_engine.get_suggested_questions(subject)
        else:
            # Fallback suggestions
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
        
        # Filter by subject if specified
        if subject:
            subject_keywords = {
                "Électricité": ["ohm", "thévenin", "puissance", "circuit"],
                "Mathématiques": ["dérivée", "intégrale", "fonction", "limite"],
                "Physique": ["newton", "force", "énergie", "mouvement"],
                "Chimie": ["ph", "acide", "base", "réaction"],
                "Électronique": ["transistor", "amplificateur", "circuit"]
            }
            
            if subject in subject_keywords:
                keywords = subject_keywords[subject]
                filtered = [s for s in suggestions 
                          if any(k in s.lower() for k in keywords)]
                suggestions = filtered if filtered else suggestions[:3]
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return []

# Enhanced error handlers
@app.exception_handler(RAGSystemError)
async def rag_error_handler(request, exc: RAGSystemError):
    """Handle RAG system-specific errors."""
    error_type = type(exc).__name__
    error_counts["total"] += 1
    
    if isinstance(exc, DocumentProcessingError):
        error_counts["document_processing"] += 1
        status_code = 400
    elif isinstance(exc, VectorStoreError):
        error_counts["vector_store"] += 1
        status_code = 500
    elif isinstance(exc, ModelError):
        error_counts["model"] += 1
        status_code = 503
    else:
        error_counts["other"] += 1
        status_code = 500
    
    logger.error(f"{error_type}: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_type,
            "message": str(exc),
            "timestamp": datetime.now().isoformat(),
            "request_path": str(request.url),
            "error_details": {
                "type": error_type,
                "category": "rag_system"
            }
        }
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request, exc: HTTPException):
    """Enhanced HTTP error handler."""
    error_counts["total"] += 1
    error_counts["other"] += 1
    
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "request_path": str(request.url),
            "error_details": {
                "type": "HTTPException",
                "category": "http",
                "status_code": exc.status_code
            }
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Enhanced global exception handler."""
    error_counts["total"] += 1
    error_counts["other"] += 1
    
    error_id = str(uuid.uuid4())
    logger.error(f"Unhandled exception ({error_id}): {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Our team has been notified.",
            "timestamp": datetime.now().isoformat(),
            "request_path": str(request.url),
            "error_details": {
                "type": type(exc).__name__,
                "category": "unhandled",
                "error_id": error_id
            }
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )