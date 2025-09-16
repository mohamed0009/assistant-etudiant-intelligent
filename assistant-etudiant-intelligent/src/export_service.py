"""
Export service for conversation and metrics data.
"""

import json
import csv
from typing import List, Dict
from pathlib import Path
import logging
from datetime import datetime
from sqlalchemy.orm import Session
import pandas as pd

from src.crud import CRUDOperations

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self, db_session: Session, export_dir: str = "exports"):
        self.crud = CRUDOperations(db_session)
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        
    def export_student_conversations(
        self,
        student_id: int,
        format: str = "json"
    ) -> str:
        """Export all conversations for a student in specified format."""
        conversations = self.crud.list_student_conversations(student_id)
        
        if not conversations:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"student_{student_id}_conversations"
        
        data = []
        for conv in conversations:
            messages = self.crud.get_conversation_messages(conv.id)
            conv_data = {
                "conversation_id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "messages": [
                    {
                        "sender": msg.sender,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat(),
                        "confidence": msg.confidence,
                        "response_time": msg.response_time,
                        "metadata": msg.message_metadata if msg.message_metadata else None
                    }
                    for msg in messages
                ]
            }
            data.append(conv_data)
            
        if format == "json":
            output_file = self.export_dir / f"{filename}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        elif format == "csv":
            output_file = self.export_dir / f"{filename}.csv"
            flattened_data = []
            for conv in data:
                for msg in conv["messages"]:
                    flattened_data.append({
                        "conversation_id": conv["conversation_id"],
                        "conversation_title": conv["title"],
                        "conversation_created": conv["created_at"],
                        "message_sender": msg["sender"],
                        "message_content": msg["content"],
                        "message_created": msg["created_at"],
                        "confidence": msg["confidence"],
                        "response_time": msg["response_time"]
                    })
                    
            df = pd.DataFrame(flattened_data)
            df.to_csv(output_file, index=False)
            
        elif format == "pdf":
            output_file = self.export_dir / f"{filename}.pdf"
            df = pd.DataFrame(data)
            df.to_pdf(output_file)
            
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
        return str(output_file)
        
    def export_metrics(self, format: str = "json") -> str:
        """Export system metrics in specified format."""
        metrics = self.crud.get_performance_metrics()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_metrics_{timestamp}"
        
        if format == "json":
            output_file = self.export_dir / f"{filename}.json"
            with open(output_file, 'w') as f:
                metrics_dict = {
                    "average_response_time": metrics["average_response_time"],
                    "average_confidence": metrics["average_confidence"],
                    "total_questions": metrics["total_questions"],
                    "questions_by_subject": {k: v for k, v in metrics["questions_by_subject"]}
                }
                json.dump(metrics_dict, f, indent=2)
                
        elif format == "csv":
            output_file = self.export_dir / f"{filename}.csv"
            
            # Flatten nested metrics for CSV format
            flattened_metrics = {
                "average_response_time": metrics["average_response_time"],
                "average_confidence": metrics["average_confidence"],
                "total_questions": metrics["total_questions"]
            }
            
            for subject, count in metrics["questions_by_subject"]:
                flattened_metrics[f"subject_{subject}"] = count
                
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=flattened_metrics.keys())
                writer.writeheader()
                writer.writerow(flattened_metrics)
                
        else:
            raise ValueError(f"Unsupported export format: {format}")
            
        return str(output_file)