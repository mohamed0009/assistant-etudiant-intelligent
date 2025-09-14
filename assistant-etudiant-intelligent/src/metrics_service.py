"""
Service de collecte et analyse des métriques de performance
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict, Counter
import os

from .models import (
    QuestionMetrics, PerformanceMetrics, UserSession,
    QuestionType, SubjectType,
)
from .crud import (
    record_question_metric,
    aggregate_performance_metrics,
    recent_question_metrics,
    get_user_sessions as crud_get_user_sessions,
    start_user_session as crud_start_user_session,
    end_user_session as crud_end_user_session,
)

class MetricsService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.metrics_file = os.path.join(data_dir, "metrics.json")
        self.sessions_file = os.path.join(data_dir, "sessions.json")
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Crée les fichiers de données s'ils n'existent pas."""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
    
    def record_question(self, question: str, response_time: float,
                       confidence: float, question_type: QuestionType,
                       subject: Optional[SubjectType], user_id: str,
                       sources_used: int = 0, db=None):
        """Enregistre une nouvelle question et ses métriques. Privilégie la DB si fournie."""
        if db is not None:
            record_question_metric(
                db,
                question=question,
                response_time=response_time,
                confidence=confidence,
                question_type=str(question_type.value if hasattr(question_type, "value") else question_type),
                subject=str(subject.value if subject is not None and hasattr(subject, "value") else subject) if subject is not None else None,
                user_id=user_id,
                sources_used=sources_used,
            )
            return
        # Fallback JSON
        metrics = QuestionMetrics(
            question=question,
            response_time=response_time,
            confidence=confidence,
            question_type=question_type,
            subject=subject,
            timestamp=datetime.now(),
            user_id=user_id,
            sources_used=sources_used,
        )
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            all_metrics = json.load(f)
        all_metrics.append(metrics.dict())
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(all_metrics, f, default=str, ensure_ascii=False, indent=2)
    
    def get_performance_metrics(self, db=None) -> PerformanceMetrics:
        """Calcule les métriques globales. Utilise la DB si dispo."""
        if db is not None:
            agg = aggregate_performance_metrics(db)
            return PerformanceMetrics(**agg)
        # Fallback JSON
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            all_metrics = json.load(f)
        if not all_metrics:
            return self._empty_metrics()
        total_questions = len(all_metrics)
        response_times = [m['response_time'] for m in all_metrics]
        confidences = [m['confidence'] for m in all_metrics]
        today = datetime.now().date()
        questions_today = sum(1 for m in all_metrics if datetime.fromisoformat(m['timestamp']).date() == today)
        subjects = [m.get('subject') for m in all_metrics if m.get('subject')]
        most_asked_subjects = dict(Counter(subjects))
        recent_response_times = response_times[-10:] if len(response_times) >= 10 else response_times
        recent_confidences = confidences[-10:] if len(confidences) >= 10 else confidences
        document_usage = defaultdict(int)
        for m in all_metrics:
            if m.get('sources_used', 0) > 0:
                document_usage['documents_accessed'] += 1
        precomputed_vs_docs = defaultdict(int)
        for m in all_metrics:
            question_type = m.get('question_type', 'unknown')
            precomputed_vs_docs[question_type] += 1
        unique_users = set(m['user_id'] for m in all_metrics)
        return PerformanceMetrics(
            total_questions=total_questions,
            average_response_time=sum(response_times) / len(response_times) if response_times else 0,
            total_users=len(unique_users),
            questions_today=questions_today,
            most_asked_subjects=most_asked_subjects,
            response_time_trend=recent_response_times,
            confidence_trend=recent_confidences,
            documents_usage=dict(document_usage),
            precomputed_vs_documents=dict(precomputed_vs_docs),
        )
    
    def _empty_metrics(self) -> PerformanceMetrics:
        """Retourne des métriques vides."""
        return PerformanceMetrics(
            total_questions=0,
            average_response_time=0,
            total_users=0,
            questions_today=0,
            most_asked_subjects={},
            response_time_trend=[],
            confidence_trend=[],
            documents_usage={},
            precomputed_vs_documents={}
        )
    
    def get_user_sessions(self, user_id: str, db=None) -> List[UserSession]:
        """Récupère les sessions d'un utilisateur. Utilise la DB si dispo."""
        if db is not None:
            rows = crud_get_user_sessions(db, user_id)
            sessions: List[UserSession] = []
            for r in rows:
                subjects = []
                if r.subjects_covered:
                    try:
                        import json as _json
                        subjects = _json.loads(r.subjects_covered)
                    except Exception:
                        subjects = []
                sessions.append(
                    UserSession(
                        user_id=r.user_id,
                        session_start=r.session_start,
                        session_end=r.session_end,
                        questions_count=r.questions_count,
                        total_time=r.total_time,
                        subjects_covered=subjects,
                    )
                )
            return sessions
        with open(self.sessions_file, 'r', encoding='utf-8') as f:
            sessions_data = json.load(f)
        user_sessions = sessions_data.get(user_id, [])
        return [UserSession(**session) for session in user_sessions]
    
    def start_user_session(self, user_id: str, db=None):
        """Démarre une nouvelle session utilisateur. Utilise la DB si dispo."""
        if db is not None:
            crud_start_user_session(db, user_id)
            return
        with open(self.sessions_file, 'r', encoding='utf-8') as f:
            sessions_data = json.load(f)
        if user_id not in sessions_data:
            sessions_data[user_id] = []
        new_session = UserSession(
            user_id=user_id,
            session_start=datetime.now(),
            session_end=None,
            questions_count=0,
            total_time=0,
            subjects_covered=[],
        )
        sessions_data[user_id].append(new_session.dict())
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions_data, f, default=str, ensure_ascii=False, indent=2)
    
    def end_user_session(self, user_id: str, db=None):
        """Termine la session active d'un utilisateur. Utilise la DB si dispo."""
        if db is not None:
            crud_end_user_session(db, user_id)
            return
        with open(self.sessions_file, 'r', encoding='utf-8') as f:
            sessions_data = json.load(f)
        if user_id in sessions_data and sessions_data[user_id]:
            for session in reversed(sessions_data[user_id]):
                if session.get('session_end') is None:
                    session['session_end'] = datetime.now().isoformat()
                    break
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(sessions_data, f, default=str, ensure_ascii=False, indent=2)
    
    def get_recent_questions(self, limit: int = 10, db=None) -> List[QuestionMetrics]:
        """Récupère les questions récentes. Utilise la DB si dispo."""
        if db is not None:
            rows = recent_question_metrics(db, limit)
            rows = list(reversed(rows))  # return chronological
            return [
                QuestionMetrics(
                    question=r.question,
                    response_time=r.response_time,
                    confidence=r.confidence,
                    question_type=r.question_type,  # already string
                    subject=r.subject,
                    timestamp=r.timestamp,
                    user_id=r.user_id,
                    sources_used=r.sources_used or 0,
                )
                for r in rows
            ]
        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            all_metrics = json.load(f)
        recent_metrics = all_metrics[-limit:] if len(all_metrics) >= limit else all_metrics
        return [QuestionMetrics(**m) for m in recent_metrics]
    
    def detect_subject(self, question: str) -> Optional[SubjectType]:
        """Détecte le sujet d'une question basé sur des mots-clés."""
        question_lower = question.lower()
        
        subject_keywords = {
            SubjectType.MATHEMATICS: ['math', 'calcul', 'dérivée', 'intégrale', 'algèbre', 'équation'],
            SubjectType.PHYSICS: ['physique', 'newton', 'force', 'énergie', 'mouvement', 'thermodynamique'],
            SubjectType.CHEMISTRY: ['chimie', 'molécule', 'atome', 'réaction', 'ph', 'acide', 'base'],
            SubjectType.ELECTRONICS: ['électronique', 'circuit', 'transistor', 'ohm', 'résistance', 'condensateur'],
            SubjectType.BIOLOGY: ['biologie', 'cellule', 'adn', 'protéine', 'mitose', 'photosynthèse'],
            SubjectType.GEOLOGY: ['géologie', 'roche', 'terre', 'séisme', 'volcan', 'tectonique'],
            SubjectType.ASTRONOMY: ['astronomie', 'étoile', 'planète', 'galaxie', 'univers', 'système solaire'],
            SubjectType.PSYCHOLOGY: ['psychologie', 'comportement', 'mémoire', 'apprentissage', 'cognition'],
            SubjectType.COMPUTER_SCIENCE: ['informatique', 'algorithme', 'programmation', 'données', 'réseau']
        }
        
        for subject, keywords in subject_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                return subject
        
        return None

