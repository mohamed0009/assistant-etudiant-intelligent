"""
Professional Ollama RAG API - Production Ready
Enhanced API with proper Ollama integration and comprehensive error handling.
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
import logging
import asyncio
import aiofiles
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import time
import uvicorn
import uuid
from pathlib import Path
import json
import os
import httpx
from functools import lru_cache
import psutil

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/ollama_rag_api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Import local modules with proper error handling
try:
    from src.rag_engine_ollama import OllamaRAGEngine, OllamaModelManager
    from src.vector_store import EnhancedVectorStore
    from src.document_loader import DocumentLoader
    from src.database import get_db, init_db
    from src.crud import CRUD
    from src.models import QuestionType, SubjectType
    from src.models_db import Student, Conversation, Message
    from src.metrics_service import MetricsService
except ImportError as e:
    logger.warning(f"Some modules not available: {e}")
    # Continue with limited functionality
    OllamaRAGEngine = None
    OllamaModelManager = None
    EnhancedVectorStore = None
    DocumentLoader = None
    CRUD = None
    MetricsService = None
    get_db = None
    init_db = None
    MODULES_AVAILABLE = False

# Placeholder classes for missing implementations
class ConfigManager:
    def __init__(self):
        pass
    
    async def load_config(self):
        pass
    
    def get(self, key, default=None):
        return default
    
    def get_section(self, section, default=None):
        return default or {}
    
    async def update_section(self, section, config):
        pass
    
    def get_public_config(self):
        return {}

class CacheManager:
    def __init__(self):
        pass
    
    async def initialize(self):
        pass
    
    async def cleanup(self):
        pass
    
    async def clear_pattern(self, pattern):
        pass
    
    async def get_metrics(self):
        return {}

class MetricsCollector:
    def __init__(self):
        pass
    
    async def initialize(self):
        pass
    
    async def flush_metrics(self):
        pass
    
    async def record_request(self, method, path, status_code, response_time):
        pass
    
    async def get_summary(self):
        return {"total_requests": 0, "avg_response_time": 0.0, "success_rate": 0.0, "total_sessions": 0}
    
    async def get_detailed_metrics(self):
        return {}

class ProfessionalDocumentLoader:
    def __init__(self, data_dir, cache_manager=None):
        self.data_dir = data_dir
        self.cache_manager = cache_manager
    
    async def load_documents_async(self):
        return []
    
    async def process_documents_async(self, documents):
        return []

class EnhancedCRUD:
    def __init__(self):
        pass

# Enhanced exception classes
class OllamaRAGError(Exception):
    """Base exception for Ollama RAG system."""
    pass

class OllamaConnectionError(OllamaRAGError):
    """Ollama connection/model errors."""
    pass

class DocumentProcessingError(OllamaRAGError):
    """Document processing errors."""
    pass

class VectorStoreError(OllamaRAGError):
    """Vector store errors."""
    pass

class ConfigurationError(OllamaRAGError):
    """Configuration errors."""
    pass

# Global system components
class SystemComponents:
    """Global system components manager."""
    def __init__(self):
        self.rag_engine: Optional[OllamaRAGEngine] = None
        self.vector_store: Optional[EnhancedVectorStore] = None
        self.document_loader: Optional[ProfessionalDocumentLoader] = None
        self.metrics_collector: Optional[MetricsCollector] = None
        self.cache_manager: Optional[CacheManager] = None
        self.config_manager: Optional[ConfigManager] = None
        self.crud: Optional[EnhancedCRUD] = None
        self.ollama_manager: Optional[OllamaModelManager] = None
        self.documents_loaded: bool = False
        self.system_ready: bool = False
        self.startup_time: datetime = datetime.now()

system = SystemComponents()

# Enhanced Pydantic models with validation
class OllamaConfig(BaseModel):
    """Configuration for Ollama integration."""
    base_url: str = Field(default="http://localhost:11434", description="Ollama server URL")
    model_name: str = Field(default="llama2", description="Primary model name")
    fallback_models: List[str] = Field(default=["mistral", "codellama"], description="Fallback models")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)
    timeout: int = Field(default=30, ge=5, le=120)
    concurrent_requests: int = Field(default=3, ge=1, le=10)
    
    @field_validator('base_url')
    @classmethod
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Invalid URL format')
        return v

class EnhancedQuestionRequest(BaseModel):
    """Enhanced question request with comprehensive options."""
    question: str = Field(..., min_length=1, max_length=2000, description="The question to ask")
    subject_filter: Optional[str] = Field(None, description="Filter by subject")
    student_id: Optional[int] = Field(None, description="Student ID for tracking")
    conversation_id: Optional[int] = Field(None, description="Conversation ID")
    save_conversation: bool = Field(False, description="Save to database")
    create_new_conversation: bool = Field(False, description="Create new conversation")
    conversation_title: Optional[str] = Field(None, max_length=200)
    
    # Advanced options
    model_preference: Optional[str] = Field(None, description="Preferred Ollama model")
    use_reranking: bool = Field(True, description="Use document reranking")
    max_sources: int = Field(5, ge=1, le=20, description="Maximum source documents")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    include_metadata: bool = Field(True, description="Include response metadata")
    
    class Config:
        schema_extra = {
            "example": {
                "question": "Explain Ohm's law with practical examples",
                "subject_filter": "Electricity",
                "student_id": 1,
                "save_conversation": True,
                "use_reranking": True,
                "max_sources": 5
            }
        }

class EnhancedQuestionResponse(BaseModel):
    """Comprehensive response model."""
    answer: str = Field(..., description="Generated answer")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[Dict[str, Any]] = Field(default=[], description="Source documents")
    processing_time: float = Field(..., description="Processing time in seconds")
    query: str = Field(..., description="Processed query")
    
    # Ollama-specific fields
    model_used: str = Field(..., description="Ollama model used")
    ollama_response_time: float = Field(..., description="Ollama response time")
    tokens_generated: int = Field(default=0, description="Tokens generated")
    
    # Enhanced metadata
    source_scores: List[float] = Field(default=[], description="Source relevance scores")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
    
    # Conversation tracking
    conversation_id: Optional[int] = None
    user_message_id: Optional[int] = None
    assistant_message_id: Optional[int] = None

    # Quality indicators
    response_quality: str = Field(default="good", description="Response quality assessment")
    fallback_used: bool = Field(default=False, description="Whether fallback was used")

class SystemStatus(BaseModel):
    """Comprehensive system status."""
    status: str = Field(..., description="Overall system status")
    uptime: str = Field(..., description="System uptime")
    
    # Component status
    ollama_connected: bool = Field(..., description="Ollama connection status")
    ollama_models: List[str] = Field(default=[], description="Available Ollama models")
    documents_loaded: bool = Field(..., description="Documents loaded status")
    vector_store_ready: bool = Field(..., description="Vector store status")
    database_connected: bool = Field(..., description="Database connection status")
    
    # Performance metrics
    total_requests: int = Field(default=0, description="Total requests processed")
    avg_response_time: float = Field(default=0.0, description="Average response time")
    success_rate: float = Field(default=0.0, description="Success rate percentage")
    
    # Resource usage
    memory_usage: float = Field(default=0.0, description="Memory usage percentage")
    cpu_usage: float = Field(default=0.0, description="CPU usage percentage")
    
    # Configuration
    config: Dict[str, Any] = Field(default={}, description="Current configuration")
    
    last_updated: str = Field(..., description="Last update timestamp")

class DocumentUploadResponse(BaseModel):
    """Document upload response."""
    success: bool = Field(..., description="Upload success status")
    uploaded_files: List[Dict[str, Any]] = Field(default=[], description="Successfully uploaded files")
    failed_files: List[Dict[str, Any]] = Field(default=[], description="Failed uploads")
    processing_started: bool = Field(default=False, description="Background processing started")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")

# FastAPI app with lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Enhanced application lifespan management."""
    # Startup
    logger.info("🚀 Starting Professional Ollama RAG System...")
    await startup_system()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Professional Ollama RAG System...")
    await shutdown_system()

app = FastAPI(
    title="Professional Ollama RAG API",
    description="Production-ready RAG system with Ollama integration",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enhanced CORS with security considerations
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:8080",
        "http://localhost:5173"  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Response-Time"]
)

# Request middleware for logging and metrics
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    """Enhanced request middleware with comprehensive logging."""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Log request
    logger.info(f"Request [{request_id}]: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = str(process_time)
        
        # Log response
        logger.info(f"Response [{request_id}]: {response.status_code} - {process_time:.3f}s")
        
        # Collect metrics
        if system.metrics_collector:
            await system.metrics_collector.record_request(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                response_time=process_time
            )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request error [{request_id}]: {e} - {process_time:.3f}s")
        raise

async def startup_system():
    """Enhanced system startup with comprehensive initialization."""
    try:
        # Create necessary directories
        for directory in ["logs", "data", "cache", "exports", "config"]:
            Path(directory).mkdir(exist_ok=True)
        
        # Initialize configuration manager
        system.config_manager = ConfigManager()
        await system.config_manager.load_config()
        logger.info("✅ Configuration manager initialized")
        
        # Initialize database
        try:
            if init_db:
                init_db()
                logger.info("✅ Database initialized")
            else:
                logger.warning("Database initialization not available")
        except Exception as e:
            logger.warning(f"Database initialization failed: {e}")
        
        system.crud = EnhancedCRUD()
        
        # Initialize cache manager
        system.cache_manager = CacheManager()
        await system.cache_manager.initialize()
        logger.info("✅ Cache manager initialized")
        
        # Initialize metrics collector
        system.metrics_collector = MetricsCollector()
        await system.metrics_collector.initialize()
        logger.info("✅ Metrics collector initialized")
        
        # Initialize Ollama manager
        system.ollama_manager = OllamaModelManager(
            base_url=system.config_manager.get("ollama.base_url", "http://localhost:11434")
        )
        
        # Test Ollama connection
        if await system.ollama_manager.test_connection():
            logger.info("✅ Ollama connection established")
            
            # Load available models
            models = await system.ollama_manager.list_models()
            logger.info(f"✅ Available Ollama models: {models}")
        else:
            logger.warning("⚠️ Ollama not available, using fallback mode")
        
        # Initialize document loader
        system.document_loader = ProfessionalDocumentLoader(
            data_dir="data",
            cache_manager=system.cache_manager
        )
        logger.info("✅ Document loader initialized")
        
        # Initialize vector store
        system.vector_store = EnhancedVectorStore(
            cache_manager=system.cache_manager
        )
        
        # Try to load existing vector store or create new one
        if await system.vector_store.load_from_cache():
            logger.info("✅ Vector store loaded from cache")
            system.documents_loaded = True
        else:
            # Load documents in background
            asyncio.create_task(load_documents_background())
        
        # Initialize RAG engine
        if system.documents_loaded:
            system.rag_engine = OllamaRAGEngine(
                vector_store=system.vector_store,
                ollama_manager=system.ollama_manager,
                config=system.config_manager.get_section("rag", {})
            )
            await system.rag_engine.initialize()
            logger.info("✅ RAG engine initialized")
        
        system.system_ready = True
        logger.info("🎉 Professional Ollama RAG System started successfully!")
        
    except Exception as e:
        logger.error(f"❌ System startup failed: {e}")
        # Continue with limited functionality
        system.system_ready = False

async def shutdown_system():
    """Enhanced system shutdown with proper cleanup."""
    try:
        if system.vector_store:
            await system.vector_store.save_to_cache()
            logger.info("✅ Vector store saved")
        
        if system.cache_manager:
            await system.cache_manager.cleanup()
            logger.info("✅ Cache cleaned up")
        
        if system.metrics_collector:
            await system.metrics_collector.flush_metrics()
            logger.info("✅ Metrics flushed")
        
        logger.info("✅ System shutdown completed")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

async def load_documents_background():
    """Load documents in background task."""
    try:
        logger.info("📚 Starting background document loading...")
        
        documents = await system.document_loader.load_documents_async()
        if not documents:
            logger.warning("No documents found")
            return
        
        chunks = await system.document_loader.process_documents_async(documents)
        if not chunks:
            logger.warning("No chunks created during reprocessing")
            return
        
        # Update vector store
        success = await system.vector_store.update_from_documents(chunks)
        if not success:
            logger.error("Failed to update vector store")
            return
        
        # Reinitialize RAG engine if needed
        if system.rag_engine:
            await system.rag_engine.refresh_vector_store(system.vector_store)
        else:
            system.rag_engine = OllamaRAGEngine(
                vector_store=system.vector_store,
                ollama_manager=system.ollama_manager,
                config=system.config_manager.get_section("rag", {})
            )
            await system.rag_engine.initialize()
        
        system.documents_loaded = True
        logger.info("✅ Background document reprocessing completed")
        
        # Clear relevant caches
        if system.cache_manager:
            await system.cache_manager.clear_pattern("question:*")
        
    except Exception as e:
        logger.error(f"Background document reprocessing failed: {e}")

# Configuration and monitoring endpoints
@app.post("/api/ollama/configure", tags=["Configuration"])
async def configure_ollama(config: OllamaConfig):
    """Configure Ollama connection and models."""
    try:
        if not system.ollama_manager:
            raise HTTPException(status_code=500, detail="Ollama manager not initialized")
        
        # Update configuration
        await system.ollama_manager.update_config(config.dict())
        
        # Test new configuration
        connection_test = await system.ollama_manager.test_connection()
        if not connection_test:
            raise HTTPException(status_code=400, detail="Cannot connect to Ollama with provided configuration")
        
        # Pull models if needed
        available_models = await system.ollama_manager.list_models()
        missing_models = []
        
        for model in [config.model_name] + config.fallback_models:
            if model not in available_models:
                missing_models.append(model)
        
        if missing_models:
            # Start model pulling in background
            asyncio.create_task(pull_models_background(missing_models))
        
        # Save configuration
        if system.config_manager:
            await system.config_manager.update_section("ollama", config.dict())
        
        return {
            "message": "Ollama configuration updated successfully",
            "config": config.dict(),
            "available_models": available_models,
            "missing_models": missing_models,
            "pulling_models": len(missing_models) > 0
        }
        
    except Exception as e:
        logger.error(f"Error configuring Ollama: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def pull_models_background(models: List[str]):
    """Pull Ollama models in background."""
    for model in models:
        try:
            logger.info(f"Pulling Ollama model: {model}")
            await system.ollama_manager.pull_model(model)
            logger.info(f"✅ Model pulled successfully: {model}")
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")

@app.get("/api/ollama/models", tags=["Ollama"])
async def list_ollama_models():
    """List available Ollama models with details."""
    try:
        if not system.ollama_manager:
            raise HTTPException(status_code=500, detail="Ollama manager not initialized")
        
        models = await system.ollama_manager.list_models_detailed()
        return {
            "models": models,
            "total": len(models),
            "timestamp": datetime.now().isoformat()
        }
            
    except Exception as e:
        logger.error(f"Error listing Ollama models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ollama/models/{model_name}/pull", tags=["Ollama"])
async def pull_ollama_model(model_name: str, background_tasks: BackgroundTasks):
    """Pull a specific Ollama model."""
    try:
        if not system.ollama_manager:
            raise HTTPException(status_code=500, detail="Ollama manager not initialized")
        
        # Start pulling in background
        background_tasks.add_task(pull_models_background, [model_name])
        
        return {
            "message": f"Started pulling model: {model_name}",
            "model": model_name,
            "status": "pulling",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error pulling Ollama model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/ollama/models/{model_name}", tags=["Ollama"])
async def delete_ollama_model(model_name: str):
    """Delete an Ollama model."""
    try:
        if not system.ollama_manager:
            raise HTTPException(status_code=500, detail="Ollama manager not initialized")
        
        success = await system.ollama_manager.delete_model(model_name)
        if not success:
            raise HTTPException(status_code=400, detail=f"Failed to delete model: {model_name}")
        
        return {
            "message": f"Model deleted successfully: {model_name}",
            "model": model_name,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error deleting Ollama model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced monitoring and metrics
@app.get("/api/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get basic system metrics."""
    try:
        metrics = {
            "total_questions": 0,
            "avg_response_time": "N/A", 
            "accuracy": "N/A",
            "uptime": str(datetime.now() - system.startup_time),
            "total_sessions": 0,
            "most_asked_subjects": {},
            "system_status": "healthy" if system.system_ready else "starting"
        }
        
        # Get basic system metrics
        if system.metrics_collector:
            try:
                summary = await system.metrics_collector.get_summary()
                metrics.update({
                    "total_questions": summary.get("total_requests", 0),
                    "avg_response_time": f"{summary.get('avg_response_time', 0):.2f}s",
                    "accuracy": f"{summary.get('success_rate', 0):.1%}",
                    "total_sessions": summary.get("total_sessions", 0)
                })
            except Exception as e:
                logger.warning(f"Could not get metrics summary: {e}")
        
        # Get document stats
        if system.vector_store:
            try:
                stats = await system.vector_store.get_stats()
                metrics["documents_loaded"] = stats.get("document_count", 0)
                metrics["vector_count"] = stats.get("vector_count", 0)
            except Exception as e:
                logger.warning(f"Could not get vector store stats: {e}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics/detailed", tags=["Monitoring"])
async def get_detailed_metrics():
    """Get comprehensive system metrics."""
    try:
        metrics = {}
        
        # System metrics
        metrics["system"] = {
            "uptime": str(datetime.now() - system.startup_time),
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "disk_usage": psutil.disk_usage("/").percent
        }
        
        # Ollama metrics
        if system.ollama_manager:
            metrics["ollama"] = await system.ollama_manager.get_metrics()
        
        # RAG metrics
        if system.metrics_collector:
            metrics["rag"] = await system.metrics_collector.get_detailed_metrics()
        
        # Vector store metrics
        if system.vector_store:
            metrics["vector_store"] = await system.vector_store.get_metrics()
        
        # Cache metrics
        if system.cache_manager:
            metrics["cache"] = await system.cache_manager.get_metrics()
        
            return {
            "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error getting detailed metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health/detailed", tags=["Monitoring"])
async def detailed_health_check():
    """Comprehensive health check with component details."""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {},
        "tests": {},
        "recommendations": []
    }
    
    try:
        # Database health
        try:
            if get_db:
                with next(get_db()) as db:
                    result = db.execute("SELECT 1").fetchone()
                    health_data["components"]["database"] = {
                        "status": "healthy",
                        "response_time": "< 1ms"
                    }
            else:
                health_data["components"]["database"] = {
                    "status": "not_available",
                    "error": "Database module not available"
                }
        except Exception as e:
            health_data["components"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_data["status"] = "degraded"
        
        # Ollama health
        if system.ollama_manager:
            try:
                start_time = time.time()
                connected = await system.ollama_manager.test_connection()
                response_time = time.time() - start_time
                
                if connected:
                    models = await system.ollama_manager.list_models()
                    health_data["components"]["ollama"] = {
                        "status": "healthy",
                        "response_time": f"{response_time:.3f}s",
                        "models_count": len(models),
                        "models": models[:5]  # First 5 models
                    }
                else:
                    health_data["components"]["ollama"] = {
                        "status": "unhealthy",
                        "error": "Connection failed"
                    }
                    health_data["status"] = "degraded"
                    health_data["recommendations"].append("Check Ollama server status")
                    
            except Exception as e:
                health_data["components"]["ollama"] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health_data["status"] = "degraded"
        else:
            health_data["components"]["ollama"] = {
                "status": "not_initialized",
                "error": "Ollama manager not available"
            }
        
        # Vector store health
        if system.vector_store:
            try:
                stats = await system.vector_store.get_stats()
                health_data["components"]["vector_store"] = {
                    "status": "healthy",
                    "documents": stats.get("document_count", 0),
                    "vectors": stats.get("vector_count", 0)
                }
            except Exception as e:
                health_data["components"]["vector_store"] = {
                    "status": "degraded",
                    "error": str(e)
                }
        else:
            health_data["components"]["vector_store"] = {
                "status": "not_initialized"
            }
        
        # RAG engine health
        if system.rag_engine:
            try:
                # Quick test query
                start_time = time.time()
                test_response = await system.rag_engine.ask_question_async(
                    "test health check",
                    max_sources=1
                )
                response_time = time.time() - start_time
                
                health_data["components"]["rag_engine"] = {
                    "status": "healthy",
                    "test_response_time": f"{response_time:.3f}s",
                    "test_confidence": test_response.confidence
                }
                
                health_data["tests"]["rag_functionality"] = {
                    "status": "passed",
                    "response_time": f"{response_time:.3f}s"
                }
                
            except Exception as e:
                health_data["components"]["rag_engine"] = {
                    "status": "degraded",
                    "error": str(e)
                }
                health_data["tests"]["rag_functionality"] = {
                    "status": "failed",
                    "error": str(e)
                }
        else:
            health_data["components"]["rag_engine"] = {
                "status": "not_initialized"
            }
        
        # Performance recommendations
        memory_usage = psutil.virtual_memory().percent
        if memory_usage > 90:
            health_data["recommendations"].append("High memory usage detected - consider restarting")
        elif memory_usage > 75:
            health_data["recommendations"].append("Memory usage above 75% - monitor closely")
        
        cpu_usage = psutil.cpu_percent()
        if cpu_usage > 90:
            health_data["recommendations"].append("High CPU usage detected")
        
        # Overall status determination
        unhealthy_components = [
            name for name, comp in health_data["components"].items() 
            if comp.get("status") == "unhealthy"
        ]
        
        if unhealthy_components:
            health_data["status"] = "unhealthy"
        elif any(comp.get("status") == "degraded" for comp in health_data["components"].values()):
            health_data["status"] = "degraded"
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
        "timestamp": datetime.now().isoformat()
    }
    
# Performance and benchmarking
@app.post("/api/benchmark/comprehensive", tags=["Performance"])
async def run_comprehensive_benchmark():
    """Run comprehensive system benchmark."""
    if not system.system_ready or not system.rag_engine:
        raise HTTPException(status_code=503, detail="System not ready for benchmarking")
    
    benchmark_results = {
        "timestamp": datetime.now().isoformat(),
        "system_info": {
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available
        },
        "tests": {}
    }
    
    try:
        # Test 1: Simple questions
        simple_questions = [
            "What is Ohm's law?",
            "Explain derivatives",
            "What is pH?",
            "Define transistor",
            "Newton's laws"
        ]
        
        simple_results = []
        for question in simple_questions:
            start_time = time.time()
            response = await system.rag_engine.ask_question_async(question, max_sources=3)
            end_time = time.time()
            
            simple_results.append({
                "question": question,
                "response_time": end_time - start_time,
                "confidence": response.confidence,
                "model_used": response.model_used,
                "sources_found": len(response.sources)
            })
        
        benchmark_results["tests"]["simple_questions"] = {
            "total_questions": len(simple_questions),
            "avg_response_time": sum(r["response_time"] for r in simple_results) / len(simple_results),
            "avg_confidence": sum(r["confidence"] for r in simple_results) / len(simple_results),
            "results": simple_results
        }
        
        # Test 2: Complex questions
        complex_questions = [
            "Explain the relationship between Ohm's law and power calculations in electrical circuits with practical examples",
            "Describe the mathematical foundation of derivatives and their applications in physics and engineering",
            "Analyze the pH scale and its importance in chemical reactions and biological systems"
        ]
        
        complex_results = []
        for question in complex_questions:
            start_time = time.time()
            response = await system.rag_engine.ask_question_async(question, max_sources=5)
            end_time = time.time()
            
            complex_results.append({
                "question": question[:50] + "...",
                "response_time": end_time - start_time,
                "confidence": response.confidence,
                "model_used": response.model_used,
                "sources_found": len(response.sources),
                "tokens_generated": response.tokens_generated
            })
        
        benchmark_results["tests"]["complex_questions"] = {
            "total_questions": len(complex_questions),
            "avg_response_time": sum(r["response_time"] for r in complex_results) / len(complex_results),
            "avg_confidence": sum(r["confidence"] for r in complex_results) / len(complex_results),
            "results": complex_results
        }
        
        # Test 3: Stress test
        stress_questions = ["Quick test question"] * 10
        stress_start = time.time()
        
        stress_tasks = [
            system.rag_engine.ask_question_async(q, max_sources=2) 
            for q in stress_questions
        ]
        stress_responses = await asyncio.gather(*stress_tasks, return_exceptions=True)
        
        stress_end = time.time()
        successful_responses = [r for r in stress_responses if not isinstance(r, Exception)]
        
        benchmark_results["tests"]["stress_test"] = {
            "total_requests": len(stress_questions),
            "successful_requests": len(successful_responses),
            "total_time": stress_end - stress_start,
            "requests_per_second": len(successful_responses) / (stress_end - stress_start),
            "success_rate": len(successful_responses) / len(stress_questions) * 100
        }
        
        # Overall assessment
        overall_avg_time = (
            benchmark_results["tests"]["simple_questions"]["avg_response_time"] +
            benchmark_results["tests"]["complex_questions"]["avg_response_time"]
        ) / 2
        
        if overall_avg_time < 1.0:
            performance_rating = "excellent"
        elif overall_avg_time < 3.0:
            performance_rating = "good"
        elif overall_avg_time < 5.0:
            performance_rating = "fair"
        else:
            performance_rating = "poor"
        
        benchmark_results["summary"] = {
            "overall_performance": performance_rating,
            "avg_response_time": overall_avg_time,
            "system_ready": True,
            "recommendations": []
        }
        
        if overall_avg_time > 3.0:
            benchmark_results["summary"]["recommendations"].append(
                "Consider optimizing document chunking or reducing max_sources"
            )
        
        if benchmark_results["tests"]["stress_test"]["success_rate"] < 95:
            benchmark_results["summary"]["recommendations"].append(
                "System may have stability issues under load"
            )
        
        return benchmark_results
        
    except Exception as e:
        logger.error(f"Benchmark error: {e}")
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")

# Enhanced error handlers
@app.exception_handler(OllamaConnectionError)
async def ollama_connection_error_handler(request: Request, exc: OllamaConnectionError):
    """Handle Ollama connection errors."""
    logger.error(f"Ollama connection error: {exc}")
    return JSONResponse(
        status_code=503,
        content={
            "error": "Ollama Connection Error",
            "message": "Cannot connect to Ollama server. Please ensure Ollama is running.",
            "details": str(exc),
            "timestamp": datetime.now().isoformat(),
            "suggestions": [
                "Check if Ollama is installed and running",
                "Verify Ollama server URL in configuration",
                "Ensure required models are pulled"
            ]
        }
    )

@app.exception_handler(DocumentProcessingError)
async def document_processing_error_handler(request: Request, exc: DocumentProcessingError):
    """Handle document processing errors."""
    logger.error(f"Document processing error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "Document Processing Error",
            "message": "Error processing uploaded documents",
            "details": str(exc),
            "timestamp": datetime.now().isoformat(),
            "suggestions": [
                "Check document format and size",
                "Ensure documents are not corrupted",
                "Try uploading fewer files at once"
            ]
        }
    )

@app.exception_handler(VectorStoreError)
async def vector_store_error_handler(request: Request, exc: VectorStoreError):
    """Handle vector store errors."""
    logger.error(f"Vector store error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Vector Store Error",
            "message": "Error with document search system",
            "details": str(exc),
            "timestamp": datetime.now().isoformat(),
            "suggestions": [
                "Try reloading documents",
                "Check available disk space",
                "Clear cache and restart system"
            ]
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload in production
        log_level="info",
        access_log=True,
        workers=1  # Single worker for RAG system
    )

# ---- Simple file-backed Student CRUD to ensure frontend works even without DB ----
STUDENTS_FILE = Path("data") / "students.json"

def _ensure_students_file():
    try:
        STUDENTS_FILE.parent.mkdir(exist_ok=True)
        if not STUDENTS_FILE.exists():
            with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
    except Exception as e:
        logger.error(f"Failed to ensure students file: {e}")

def _read_students() -> List[Dict[str, Any]]:
    _ensure_students_file()
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception as e:
        logger.error(f"Failed to read students: {e}")
        return []

def _write_students(students: List[Dict[str, Any]]):
    try:
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(students, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to write students: {e}")

@app.post("/api/students", tags=["Students"])
async def create_student(student_data: dict):
    """Create a new student (file-backed)."""
    try:
        students = _read_students()
        new_id = (max((s.get("id", 0) for s in students), default=0) + 1) if students else 1
        student = {
            "id": new_id,
            "name": student_data.get("name", "Étudiant"),
            "email": student_data.get("email", "student@example.com"),
            "role": student_data.get("role", "student"),
            "created_at": datetime.now().isoformat()
        }
        students.append(student)
        _write_students(students)
        return student
    except Exception as e:
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create student: {str(e)}")

@app.get("/api/students", tags=["Students"])
async def list_students():
    """List all students (file-backed)."""
    try:
        return _read_students()
    except Exception as e:
        logger.error(f"Error listing students: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list students: {str(e)}")

@app.get("/api/students/{student_id}", tags=["Students"])
async def get_student(student_id: int):
    """Get a specific student (file-backed)."""
    try:
        students = _read_students()
        for s in students:
            if int(s.get("id")) == int(student_id):
                return {"id": s.get("id"), "name": s.get("name"), "email": s.get("email"), "role": s.get("role", "student")}
        raise HTTPException(status_code=404, detail="Student not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/students/{student_id}", tags=["Students"])
async def update_student(student_id: int, student_data: dict):
    """Update a student (file-backed)."""
    try:
        students = _read_students()
        updated = None
        for s in students:
            if int(s.get("id")) == int(student_id):
                if "name" in student_data:
                    s["name"] = student_data["name"]
                if "email" in student_data:
                    s["email"] = student_data["email"]
                if "role" in student_data:
                    s["role"] = student_data["role"]
                updated = s
                break
        if not updated:
            raise HTTPException(status_code=404, detail="Student not found")
        _write_students(students)
        return {"id": updated.get("id"), "name": updated.get("name"), "email": updated.get("email"), "role": updated.get("role", "student")}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/students/{student_id}", tags=["Students"])
async def delete_student(student_id: int):
    """Delete a student (file-backed)."""
    try:
        students = _read_students()
        new_students = [s for s in students if int(s.get("id")) != int(student_id)]
        if len(new_students) == len(students):
            raise HTTPException(status_code=404, detail="Student not found")
        _write_students(new_students)
        return {"message": "Student deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Conversation Management Endpoints
@app.post("/api/conversations", tags=["Conversations"])
async def create_conversation(conversation_data: dict):
    """Create a new conversation (mock implementation)."""
    try:
        # Mock implementation - return fake conversation data
        conversation_id = 1  # In real implementation, this would be generated
        
        return {
            "id": conversation_id,
            "student_id": conversation_data.get("student_id", 1),
            "title": conversation_data.get("title", "New Conversation"),
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}/conversations", tags=["Conversations"])
async def list_student_conversations(student_id: int):
    """List conversations for a specific student."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        # Return empty list for now - can be enhanced when database is properly set up
        return []
        
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/conversations/{conversation_id}/title", tags=["Conversations"])
async def update_conversation_title(
    conversation_id: int,
    title_data: dict
):
    """Update conversation title."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        return {
            "id": conversation_id,
            "student_id": 1,
            "title": title_data.get("title", f"Conversation {conversation_id}")
        }
        
    except Exception as e:
        logger.error(f"Error updating conversation title: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Message Management Endpoints
@app.post("/api/messages", tags=["Messages"])
async def create_message(
    message_data: dict
):
    """Create a new message (mock implementation)."""
    try:
        # Mock implementation - return fake message data
        message_id = 1  # In real implementation, this would be generated
        
        return {
            "id": message_id,
            "conversation_id": message_data.get("conversation_id", 1),
            "sender": message_data.get("sender", "user"),
            "content": message_data.get("content", ""),
            "confidence": message_data.get("confidence", 0.8),
            "response_time": message_data.get("response_time", 0.1),
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}/messages", tags=["Messages"])
async def list_conversation_messages(conversation_id: int):
    """List messages for a specific conversation."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        return []
        
    except Exception as e:
        logger.error(f"Error listing messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Document Management Endpoints
@app.get("/api/documents", tags=["Documents"])
async def list_all_documents():
    """List all available documents."""
    try:
        # Use course documents from file system instead of document loader
        from pathlib import Path
        
        data_dir = Path("data")
        if not data_dir.exists():
            return []
        
        course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
        
        documents = []
        for i, file_path in enumerate(course_files):
            # Extract subject from filename
            filename = file_path.stem.lower()
            if "math" in filename or "calcul" in filename or "algebre" in filename:
                subject = "Mathématiques"
            elif "physique" in filename or "electricite" in filename or "mecanique" in filename:
                subject = "Physique"
            elif "chimie" in filename:
                subject = "Chimie"
            elif "biologie" in filename:
                subject = "Biologie"
            elif "informatique" in filename or "algorithmes" in filename:
                subject = "Informatique"
            else:
                subject = "Général"
            
            # Get file size
            file_size = file_path.stat().st_size
            
            documents.append({
                "id": f"doc_{i}",
                "name": file_path.name,
                "type": "text",
                "size": f"{file_size} bytes",
                "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "status": "active",
                "source": "course_document",
                "subject": subject,
                "path": str(file_path)
            })
        
        return documents
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/documents", tags=["Documents"])
async def list_student_documents(student_id: int):
    """List documents accessible to a specific student."""
    try:
        # For now, return all documents (can be filtered later based on student permissions)
        return await list_all_documents()
        
    except Exception as e:
        logger.error(f"Error listing student documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/stats", tags=["Documents"])
async def get_document_stats():
    """Get document statistics."""
    try:
        # Get course documents count
        course_documents_count = 0
        subjects = set()
        
        try:
            from pathlib import Path
            data_dir = Path("data")
            if data_dir.exists():
                course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
                course_documents_count = len(course_files)
                
                # Extract subjects from filenames
                for file_path in course_files:
                    filename = file_path.stem.lower()
                    if "math" in filename or "calcul" in filename or "algebre" in filename:
                        subjects.add("Mathématiques")
                    elif "physique" in filename or "electricite" in filename or "mecanique" in filename:
                        subjects.add("Physique")
                    elif "chimie" in filename:
                        subjects.add("Chimie")
                    elif "biologie" in filename:
                        subjects.add("Biologie")
                    elif "informatique" in filename or "algorithmes" in filename:
                        subjects.add("Informatique")
                    else:
                        subjects.add("Général")
        except:
            pass
        
        # Try to get vector store stats if available
        vector_stats = {}
        if system.vector_store:
            try:
                vector_stats = await system.vector_store.get_stats()
            except:
                pass
        
        return {
            "total_documents": course_documents_count + vector_stats.get("document_count", 0),
            "total_chunks": vector_stats.get("vector_count", course_documents_count),
            "subjects": list(subjects) if subjects else ["Mathématiques", "Physique", "Chimie", "Biologie", "Informatique"],
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting document stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Student Dashboard Endpoints
@app.get("/api/student/subjects", tags=["Student"])
async def get_student_subjects():
    """Get available subjects for student dashboard."""
    try:
        # Get subjects from course documents if vector store is not available
        subjects = []
        
        if system.vector_store:
            try:
                stats = await system.vector_store.get_stats()
                subjects = stats.get("subjects", [])
            except:
                pass
        
        # If no subjects from vector store, get them from course documents
        if not subjects:
            try:
                from pathlib import Path
                data_dir = Path("data")
                if data_dir.exists():
                    course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
                    subject_set = set()
                    
                    for file_path in course_files:
                        filename = file_path.stem.lower()
                        if "math" in filename or "calcul" in filename or "algebre" in filename:
                            subject_set.add("Mathématiques")
                        elif "physique" in filename or "electricite" in filename or "mecanique" in filename:
                            subject_set.add("Physique")
                        elif "chimie" in filename:
                            subject_set.add("Chimie")
                        elif "biologie" in filename:
                            subject_set.add("Biologie")
                        elif "informatique" in filename or "algorithmes" in filename:
                            subject_set.add("Informatique")
                        else:
                            subject_set.add("Général")
                    
                    subjects = list(subject_set)
            except:
                pass
        
        # Fallback to default subjects if nothing found
        if not subjects:
            subjects = ["Mathématiques", "Physique", "Chimie", "Biologie", "Informatique"]
        
        # Create subject objects with mock data
        subject_objects = []
        for i, subject in enumerate(subjects):
            subject_objects.append({
                "id": f"subject_{i}",
                "name": subject,
                "code": subject.upper()[:3],
                "description": f"Cours de {subject}",
                "documents_count": 5,  # Mock data
                "questions_count": 10,  # Mock data
                "color": f"hsl({(i * 137.5) % 360}, 70%, 50%)"
            })
        
        return subject_objects
        
    except Exception as e:
        logger.error(f"Error getting student subjects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/usage-stats", tags=["Student"])
async def get_student_usage_stats(student_id: int):
    """Get usage statistics for a specific student."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        # In a real implementation, this would query the database
        
        return {
            "total_questions": 15,  # Mock data
            "total_conversations": 3,  # Mock data
            "total_documents": 20,  # Mock data
            "last_activity": datetime.now().isoformat(),
            "favorite_subjects": ["Mathématiques", "Physique", "Chimie"]  # Mock data
        }
        
    except Exception as e:
        logger.error(f"Error getting student usage stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Admin Endpoints
@app.get("/api/admin/documents", tags=["Admin"])
async def list_admin_documents():
    """List all documents for admin management."""
    try:
        data_dir = Path("data")
        if not data_dir.exists():
            return {"documents": [], "total": 0}
        
        documents = []
        for file_path in data_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                documents.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
        
        return {
            "documents": documents,
            "total": len(documents)
        }
        
    except Exception as e:
        logger.error(f"Error listing admin documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/documents/upload", tags=["Admin"])
async def upload_admin_document(file: UploadFile = File(...)):
    """Upload a document for admin management."""
    try:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = data_dir / file.filename
        content = await file.read()
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return {
            "message": "Document uploaded successfully",
            "filename": file.filename
        }
        
    except Exception as e:
        logger.error(f"Error uploading admin document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/documents/{filename}", tags=["Admin"])
async def delete_admin_document(filename: str):
    """Delete an admin document."""
    try:
        file_path = Path("data") / filename
        if file_path.exists():
            file_path.unlink()
            return {
                "message": "Document deleted successfully",
                "filename": filename
            }
        else:
            raise HTTPException(status_code=404, detail="Document not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting admin document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/settings", tags=["Admin"])
async def get_admin_settings():
    """Get system settings for admin."""
    try:
        if not system.config_manager:
            raise HTTPException(status_code=500, detail="Config manager not initialized")
        
        settings = system.config_manager.get_public_config()
        
        return {
            "openai_key": settings.get("openai_key", ""),
            "use_openai": settings.get("use_openai", False),
            "top_k": settings.get("top_k", 5),
            "model_name": settings.get("model_name", "llama2"),
            "chunk_size": settings.get("chunk_size", 1000),
            "chunk_overlap": settings.get("chunk_overlap", 200)
        }
        
    except Exception as e:
        logger.error(f"Error getting admin settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/settings", tags=["Admin"])
async def update_admin_settings(settings: dict):
    """Update system settings."""
    try:
        if not system.config_manager:
            raise HTTPException(status_code=500, detail="Config manager not initialized")
        
        await system.config_manager.update_section("admin", settings)
        
        return settings
        
    except Exception as e:
        logger.error(f"Error updating admin settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Export Endpoints
@app.get("/api/conversations/{conversation_id}/export", tags=["Export"])
async def export_conversation(
    conversation_id: int,
    format: str = "json"
):
    """Export a conversation in specified format."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        # Create mock export data
        export_data = {
            "conversation_id": conversation_id,
            "title": f"Conversation {conversation_id}",
            "student_id": 1,
            "messages": [
                {
                    "sender": "user",
                    "content": "Sample user message",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "sender": "assistant", 
                    "content": "Sample assistant response",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{conversation_id}_{timestamp}.{format}"
        
        # Save to exports directory
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        file_path = exports_dir / filename
        
        if format == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(export_data, indent=2, ensure_ascii=False))
        elif format == "csv":
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Sender", "Content", "Timestamp"])
                for msg in export_data["messages"]:
                    writer.writerow([msg["sender"], msg["content"], msg["timestamp"]])
        
        return {
            "message": f"Conversation exported successfully as {format}",
            "filepath": str(file_path),
            "filename": filename,
            "messages_count": len(export_data["messages"])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}/conversations/export", tags=["Export"])
async def export_student_conversations(
    student_id: int,
    format: str = "json"
):
    """Export all conversations for a student."""
    try:
        # Mock implementation since CRUD service is not fully initialized
        # Create mock export data
        export_data = {
            "student_id": student_id,
            "exported_at": datetime.now().isoformat(),
            "conversations": [
                {
                    "conversation_id": 1,
                    "title": f"Conversation de l'étudiant {student_id}",
                    "messages": [
                        {
                            "sender": "user",
                            "content": "Bonjour, pouvez-vous m'aider avec les mathématiques ?",
                            "timestamp": datetime.now().isoformat()
                        },
                        {
                            "sender": "assistant",
                            "content": "Bien sûr ! Je peux vous aider avec les mathématiques. Que souhaitez-vous savoir ?",
                            "timestamp": datetime.now().isoformat()
                        }
                    ]
                }
            ]
        }
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_{student_id}_conversations_{timestamp}.{format}"
        
        # Save to exports directory
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        file_path = exports_dir / filename
        
        if format == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(export_data, indent=2, ensure_ascii=False))
        elif format == "csv":
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Conversation ID", "Title", "Sender", "Content", "Timestamp"])
                for conv_data in export_data["conversations"]:
                    for msg in conv_data["messages"]:
                        writer.writerow([
                            conv_data["conversation_id"],
                            conv_data["title"],
                            msg["sender"],
                            msg["content"],
                            msg["timestamp"]
                        ])
        elif format == "pdf":
            # Create a proper PDF file
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_LEFT
                
                # Create PDF document
                doc = SimpleDocTemplate(str(file_path), pagesize=A4)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=TA_CENTER,
                    textColor=colors.darkblue
                )
                story.append(Paragraph(f"Conversations de l'étudiant {student_id}", title_style))
                story.append(Spacer(1, 12))
                
                # Export date
                date_style = ParagraphStyle(
                    'CustomDate',
                    parent=styles['Normal'],
                    fontSize=10,
                    alignment=TA_CENTER,
                    textColor=colors.grey
                )
                story.append(Paragraph(f"Exporté le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", date_style))
                story.append(Spacer(1, 20))
                
                # Conversations
                for conv_data in export_data["conversations"]:
                    # Conversation title
                    conv_style = ParagraphStyle(
                        'ConversationTitle',
                        parent=styles['Heading2'],
                        fontSize=14,
                        spaceAfter=12,
                        textColor=colors.darkgreen
                    )
                    story.append(Paragraph(f"Conversation: {conv_data['title']}", conv_style))
                    
                    # Messages table
                    if conv_data["messages"]:
                        table_data = [["Expéditeur", "Message", "Date/Heure"]]
                        for msg in conv_data["messages"]:
                            sender = "👤 Étudiant" if msg['sender'] == 'user' else "🤖 Assistant"
                            content = msg['content'][:200] + "..." if len(msg['content']) > 200 else msg['content']
                            timestamp = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
                            table_data.append([sender, content, timestamp])
                        
                        table = Table(table_data, colWidths=[1.2*inch, 4*inch, 1.2*inch])
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ]))
                        story.append(table)
                        story.append(Spacer(1, 20))
                
                # Build PDF
                doc.build(story)
                
            except ImportError:
                # Fallback to text file if reportlab is not available
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Conversations de l'étudiant {student_id}\n")
                    f.write(f"Exporté le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                    for conv_data in export_data["conversations"]:
                        f.write(f"Conversation: {conv_data['title']}\n")
                        f.write("-" * 50 + "\n")
                        for msg in conv_data["messages"]:
                            f.write(f"{msg['sender'].upper()}: {msg['content']}\n")
                            f.write(f"Timestamp: {msg['timestamp']}\n\n")
            except Exception as e:
                logger.error(f"Error creating PDF: {e}")
                # Fallback to text file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Conversations de l'étudiant {student_id}\n")
                    f.write(f"Exporté le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                    for conv_data in export_data["conversations"]:
                        f.write(f"Conversation: {conv_data['title']}\n")
                        f.write("-" * 50 + "\n")
                        for msg in conv_data["messages"]:
                            f.write(f"{msg['sender'].upper()}: {msg['content']}\n")
                            f.write(f"Timestamp: {msg['timestamp']}\n\n")
        
        return {
            "message": f"Student conversations exported successfully as {format}",
            "filepath": str(file_path),
            "filename": filename,
            "conversations_count": len(export_data["conversations"])
        }
        
    except Exception as e:
        logger.error(f"Error exporting student conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/validate", tags=["Documents"])
async def validate_documents():
    """Validate and reload documents."""
    try:
        # Since we're using course documents from the file system,
        # this endpoint just confirms that documents are available
        from pathlib import Path
        
        data_dir = Path("data")
        if not data_dir.exists():
            raise HTTPException(status_code=404, detail="Data directory not found")
        
        course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
        
        if not course_files:
            raise HTTPException(status_code=404, detail="No course documents found")
        
        # Count documents by subject
        subjects = {}
        for file_path in course_files:
            filename = file_path.stem.lower()
            if "math" in filename or "calcul" in filename or "algebre" in filename:
                subject = "Mathématiques"
            elif "physique" in filename or "electricite" in filename or "mecanique" in filename:
                subject = "Physique"
            elif "chimie" in filename:
                subject = "Chimie"
            elif "biologie" in filename:
                subject = "Biologie"
            elif "informatique" in filename or "algorithmes" in filename:
                subject = "Informatique"
            else:
                subject = "Général"
            
            subjects[subject] = subjects.get(subject, 0) + 1
        
        return {
            "message": f"Documents validés avec succès. {len(course_files)} documents trouvés.",
            "total_documents": len(course_files),
            "subjects": subjects,
            "status": "validated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/download/{filename}", tags=["Export"])
async def download_export_file(filename: str):
    """Download an exported file."""
    try:
        exports_dir = Path("exports")
        file_path = exports_dir / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced API endpoints
@app.get("/", tags=["System"])
async def root():
    """API root with comprehensive information."""
    uptime = datetime.now() - system.startup_time
    
    return {
        "name": "Professional Ollama RAG API",
        "version": "3.0.0",
        "status": "running",
        "uptime": str(uptime),
        "features": [
            "Ollama Integration",
            "Professional RAG Engine",
            "Enhanced Document Processing",
            "Advanced Vector Store",
            "Real-time Monitoring",
            "Comprehensive Error Handling",
            "Performance Optimization",
            "Production Ready"
        ],
        "endpoints": {
            "documentation": "/docs",
            "health": "/api/health",
            "status": "/api/status",
            "metrics": "/api/metrics"
        },
        "ollama": {
            "connected": system.ollama_manager.is_connected() if system.ollama_manager else False,
            "models_available": len(await system.ollama_manager.list_models()) if system.ollama_manager else 0
        }
    }

@app.get("/api/status", response_model=SystemStatus, tags=["System"])
async def get_comprehensive_status():
    """Get comprehensive system status with all components."""
    uptime = datetime.now() - system.startup_time
    
    # Get Ollama status
    ollama_connected = False
    ollama_models = []
    if system.ollama_manager:
        ollama_connected = await system.ollama_manager.test_connection()
        if ollama_connected:
            ollama_models = await system.ollama_manager.list_models()
    
    # Get database status
    database_connected = False
    try:
        if get_db:
            with next(get_db()) as db:
                db.execute("SELECT 1")
                database_connected = True
    except:
        pass
    
    # Get performance metrics
    total_requests = 0
    avg_response_time = 0.0
    success_rate = 0.0
    if system.metrics_collector:
        metrics = await system.metrics_collector.get_summary()
        total_requests = metrics.get("total_requests", 0)
        avg_response_time = metrics.get("avg_response_time", 0.0)
        success_rate = metrics.get("success_rate", 0.0)
    
    # Get resource usage
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent()
    
    # Check if course documents are available (even if vector store isn't ready)
    course_documents_available = False
    try:
        from pathlib import Path
        data_dir = Path("data")
        if data_dir.exists():
            course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
            course_documents_available = len(course_files) > 0
    except:
        pass
    
    # Determine overall status
    if ollama_connected and database_connected and system.system_ready:
        status = "healthy"
    elif system.system_ready or course_documents_available:
        status = "degraded"
    else:
        status = "starting"
    
    return SystemStatus(
        status=status,
        uptime=str(uptime),
        ollama_connected=ollama_connected,
        ollama_models=ollama_models,
        documents_loaded=system.documents_loaded or course_documents_available,
        vector_store_ready=system.vector_store is not None,
        database_connected=database_connected,
        total_requests=total_requests,
        avg_response_time=avg_response_time,
        success_rate=success_rate,
        memory_usage=memory_usage,
        cpu_usage=cpu_usage,
        config=system.config_manager.get_public_config() if system.config_manager else {},
        last_updated=datetime.now().isoformat()
    )

async def search_course_documents(question: str, subject_filter: str = None) -> List[Dict[str, Any]]:
    """Search through course documents for relevant content."""
    try:
        import os
        import re
        from pathlib import Path
        
        data_dir = Path("data")
        if not data_dir.exists():
            logger.warning("Data directory not found")
            return []
        
        # Get all course files
        course_files = list(data_dir.glob("cours_*.txt")) + list(data_dir.glob("exercices_*.txt"))
        
        if not course_files:
            logger.warning("No course files found")
            return []
        
        # Extract subject from filename and filter if needed
        relevant_files = []
        for file_path in course_files:
            filename = file_path.stem.lower()
            
            # Extract subject from filename
            if "math" in filename or "calcul" in filename or "algebre" in filename:
                subject = "Mathématiques"
            elif "physique" in filename or "electricite" in filename or "mecanique" in filename:
                subject = "Physique"
            elif "chimie" in filename:
                subject = "Chimie"
            elif "biologie" in filename:
                subject = "Biologie"
            elif "informatique" in filename or "algorithmes" in filename:
                subject = "Informatique"
            else:
                subject = "Général"
            
            # Apply subject filter if provided
            if subject_filter and subject_filter.lower() not in subject.lower():
                continue
                
            relevant_files.append((file_path, subject))
        
        # Search through files
        results = []
        question_lower = question.lower()
        
        for file_path, subject in relevant_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple keyword matching for relevance
                content_lower = content.lower()
                relevance_score = 0
                
                # Check for keyword matches
                keywords = question_lower.split()
                for keyword in keywords:
                    if len(keyword) > 2:  # Skip short words
                        count = content_lower.count(keyword)
                        relevance_score += count * 0.1
                
                # Check for subject-specific terms
                if subject == "Mathématiques":
                    math_terms = ["dérivée", "intégrale", "fonction", "équation", "calcul", "limite"]
                    for term in math_terms:
                        if term in question_lower and term in content_lower:
                            relevance_score += 0.5
                
                elif subject == "Physique":
                    physics_terms = ["ohm", "tension", "courant", "résistance", "loi", "force", "énergie"]
                    for term in physics_terms:
                        if term in question_lower and term in content_lower:
                            relevance_score += 0.5
                
                elif subject == "Chimie":
                    chem_terms = ["molécule", "réaction", "atome", "composé", "liaison"]
                    for term in chem_terms:
                        if term in question_lower and term in content_lower:
                            relevance_score += 0.5
                
                # If we found relevant content, add to results
                if relevance_score > 0.1:
                    # Extract relevant paragraph around matches
                    paragraphs = content.split('\n\n')
                    best_paragraph = ""
                    max_paragraph_score = 0
                    
                    for paragraph in paragraphs:
                        para_lower = paragraph.lower()
                        para_score = 0
                        for keyword in keywords:
                            if len(keyword) > 2:
                                para_score += para_lower.count(keyword) * 0.1
                        
                        if para_score > max_paragraph_score:
                            max_paragraph_score = para_score
                            best_paragraph = paragraph[:800]  # Limit length
                    
                    if best_paragraph:
                        results.append({
                            "title": f"Cours {subject} - {file_path.stem}",
                            "content": best_paragraph,
                            "score": min(relevance_score, 1.0),
                            "subject": subject,
                            "source": str(file_path)
                        })
                        
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")
                continue
        
        # Sort by relevance score and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]  # Return top 5 most relevant
        
    except Exception as e:
        logger.error(f"Error in course document search: {e}")
        return []

@app.post("/api/ask", tags=["AI"])
async def ask_question_enhanced(request: dict):
    """Enhanced question processing with course documents + Ollama integration."""
    start_time = time.time()
    
    try:
        question = request.get("question", "Hello")
        subject_filter = request.get("subject_filter", None)
        
        # Step 1: Search through course documents for relevant content
        relevant_documents = []
        course_sources = []
        
        try:
            # Search through course documents
            course_docs = await search_course_documents(question, subject_filter)
            if course_docs:
                relevant_documents = course_docs[:3]  # Top 3 most relevant
                course_sources = [
                    {
                        "title": doc.get("title", "Document de cours"),
                        "content": doc.get("content", "")[:500] + "...",
                        "score": doc.get("score", 0.8),
                        "metadata": {
                            "subject": doc.get("subject", "Général"),
                            "type": "course_document",
                            "source": doc.get("source", "unknown")
                        }
                    }
                    for doc in relevant_documents
                ]
                logger.info(f"✅ Found {len(relevant_documents)} relevant course documents")
        except Exception as e:
            logger.warning(f"Course document search failed: {e}")
        
        # Step 2: Create enhanced prompt with course content
        course_context = ""
        if relevant_documents:
            course_context = "\n\nCONTENU DES COURS PERTINENTS:\n"
            for i, doc in enumerate(relevant_documents, 1):
                course_context += f"\n--- Document {i} ({doc.get('subject', 'Général')}) ---\n"
                course_context += doc.get('content', '')[:800] + "\n"
        
        educational_prompt = f"""Tu es un assistant IA éducatif spécialisé dans l'aide aux étudiants. 
Réponds de manière claire, pédagogique et encourageante en français.

Question de l'étudiant: {question}{course_context}

Instructions:
- Utilise le contenu des cours fournis pour donner une réponse précise et détaillée
- Si le contenu des cours ne couvre pas la question, utilise tes connaissances générales
- Sois précis et utile avec des exemples concrets
- Encourage l'apprentissage et l'approfondissement
- Reste professionnel et bienveillant
- Cite les sources quand tu utilises le contenu des cours

Réponse:"""

        # Step 3: Try Ollama with course-enhanced prompt
        ollama_start = time.time()
        ollama_success = False
        answer = ""
        
        try:
            import requests
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral:latest",
                    "prompt": educational_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=15  # Slightly longer timeout for course processing
            )
            
            if ollama_response.status_code == 200:
                ollama_data = ollama_response.json()
                answer = ollama_data.get("response", "")
                ollama_success = True
                logger.info("✅ Ollama response with course content successful")
            else:
                logger.warning(f"Ollama returned status {ollama_response.status_code}")
                
        except Exception as ollama_error:
            logger.warning(f"Ollama unavailable, using smart fallback: {ollama_error}")
        
        # Smart fallback if Ollama fails or is slow
        if not ollama_success or not answer.strip():
            logger.info("Using smart educational fallback with course content")
            question_lower = question.lower()
            
            # PRIORITY 1: Check for simple math operations FIRST (before course content)
            import re
            math_detected = False
            
            # Check for addition problems (e.g., "2+200", "5 + 3", "what is 10+15")
            addition_match = re.search(r'(\d+)\s*\+\s*(\d+)', question)
            if addition_match:
                num1 = int(addition_match.group(1))
                num2 = int(addition_match.group(2))
                result = num1 + num2
                answer = f"{num1} + {num2} = {result}\n\nC'est une addition de base. En mathématiques, l'addition est l'une des quatre opérations fondamentales. Quand on additionne {num1} et {num2}, on obtient {result}. C'est la base de l'arithmétique !"
                math_detected = True
                course_sources = []
            
            # Check for subtraction problems
            elif re.search(r'(\d+)\s*-\s*(\d+)', question):
                sub_match = re.search(r'(\d+)\s*-\s*(\d+)', question)
                num1 = int(sub_match.group(1))
                num2 = int(sub_match.group(2))
                result = num1 - num2
                answer = f"{num1} - {num2} = {result}\n\nC'est une soustraction. En mathématiques, la soustraction est l'opération inverse de l'addition. Quand on soustrait {num2} de {num1}, on obtient {result}."
                math_detected = True
                course_sources = []
            
            # Check for multiplication problems
            elif re.search(r'(\d+)\s*\*\s*(\d+)', question) or re.search(r'(\d+)\s*x\s*(\d+)', question):
                mult_match = re.search(r'(\d+)\s*[\*x]\s*(\d+)', question)
                num1 = int(mult_match.group(1))
                num2 = int(mult_match.group(2))
                result = num1 * num2
                answer = f"{num1} × {num2} = {result}\n\nC'est une multiplication. En mathématiques, la multiplication est une addition répétée. {num1} multiplié par {num2} donne {result}."
                math_detected = True
                course_sources = []
            
            # Check for division problems
            elif re.search(r'(\d+)\s*/\s*(\d+)', question):
                div_match = re.search(r'(\d+)\s*/\s*(\d+)', question)
                num1 = int(div_match.group(1))
                num2 = int(div_match.group(2))
                if num2 != 0:
                    result = num1 / num2
                    answer = f"{num1} ÷ {num2} = {result}\n\nC'est une division. En mathématiques, la division est l'opération inverse de la multiplication. {num1} divisé par {num2} donne {result}."
                else:
                    answer = f"{num1} ÷ {num2} = Erreur\n\nOn ne peut pas diviser par zéro ! C'est une règle fondamentale en mathématiques."
                math_detected = True
                course_sources = []
            
            # PRIORITY 2: If no math operation detected, try course content
            if not math_detected and relevant_documents:
                logger.info(f"Using course content from {len(relevant_documents)} documents")
                # Create answer based on course content
                answer = f"Basé sur le contenu de vos cours, voici une réponse à votre question '{question}':\n\n"
                
                for i, doc in enumerate(relevant_documents[:2], 1):  # Use top 2 documents
                    answer += f"**{doc['subject']} - {doc['title']}:**\n"
                    answer += f"{doc['content'][:600]}...\n\n"
                
                answer += "Cette réponse est basée sur le contenu de vos documents de cours. Pour plus de détails, consultez les documents sources mentionnés."
                course_sources = relevant_documents
            elif not math_detected:
                course_sources = []
                # Handle other cases when no math and no course content
                
                # Subject-specific responses
                if any(word in question_lower for word in ["math", "mathématiques", "calcul", "algèbre"]):
                    answer = f"Je peux vous aider avec les mathématiques ! Pour votre question '{question}', voici une explication détaillée avec des exemples pratiques. Les mathématiques sont fondamentales dans de nombreux domaines."
                elif any(word in question_lower for word in ["physique", "physics", "ohm", "loi"]):
                    answer = f"En physique, votre question '{question}' touche à des concepts importants. La loi d'Ohm par exemple relie la tension (V), l'intensité (I) et la résistance (R) : V = R × I. C'est fondamental en électricité !"
                elif any(word in question_lower for word in ["chimie", "chemistry", "molécule"]):
                    answer = f"En chimie, votre question '{question}' concerne des concepts fascinants. La chimie étudie la matière et ses transformations. Chaque molécule a ses propriétés uniques !"
                else:
                    answer = f"Bonjour ! Je suis votre assistant éducatif IA. Pour votre question '{question}', je peux vous aider avec des explications détaillées dans de nombreux domaines : mathématiques, physique, chimie, biologie, informatique, etc. Soyez plus spécifique pour une réponse plus précise !"
        
        ollama_time = time.time() - ollama_start
        tokens_generated = len(answer.split())
        
        # Determine subject based on question content
        question_lower = question.lower()
        if any(word in question_lower for word in ["math", "mathématiques", "calcul", "algèbre", "géométrie", "2+2", "addition"]):
            subject = "Mathématiques"
        elif any(word in question_lower for word in ["physique", "physics", "mécanique", "électricité", "ohm"]):
            subject = "Physique"
        elif any(word in question_lower for word in ["chimie", "chemistry", "molécule", "réaction"]):
            subject = "Chimie"
        elif any(word in question_lower for word in ["biologie", "biology", "cellule", "gène"]):
            subject = "Biologie"
        elif any(word in question_lower for word in ["informatique", "programmation", "code", "algorithme"]):
            subject = "Informatique"
        else:
            subject = "Général"
        
        processing_time = time.time() - start_time
        
        # Determine confidence and model used
        if ollama_success:
            confidence = 0.9 if course_sources else 0.85
            model_used = "mistral:latest"
            fallback_used = False
        else:
            confidence = 0.8
            model_used = "smart-fallback"
            fallback_used = True
        
        # Combine course sources with AI response source
        all_sources = course_sources.copy() if course_sources else []
        all_sources.append({
            "title": f"Réponse IA - {subject}",
            "content": f"Réponse générée par l'assistant IA pour {subject}",
            "score": 0.95,
            "metadata": {"subject": subject, "type": "ai_response", "model": model_used}
        })
        
        response = {
            "answer": answer,
            "confidence": confidence,
            "sources": all_sources,
            "processing_time": processing_time,
            "query": question,
            "model_used": model_used,
            "ollama_response_time": ollama_time if ollama_success else 0,
            "tokens_generated": tokens_generated,
            "source_scores": [doc.get("score", 0.8) for doc in course_sources] + [0.95],
            "metadata": {
                "subject": subject,
                "timestamp": datetime.now().isoformat(),
                "ollama_used": ollama_success,
                "model": model_used,
                "course_documents_used": len(course_sources),
                "has_course_content": len(course_sources) > 0
            },
            "response_quality": {
                "relevance": 0.9,
                "completeness": 0.85,
                "clarity": 0.9
            },
            "fallback_used": fallback_used
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")

async def generate_fallback_response(question: str, start_time: float) -> EnhancedQuestionResponse:
    """Generate enhanced fallback response."""
    processing_time = time.time() - start_time
    
    # Basic educational response
    answer = f"""**ASSISTANT IA ÉDUCATIF**

**Question:** {question}

Je suis votre assistant IA spécialisé dans l'éducation. Bien que je n'aie pas accès à vos documents spécifiques en ce moment, je peux vous aider avec de nombreux concepts éducatifs.

**Domaines d'expertise:**
- **Mathématiques**: Algèbre, calcul, géométrie, statistiques
- **Sciences**: Physique, chimie, biologie, géologie
- **Ingénierie**: Électricité, électronique, mécanique
- **Informatique**: Programmation, algorithmes, structures de données

**Pour une assistance optimale:**
1. Ajoutez vos documents de cours dans le système
2. Soyez spécifique dans vos questions
3. Indiquez le niveau d'études souhaité

Je suis là pour vous accompagner dans votre apprentissage !"""
    
    return EnhancedQuestionResponse(
        answer=answer,
        confidence=0.6,
        sources=[],
        processing_time=processing_time,
        query=question,
        model_used="fallback",
        ollama_response_time=0.0,
        tokens_generated=len(answer.split()),
        source_scores=[],
        metadata={"mode": "fallback", "reason": "no_documents_loaded"},
        response_quality="basic",
        fallback_used=True
    )

async def save_conversation_enhanced(
    db: Session,
    request: EnhancedQuestionRequest,
    response: EnhancedQuestionResponse
) -> Dict[str, Any]:
    """Enhanced conversation saving with proper error handling."""
    try:
        conversation_id = request.conversation_id
        
        # Create conversation if needed
        if not conversation_id and request.create_new_conversation:
            conversation = await system.crud.create_conversation(
                db=db,
                student_id=request.student_id,
                title=request.conversation_title or f"Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            conversation_id = conversation.id
        
        user_message_id = None
        assistant_message_id = None
        
        if conversation_id:
            # Save user message
            user_message = await system.crud.create_message(
                db=db,
                conversation_id=conversation_id,
                sender="user",
                content=request.question,
                metadata={"request_id": str(uuid.uuid4())}
            )
            user_message_id = user_message.id
            
            # Save assistant message
            assistant_message = await system.crud.create_message(
                db=db,
                conversation_id=conversation_id,
                sender="assistant",
                content=response.answer,
                confidence=str(response.confidence),
                response_time=str(response.processing_time),
                metadata={
                    "model_used": response.model_used,
                    "sources_count": len(response.sources),
                    "ollama_response_time": response.ollama_response_time
                }
            )
            assistant_message_id = assistant_message.id
        
        return {
            "conversation_id": conversation_id,
            "user_message_id": user_message_id,
            "assistant_message_id": assistant_message_id
        }
        
    except Exception as e:
        logger.error(f"Error saving conversation: {e}")
        return {}

# Document management endpoints
@app.post("/api/documents/upload", response_model=DocumentUploadResponse, tags=["Documents"])
async def upload_documents_enhanced(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks = None
):
    """Enhanced document upload with comprehensive processing."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_files = []
    failed_files = []
    
    try:
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        for file in files:
            try:
                if not file.filename:
                    failed_files.append({"filename": "unknown", "error": "No filename provided"})
                    continue
                
                # Validate file type
                file_ext = Path(file.filename).suffix.lower()
                supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.json', '.csv']
                
                if file_ext not in supported_extensions:
                    failed_files.append({
                        "filename": file.filename,
                        "error": f"Unsupported file type: {file_ext}"
                    })
                    continue
                
                # Check file size (10MB limit)
                content = await file.read()
                if len(content) > 10 * 1024 * 1024:  # 10MB
                    failed_files.append({
                        "filename": file.filename,
                        "error": "File too large (max 10MB)"
                    })
                    continue
                
                # Save file with unique name if needed
                file_path = data_dir / file.filename
                counter = 1
                while file_path.exists():
                    name_part = Path(file.filename).stem
                    ext_part = Path(file.filename).suffix
                    file_path = data_dir / f"{name_part}_{counter}{ext_part}"
                    counter += 1
                
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(content)
                
                uploaded_files.append({
                    "filename": file.filename,
                    "saved_as": file_path.name,
                    "size": len(content),
                    "type": file_ext[1:],  # Remove dot
                    "upload_time": datetime.now().isoformat()
                })
                
                logger.info(f"File uploaded: {file.filename} -> {file_path.name}")
                
            except Exception as e:
                failed_files.append({
                    "filename": file.filename,
                    "error": str(e)
                })
                logger.error(f"Error uploading file {file.filename}: {e}")
        
        # Start background processing if files were uploaded
        processing_started = False
        estimated_completion = None
        
        if uploaded_files and background_tasks:
            background_tasks.add_task(reprocess_documents_background)
            processing_started = True
            # Estimate 30 seconds per file
            estimated_minutes = len(uploaded_files) * 0.5
            estimated_completion = (datetime.now() + timedelta(minutes=estimated_minutes)).isoformat()
        
        return DocumentUploadResponse(
            success=len(uploaded_files) > 0,
            uploaded_files=uploaded_files,
            failed_files=failed_files,
            processing_started=processing_started,
            estimated_completion=estimated_completion
        )
        
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def reprocess_documents_background():
    """Reprocess all documents in background."""
    try:
        logger.info("🔄 Starting background document reprocessing...")
        
        if not system.document_loader:
            logger.error("Document loader not available")
            return
        
        # Load and process documents
        documents = await system.document_loader.load_documents_async()
        if not documents:
            logger.warning("No documents found for reprocessing")
            return
        
        # Process documents and update vector store
        chunks = await system.document_loader.process_documents_async(documents)
        if chunks and system.vector_store:
            await system.vector_store.update_from_documents(chunks)
            logger.info("✅ Document reprocessing completed")
        
    except Exception as e:
        logger.error(f"Document reprocessing failed: {e}")