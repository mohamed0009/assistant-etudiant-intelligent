"""
Metrics service for tracking and analyzing system performance.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import logging
from sqlalchemy.orm import Session

from src.crud import CRUDOperations

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(self, db_session: Session, metrics_file: str = "data/metrics.json"):
        self.crud = CRUDOperations(db_session)
        self.metrics_file = Path(metrics_file)
        self.ensure_metrics_file()
        
    def ensure_metrics_file(self):
        """Ensure metrics file exists with proper structure."""
        if not self.metrics_file.exists():
            self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
            self.save_metrics({
                "questions": [],
                "response_times": [],
                "confidence_scores": [],
                "subject_distribution": {},
                "daily_usage": {}
            })
            
    def load_metrics(self) -> Dict:
        """Load metrics from file."""
        try:
            with open(self.metrics_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading metrics: {e}")
            return {}
            
    def save_metrics(self, metrics: Dict):
        """Save metrics to file."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
            
    def record_question(
        self,
        question: str,
        response_time: float,
        confidence: float,
        subject: str,
        user_id: str,
        sources_used: int,
        question_type: str = "general",
        metadata: Dict = None
    ):
        """Record a new question interaction."""
        # Save to database
        self.crud.create_question_metrics(
            question=question,
            response_time=response_time,
            confidence=confidence,
            question_type=question_type,
            subject=subject,
            user_id=user_id,
            sources_used=sources_used,
            metadata=metadata
        )
        
        # Update metrics file
        metrics = self.load_metrics()
        today = datetime.now().strftime("%Y-%m-%d")
        
        metrics["questions"].append({
            "text": question,
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time,
            "confidence": confidence,
            "subject": subject,
            "user_id": user_id
        })
        
        metrics["response_times"].append(response_time)
        metrics["confidence_scores"].append(confidence)
        
        # Update subject distribution
        metrics["subject_distribution"][subject] = metrics["subject_distribution"].get(subject, 0) + 1
        
        # Update daily usage
        metrics["daily_usage"][today] = metrics["daily_usage"].get(today, 0) + 1
        
        self.save_metrics(metrics)
        
    def get_performance_stats(self) -> Dict:
        """Get system performance statistics."""
        return self.crud.get_performance_metrics()
        
    def get_usage_trends(self) -> Dict:
        """Get usage trends over time."""
        metrics = self.load_metrics()
        return {
            "daily_usage": metrics.get("daily_usage", {}),
            "subject_distribution": metrics.get("subject_distribution", {}),
            "total_questions": len(metrics.get("questions", [])),
            "average_response_time": sum(metrics.get("response_times", [])) / len(metrics.get("response_times", [1])),
            "average_confidence": sum(metrics.get("confidence_scores", [])) / len(metrics.get("confidence_scores", [1]))
        }