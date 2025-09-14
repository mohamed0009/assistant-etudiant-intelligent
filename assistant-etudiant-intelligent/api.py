"""
API FastAPI pour l'Assistant Étudiant Intelligent
Interface API pour communiquer avec le système RAG.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine
from src.metrics_service import MetricsService
from src.models import QuestionType, SubjectType
from src.export_service import ExportService
from src.db import get_db, init_db
from src import crud
from src.models_db import Student, Conversation, Message

# Modèles Pydantic
class QuestionRequest(BaseModel):
    question: str
    subject_filter: Optional[str] = None
    # Persistence options
    save: Optional[bool] = True
    conversation_id: Optional[int] = None
    student_id: Optional[int] = None
    create_conversation: Optional[bool] = False
    title: Optional[str] = None

class QuestionResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[Dict[str, Any]]
    processing_time: float
    query: str
    conversation_id: Optional[int] = None
    user_message_id: Optional[int] = None
    assistant_message_id: Optional[int] = None

class SystemStatus(BaseModel):
    documents_loaded: bool
    total_vectors: int
    model: str
    llm_configured: bool

class DocumentStats(BaseModel):
    total_documents: int
    total_chunks: int
    subjects: List[str]

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Assistant Étudiant Intelligent API",
    description="API pour l'assistant étudiant intelligent basé sur RAG",
    version="1.0.0"
)

# Configuration CORS pour Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
rag_engine = None
vector_store = None
documents_loaded = False
metrics_service = MetricsService()
export_service = ExportService()

@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage de l'API."""
    global rag_engine, vector_store, documents_loaded
    
    try:
        # Init DB
        init_db()
        
        # Charger les documents automatiquement au démarrage
        print("🔄 Chargement automatique des documents...")
        success = await load_documents()
        if success:
            print("✅ Documents chargés automatiquement")
        else:
            print("⚠️ Aucun document trouvé, l'API fonctionne sans base de connaissances")
        print("✅ API démarrée avec succès")
    except Exception as e:
        print(f"⚠️ Erreur lors du démarrage: {e}")
        print("✅ API démarrée sans base de connaissances")

async def load_documents():
    """Charge et configure les documents."""
    global rag_engine, vector_store, documents_loaded
    
    try:
        # Charger les documents
        loader = DocumentLoader()
        documents = loader.load_documents()
        
        if not documents:
            print("⚠️ Aucun document trouvé")
            return False
        
        # Segmenter les documents
        chunks = loader.split_documents(documents)
        print(f"📝 {len(chunks)} segments créés")
        
        # Créer la base vectorielle
        vector_store = VectorStore()
        success = vector_store.create_vector_store(chunks)
        
        if not success:
            print("❌ Erreur création base vectorielle")
            return False
        
        # Initialiser le moteur RAG
        rag_engine = RAGEngine(vector_store)
        documents_loaded = True
        
        print(f"✅ {len(documents)} documents chargés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur chargement: {e}")
        return False

@app.get("/")
async def root():
    """Point d'entrée de l'API."""
    return {
        "message": "Assistant Étudiant Intelligent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/status")
async def get_status() -> SystemStatus:
    """Récupère le statut du système."""
    global documents_loaded, vector_store, rag_engine
    
    if vector_store:
        info = vector_store.get_vector_store_info()
        return SystemStatus(
            documents_loaded=documents_loaded,
            total_vectors=info.get('total_vectors', 0),
            model=info.get('model', 'N/A'),
            llm_configured=rag_engine is not None
        )
    else:
        return SystemStatus(
            documents_loaded=False,
            total_vectors=0,
            model="N/A",
            llm_configured=False
        )

@app.get("/api/stats")
async def get_stats() -> DocumentStats:
    """Récupère les statistiques des documents."""
    global documents_loaded
    
    if not documents_loaded:
        # Retourner des statistiques vides si pas de documents
        return DocumentStats(
            total_documents=0,
            total_chunks=0,
            subjects=[]
        )
    
    try:
        loader = DocumentLoader()
        documents = loader.load_documents()
        chunks = loader.split_documents(documents)
        
        # Extraire les sujets uniques
        subjects = list(set([
            doc.metadata.get("subject", "Général") 
            for doc in documents 
            if doc.metadata.get("subject")
        ]))
        
        return DocumentStats(
            total_documents=len(documents),
            total_chunks=len(chunks),
            subjects=subjects
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask")
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db)) -> QuestionResponse:
    """Pose une question à l'assistant."""
    global rag_engine, documents_loaded, metrics_service
    
    start_time = time.time()
    
    if not documents_loaded or not rag_engine:
        # Retourner une réponse générique si pas de documents
        response = QuestionResponse(
            answer="**ASSISTANT IA UNIVERSITAIRE**\n\nBonjour ! Je suis votre assistant IA spécialisé dans l'aide aux étudiants.\n\n**Statut actuel :**\nActuellement, je n'ai pas encore accès à vos documents de cours, mais je peux vous aider avec des questions générales sur les matières universitaires.\n\n**Matières disponibles :**\n- Mathématiques (calcul différentiel, algèbre linéaire)\n- Physique (mécanique, électromagnétisme, thermodynamique, optique)\n- Électricité et électronique\n- Chimie (générale et organique)\n- Informatique (algorithmes, structures de données)\n- Biologie (cellulaire, moléculaire)\n- Géologie (structure de la Terre, tectonique des plaques)\n- Astronomie (système solaire, étoiles, galaxies)\n- Psychologie (comportement, cognition, développement)\n\n**Pour des réponses complètes et détaillées :**\n1. Ajoutez vos documents de cours dans le dossier 'data/'\n2. Utilisez le bouton 'Recharger' pour mettre à jour la base de connaissances\n3. Posez vos questions - je vous donnerai des réponses complètes avec exemples pratiques\n\n**Exemple de question :**\n\"Explique-moi la loi d'Ohm avec un exemple pratique\"\n\nJe suis là pour vous aider à réussir vos études !",
            confidence=0.5,
            sources=[],
            processing_time=0.1,
            query=request.question
        )
        
        # Enregistrer les métriques
        processing_time = time.time() - start_time
        subject = metrics_service.detect_subject(request.question)
        metrics_service.record_question(
            question=request.question,
            response_time=processing_time,
            confidence=response.confidence,
            question_type=QuestionType.PRECOMPUTED,
            subject=subject,
            user_id="anonymous",
            sources_used=0,
            db=db,
        )
        
        # Optionally persist the question/answer even without documents
        user_msg_id = None
        assistant_msg_id = None
        conv_id = None
        if request.save and request.student_id:
            try:
                conv_id = request.conversation_id
                if not conv_id and request.create_conversation:
                    conv = crud.create_conversation(db, student_id=request.student_id, title=request.title or "Conversation")
                    conv_id = conv.id
                if conv_id:
                    # Save user question
                    user_msg = crud.add_message(db, conversation_id=conv_id, sender="user", content=request.question)
                    user_msg_id = user_msg.id
                    # Save assistant answer
                    assistant_msg = crud.add_message(db, conversation_id=conv_id, sender="assistant", content=response.answer, confidence=str(response.confidence), response_time=str(processing_time))
                    assistant_msg_id = assistant_msg.id
            except Exception as _:
                pass
        
        response.conversation_id = conv_id
        response.user_message_id = user_msg_id
        response.assistant_message_id = assistant_msg_id
        return response
    
    try:
        # Create conversation if needed and save the user question
        conv_id = request.conversation_id
        user_msg_id = None
        assistant_msg_id = None
        if request.save and request.student_id:
            if not conv_id and request.create_conversation:
                conv = crud.create_conversation(db, student_id=request.student_id, title=request.title or "Conversation")
                conv_id = conv.id
            if conv_id:
                user_msg = crud.add_message(db, conversation_id=conv_id, sender="user", content=request.question)
                user_msg_id = user_msg.id
        # Obtenir la réponse
        response = rag_engine.ask_question(
            question=request.question,
            subject_filter=request.subject_filter
        )
        
        processing_time = time.time() - start_time
        
        # Convertir les sources en format JSON
        sources = []
        for source in response.sources:
            sources.append({
                "content": source.page_content[:200] + "..." if len(source.page_content) > 200 else source.page_content,
                "source": source.metadata.get("source", "Document inconnu"),
                "subject": source.metadata.get("subject", "Général")
            })
        
        # Déterminer le type de question et le sujet
        subject = metrics_service.detect_subject(request.question)
        question_type = QuestionType.PRECOMPUTED if len(sources) == 0 else QuestionType.DOCUMENT_BASED
        
        # Enregistrer les métriques
        metrics_service.record_question(
            question=request.question,
            response_time=processing_time,
            confidence=response.confidence,
            question_type=question_type,
            subject=subject,
            user_id="anonymous",
            sources_used=len(sources),
            db=db,
        )
        
        resp = QuestionResponse(
            answer=response.answer,
            confidence=response.confidence,
            sources=sources,
            processing_time=processing_time,
            query=response.query,
            conversation_id=conv_id,
            user_message_id=user_msg_id,
            assistant_message_id=None,
        )
        # Save assistant answer message
        if request.save and request.student_id and conv_id:
            try:
                assistant_msg = crud.add_message(
                    db,
                    conversation_id=conv_id,
                    sender="assistant",
                    content=resp.answer,
                    confidence=str(resp.confidence),
                    response_time=str(processing_time),
                )
                resp.assistant_message_id = assistant_msg.id
            except Exception as _:
                pass
        return resp
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/suggestions")
async def get_suggestions(subject: Optional[str] = None) -> List[str]:
    """Récupère les questions suggérées."""
    global rag_engine, documents_loaded
    
    if not documents_loaded or not rag_engine:
        return []
    
    try:
        suggestions = rag_engine.get_suggested_questions(subject)
        return suggestions
    except Exception as e:
        print(f"Erreur suggestions: {e}")
        return []

@app.post("/api/reload")
async def reload_documents():
    """Recharge les documents."""
    global documents_loaded
    
    try:
        success = await load_documents()
        if success:
            return {"message": "Documents rechargés avec succès"}
        else:
            raise HTTPException(status_code=500, detail="Erreur lors du rechargement")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Vérification de santé de l'API."""
    return {
        "status": "healthy",
        "documents_loaded": documents_loaded,
        "rag_engine_ready": rag_engine is not None
    }

# Nouveaux endpoints pour les métriques et l'administration

@app.get("/api/metrics")
async def get_performance_metrics(db: Session = Depends(get_db)):
    """Récupère les métriques de performance en temps réel."""
    global metrics_service
    try:
        metrics = metrics_service.get_performance_metrics(db)
        return metrics.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics/recent")
async def get_recent_questions(limit: int = 10, db: Session = Depends(get_db)):
    """Récupère les questions récentes."""
    global metrics_service
    try:
        recent_questions = metrics_service.get_recent_questions(limit, db)
        return [q.dict() for q in recent_questions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics/sessions/{user_id}")
async def get_user_sessions(user_id: str, db: Session = Depends(get_db)):
    """Récupère les sessions d'un utilisateur."""
    global metrics_service
    try:
        sessions = metrics_service.get_user_sessions(user_id, db)
        return [s.dict() for s in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/metrics/sessions/{user_id}/start")
async def start_user_session(user_id: str, db: Session = Depends(get_db)):
    """Démarre une nouvelle session utilisateur."""
    global metrics_service
    try:
        metrics_service.start_user_session(user_id, db)
        return {"message": "Session démarrée", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/metrics/sessions/{user_id}/end")
async def end_user_session(user_id: str, db: Session = Depends(get_db)):
    """Termine la session active d'un utilisateur."""
    global metrics_service
    try:
        metrics_service.end_user_session(user_id, db)
        return {"message": "Session terminée", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints d'administration
@app.get("/api/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    """Récupère les statistiques d'administration."""
    global documents_loaded, rag_engine, metrics_service
    try:
        metrics = metrics_service.get_performance_metrics(db)
        
        # Statistiques système
        system_health = "healthy" if documents_loaded and rag_engine else "degraded"
        documents_count = len(os.listdir("data")) if os.path.exists("data") else 0
        active_users = metrics.total_users
        error_rate = 0.0  # À calculer avec les logs d'erreur
        uptime = time.time()  # À améliorer avec un timestamp de démarrage
        
        return {
            "system_health": system_health,
            "documents_count": documents_count,
            "active_users": active_users,
            "error_rate": error_rate,
            "uptime": uptime,
            "last_backup": None,  # À implémenter
            "performance_metrics": metrics.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/backup")
async def create_backup():
    """Crée une sauvegarde du système."""
    try:
        # Créer un dossier de sauvegarde avec timestamp
        backup_dir = f"backups/backup_{int(time.time())}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copier les fichiers importants
        import shutil
        if os.path.exists("data"):
            shutil.copytree("data", f"{backup_dir}/data")
        
        return {
            "message": "Sauvegarde créée avec succès",
            "backup_path": backup_dir,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints d'export et sauvegarde

@app.get("/api/export/conversations")
async def export_conversations(format: str = "json", db: Session = Depends(get_db)):
    """Exporte les conversations dans le format spécifié."""
    global export_service, metrics_service
    try:
        # Récupérer les questions récentes comme conversations
        recent_questions = metrics_service.get_recent_questions(limit=1000, db=db)
        conversations = [q.dict() for q in recent_questions]
        
        if format.lower() == "json":
            filepath = export_service.export_conversations_json(conversations)
        elif format.lower() == "csv":
            filepath = export_service.export_conversations_csv(conversations)
        else:
            raise HTTPException(status_code=400, detail="Format non supporté. Utilisez 'json' ou 'csv'")
        
        return {
            "message": f"Export {format} créé avec succès",
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "conversations_count": len(conversations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/metrics")
async def export_metrics(format: str = "json", db: Session = Depends(get_db)):
    """Exporte les métriques dans le format spécifié."""
    global export_service, metrics_service
    try:
        metrics = metrics_service.get_performance_metrics(db)
        
        if format.lower() == "json":
            filepath = export_service.export_metrics_json(metrics)
        elif format.lower() == "csv":
            filepath = export_service.export_metrics_csv(metrics)
        else:
            raise HTTPException(status_code=400, detail="Format non supporté. Utilisez 'json' ou 'csv'")
        
        return {
            "message": f"Export métriques {format} créé avec succès",
            "filepath": filepath,
            "filename": os.path.basename(filepath)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export/backup")
async def create_full_backup(include_data: bool = True, include_metrics: bool = True):
    """Crée une sauvegarde complète du système."""
    global export_service
    try:
        filepath = export_service.create_full_backup(include_data, include_metrics)
        
        return {
            "message": "Sauvegarde complète créée avec succès",
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "includes_data": include_data,
            "includes_metrics": include_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/list")
async def list_exports():
    """Liste tous les fichiers d'export disponibles."""
    global export_service
    try:
        exports = export_service.list_exports()
        return {
            "exports": exports,
            "total": len(exports)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------- Conversation exports --------

@app.get("/api/conversations/{conversation_id}/export")
async def export_conversation(conversation_id: int, format: str = "json", db: Session = Depends(get_db)):
    """Exporte une conversation (messages) en JSON ou CSV."""
    try:
        # Ensure conversation exists
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation introuvable")

        messages = crud.get_conversation_messages(db, conversation_id)
        records = [
            {
                "conversation_id": m.conversation_id,
                "sender": m.sender,
                "content": m.content,
                "confidence": m.confidence,
                "response_time": m.response_time,
                "created_at": m.created_at,
            }
            for m in messages
        ]

        if format.lower() == "json":
            filename = f"conversation_{conversation_id}.json"
            filepath = export_service.export_conversations_json(records, filename=filename)
        elif format.lower() == "csv":
            filename = f"conversation_{conversation_id}.csv"
            filepath = export_service.export_conversations_csv(records, filename=filename)
        else:
            raise HTTPException(status_code=400, detail="Format non supporté. Utilisez 'json' ou 'csv'")

        return {
            "message": f"Export {format} créé avec succès",
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "messages_count": len(records),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/students/{student_id}/conversations/export")
async def export_student_conversations(student_id: int, format: str = "json", db: Session = Depends(get_db)):
    """Exporte toutes les conversations d'un étudiant en un seul fichier."""
    try:
        student = crud.get_student(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant introuvable")

        conversations = crud.get_student_conversations(db, student_id)
        full_payload = []
        for conv in conversations:
            messages = crud.get_conversation_messages(db, conv.id)
            full_payload.append({
                "conversation_id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
                "messages": [
                    {
                        "sender": m.sender,
                        "content": m.content,
                        "confidence": m.confidence,
                        "response_time": m.response_time,
                        "created_at": m.created_at,
                    }
                    for m in messages
                ],
            })

        if format.lower() == "json":
            filename = f"student_{student_id}_conversations.json"
            filepath = export_service.export_conversations_json(full_payload, filename=filename)
        elif format.lower() == "csv":
            # Flatten messages for CSV
            flattened = []
            for conv in full_payload:
                for m in conv["messages"]:
                    row = {
                        "conversation_id": conv["conversation_id"],
                        "title": conv["title"],
                        "sender": m["sender"],
                        "content": m["content"],
                        "confidence": m["confidence"],
                        "response_time": m["response_time"],
                        "message_created_at": m["created_at"],
                    }
                    flattened.append(row)
            filename = f"student_{student_id}_conversations.csv"
            filepath = export_service.export_conversations_csv(flattened, filename=filename)
        elif format.lower() == "pdf":
            filename = f"student_{student_id}_conversations.pdf"
            filepath = export_service.export_conversations_pdf(full_payload, filename=filename)
        else:
            raise HTTPException(status_code=400, detail="Format non supporté. Utilisez 'json', 'csv' ou 'pdf'")

        return {
            "message": f"Export {format} créé avec succès",
            "filepath": filepath,
            "filename": os.path.basename(filepath),
            "conversations_count": len(conversations),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/download/{filename}")
async def download_export(filename: str):
    """Télécharge un fichier d'export."""
    global export_service
    try:
        export_info = export_service.get_export_info(filename)
        if not export_info:
            raise HTTPException(status_code=404, detail="Fichier d'export non trouvé")
        
        from fastapi.responses import FileResponse
        return FileResponse(
            export_info["path"],
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/export/{filename}")
async def delete_export(filename: str):
    """Supprime un fichier d'export."""
    global export_service
    try:
        success = export_service.delete_export(filename)
        if not success:
            raise HTTPException(status_code=404, detail="Fichier d'export non trouvé")
        
        return {"message": f"Fichier {filename} supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- DB-backed endpoints ----------------

class StudentCreate(BaseModel):
    name: str
    email: str
    role: Optional[str] = "student"

class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    class Config:
        orm_mode = True

@app.post("/api/students", response_model=StudentOut)
async def create_student_endpoint(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = crud.get_student_by_email(db, payload.email)
    if existing:
        return existing
    student = crud.create_student(db, name=payload.name, email=payload.email, role=payload.role or "student")
    return student

@app.get("/api/students/{student_id}", response_model=StudentOut)
async def get_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    return student

class ConversationCreate(BaseModel):
    student_id: int
    title: Optional[str] = "Conversation"

class ConversationOut(BaseModel):
    id: int
    student_id: int
    title: str
    class Config:
        orm_mode = True

@app.post("/api/conversations", response_model=ConversationOut)
async def create_conversation_endpoint(payload: ConversationCreate, db: Session = Depends(get_db)):
    # Ensure student exists
    student = crud.get_student(db, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    conv = crud.create_conversation(db, student_id=payload.student_id, title=payload.title or "Conversation")
    return conv

@app.get("/api/students/{student_id}/conversations", response_model=List[ConversationOut])
async def list_student_conversations(student_id: int, db: Session = Depends(get_db)):
    # Ensure student exists
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    return crud.get_student_conversations(db, student_id)

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str
    confidence: Optional[str] = None
    response_time: Optional[str] = None

class MessageOut(BaseModel):
    id: int
    conversation_id: int
    sender: str
    content: str
    confidence: Optional[str]
    response_time: Optional[str]
    class Config:
        orm_mode = True

@app.post("/api/messages", response_model=MessageOut)
async def add_message_endpoint(payload: MessageCreate, db: Session = Depends(get_db)):
    # Ensure conversation exists
    conv = db.query(Conversation).filter(Conversation.id == payload.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    msg = crud.add_message(
        db,
        conversation_id=payload.conversation_id,
        sender=payload.sender,
        content=payload.content,
        confidence=payload.confidence,
        response_time=payload.response_time,
    )
    return msg

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[MessageOut])
async def list_messages_endpoint(conversation_id: int, db: Session = Depends(get_db)):
    # Ensure conversation exists
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    return crud.get_conversation_messages(db, conversation_id)

# ---------------- Conversation Utilities ----------------

class ConversationTitleUpdate(BaseModel):
    title: str

@app.put("/api/conversations/{conversation_id}/title", response_model=ConversationOut)
async def update_conversation_title(conversation_id: int, payload: ConversationTitleUpdate, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    conv.title = payload.title or conv.title
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

class ConversationDuplicateRequest(BaseModel):
    new_title: str

@app.post("/api/conversations/{conversation_id}/duplicate", response_model=ConversationOut)
async def duplicate_conversation(conversation_id: int, payload: ConversationDuplicateRequest, db: Session = Depends(get_db)):
    # Source conversation
    src = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not src:
        raise HTTPException(status_code=404, detail="Conversation introuvable")
    # Create new conversation
    new_conv = crud.create_conversation(db, student_id=src.student_id, title=payload.new_title or f"Copie de {src.title}")
    # Copy messages
    messages = crud.get_conversation_messages(db, conversation_id)
    for m in messages:
        crud.add_message(
            db,
            conversation_id=new_conv.id,
            sender=m.sender,
            content=m.content,
            confidence=m.confidence,
            response_time=m.response_time,
        )
    return new_conv

# ---------------- Students CRUD (Admin) ----------------

from sqlalchemy.orm import Session
from src.db import get_db
from src import crud

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

@app.get("/api/students", response_model=List[StudentOut])
async def list_students_endpoint(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.created_at.desc()).all()
    return students

@app.put("/api/students/{student_id}", response_model=StudentOut)
async def update_student_endpoint(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    if payload.name is not None:
        student.name = payload.name
    if payload.email is not None:
        student.email = payload.email
    if payload.role is not None:
        student.role = payload.role
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.delete("/api/students/{student_id}")
async def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant introuvable")
    db.delete(student)
    db.commit()
    return {"message": "Étudiant supprimé avec succès"}

# ---------------- Admin Documents Management ----------------

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

@app.get("/api/admin/documents")
async def list_documents():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        files = []
        for f in DATA_DIR.iterdir():
            if f.is_file():
                stat = f.stat()
                files.append({
                    "filename": f.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                })
        files.sort(key=lambda x: x["filename"].lower())
        return {"documents": files, "total": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        target = DATA_DIR / file.filename
        content = await file.read()
        with open(target, "wb") as out:
            out.write(content)
        # Reload vector store
        await load_documents()
        return {"message": "Document téléversé et index rechargé", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/documents/{filename}")
async def delete_document(filename: str):
    try:
        target = DATA_DIR / filename
        if not target.exists() or not target.is_file():
            raise HTTPException(status_code=404, detail="Fichier introuvable")
        target.unlink()
        # Reload vector store
        await load_documents()
        return {"message": "Document supprimé et index rechargé", "filename": filename}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Student Dashboard Data ----------------

class SubjectOut(BaseModel):
    id: str
    name: str
    code: str
    description: str
    documents_count: int
    questions_count: int
    color: str

class StudentUsageStats(BaseModel):
    total_questions: int
    total_conversations: int
    total_documents: int
    last_activity: str
    favorite_subjects: List[str]

@app.get("/api/student/subjects", response_model=List[SubjectOut])
async def get_student_subjects(db: Session = Depends(get_db)):
    """Get all subjects with their statistics."""
    try:
        # Get document stats to determine subjects
        stats = await get_stats()
        
        # Create subjects based on available documents and metrics
        subjects = []
        if stats and stats.subjects:
            colors = ['rose', 'blue', 'green', 'purple', 'emerald', 'amber', 'red', 'yellow', 'indigo', 'pink']
            for i, subject in enumerate(stats.subjects):
                # Get questions count for this subject
                questions_count = db.query(Message).join(Conversation).filter(
                    Message.sender == "assistant",
                    Conversation.title.contains(subject)
                ).count()
                
                subjects.append(SubjectOut(
                    id=str(i + 1),
                    name=subject,
                    code=f"{subject[:3].upper()}101",
                    description=f"Cours et exercices de {subject}",
                    documents_count=stats.total_documents // len(stats.subjects) if stats.subjects else 0,
                    questions_count=questions_count,
                    color=colors[i % len(colors)]
                ))
        else:
            # Default subjects if no documents loaded
            default_subjects = [
                {"name": "Mathématiques", "code": "MATH101", "description": "Calcul différentiel et intégral, Algèbre linéaire"},
                {"name": "Physique", "code": "PHYS101", "description": "Mécanique classique, Électromagnétisme"},
                {"name": "Informatique", "code": "INFO101", "description": "Algorithmes, Structures de données, Programmation"},
                {"name": "Chimie", "code": "CHIM101", "description": "Chimie générale, Thermodynamique"},
                {"name": "Biologie", "code": "BIO101", "description": "Biologie cellulaire, Génétique"},
                {"name": "Économie", "code": "ECO101", "description": "Microéconomie, Macroéconomie"}
            ]
            colors = ['rose', 'blue', 'green', 'purple', 'emerald', 'amber']
            
            for i, subject in enumerate(default_subjects):
                subjects.append(SubjectOut(
                    id=str(i + 1),
                    name=subject["name"],
                    code=subject["code"],
                    description=subject["description"],
                    documents_count=0,
                    questions_count=0,
                    color=colors[i]
                ))
        
        return subjects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/usage-stats", response_model=StudentUsageStats)
async def get_student_usage_stats(student_id: int, db: Session = Depends(get_db)):
    """Get usage statistics for a specific student."""
    try:
        # Get student's conversations
        conversations = db.query(Conversation).filter(Conversation.student_id == student_id).all()
        
        # Count total questions (user messages)
        total_questions = db.query(Message).join(Conversation).filter(
            Conversation.student_id == student_id,
            Message.sender == "user"
        ).count()
        
        # Count total conversations
        total_conversations = len(conversations)
        
        # Count total documents (from localStorage for now, could be stored in DB)
        total_documents = 0  # This would need to be tracked in the database
        
        # Get last activity
        last_activity = "Aujourd'hui"
        if conversations:
            latest_conv = max(conversations, key=lambda c: c.created_at)
            last_activity = latest_conv.created_at.strftime("%d/%m/%Y")
        
        # Get favorite subjects (most discussed topics)
        favorite_subjects = []
        if conversations:
            # Simple implementation - could be enhanced with topic analysis
            favorite_subjects = ["Mathématiques", "Physique", "Informatique"]
        
        return StudentUsageStats(
            total_questions=total_questions,
            total_conversations=total_conversations,
            total_documents=total_documents,
            last_activity=last_activity,
            favorite_subjects=favorite_subjects
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Document Management ----------------

class DocumentOut(BaseModel):
    id: str
    name: str
    type: str
    size: str
    uploaded_at: str
    status: str
    source: str
    subject: Optional[str] = None

@app.get("/api/documents", response_model=List[DocumentOut])
async def get_all_documents():
    """Get all available documents (admin + student documents)."""
    try:
        documents = []
        
        # Get admin documents from data directory
        if DATA_DIR.exists():
            for file_path in DATA_DIR.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.docx', '.txt']:
                    stat = file_path.stat()
                    documents.append(DocumentOut(
                        id=f"admin-{file_path.name}",
                        name=file_path.name,
                        type=file_path.suffix.upper().replace('.', ''),
                        size=f"{stat.st_size / 1024 / 1024:.1f} MB",
                        uploaded_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        status="active",
                        source="admin",
                        subject="Cours"
                    ))
        
        # Get document stats to add virtual documents if needed
        stats = await get_stats()
        if stats and stats.subjects:
            for i, subject in enumerate(stats.subjects):
                documents.append(DocumentOut(
                    id=f"virtual-{i}",
                    name=f"Document de cours - {subject}",
                    type="PDF",
                    size="2.5 MB",
                    uploaded_at=datetime.now().isoformat(),
                    status="active",
                    source="system",
                    subject=subject
                ))
        
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/documents", response_model=List[DocumentOut])
async def get_student_documents(student_id: int):
    """Get student's personal documents."""
    try:
        # For now, return empty list as student documents are stored in localStorage
        # In a real implementation, this would query a documents table
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Admin Settings ----------------

class SystemSettings(BaseModel):
    openai_key: Optional[str] = None
    use_openai: bool = False
    top_k: int = 5
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200

@app.get("/api/admin/settings", response_model=SystemSettings)
async def get_system_settings():
    """Get current system settings."""
    try:
        # In a real implementation, this would be stored in database
        # For now, return default settings
        return SystemSettings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/settings", response_model=SystemSettings)
async def update_system_settings(settings: SystemSettings):
    """Update system settings."""
    try:
        # In a real implementation, this would update database and reload system
        # For now, just return the settings
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
