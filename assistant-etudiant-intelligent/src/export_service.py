"""
Service d'export et de sauvegarde des données
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import zipfile

from .models import ExportData, QuestionMetrics, PerformanceMetrics

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class ExportService:
    def __init__(self, data_dir: str = "data", exports_dir: str = "exports"):
        self.data_dir = data_dir
        self.exports_dir = exports_dir
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Crée les répertoires nécessaires."""
        os.makedirs(self.exports_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def export_conversations_json(self, conversations: List[Dict], filename: Optional[str] = None) -> str:
        """Exporte les conversations en format JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversations_{timestamp}.json"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "format": "json",
            "conversations": conversations,
            "total_conversations": len(conversations)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        return filepath
    
    def export_conversations_csv(self, conversations: List[Dict], filename: Optional[str] = None) -> str:
        """Exporte les conversations en format CSV."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversations_{timestamp}.csv"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        if not conversations:
            # Créer un fichier CSV vide avec les en-têtes
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'question', 'answer', 'confidence', 'response_time', 'sources_count'])
            return filepath
        
        # Extraire les clés de la première conversation pour les en-têtes
        headers = list(conversations[0].keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(conversations)
        
        return filepath
    
    def export_conversations_pdf(self, conversations: List[Dict], filename: Optional[str] = None) -> str:
        """Exporte les conversations en format PDF."""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab n'est pas installé. Installez-le avec: pip install reportlab")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversations_{timestamp}.pdf"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        # Créer le document PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        # Titre principal
        story.append(Paragraph("Export des Conversations", title_style))
        story.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", normal_style))
        story.append(Spacer(1, 20))
        
        if not conversations:
            story.append(Paragraph("Aucune conversation trouvée.", normal_style))
        else:
            # Statistiques
            story.append(Paragraph("Statistiques", heading_style))
            stats_data = [
                ['Total des conversations', str(len(conversations))],
                ['Date d\'export', datetime.now().strftime('%d/%m/%Y %H:%M')]
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # Conversations
            for i, conv in enumerate(conversations, 1):
                story.append(Paragraph(f"Conversation {i}", heading_style))
                
                # Informations de la conversation
                if 'conversation_id' in conv:
                    story.append(Paragraph(f"<b>ID:</b> {conv['conversation_id']}", normal_style))
                if 'title' in conv:
                    story.append(Paragraph(f"<b>Titre:</b> {conv['title']}", normal_style))
                if 'created_at' in conv:
                    story.append(Paragraph(f"<b>Créée le:</b> {conv['created_at']}", normal_style))
                
                story.append(Spacer(1, 10))
                
                # Messages
                if 'messages' in conv and conv['messages']:
                    story.append(Paragraph("Messages:", normal_style))
                    
                    for msg in conv['messages']:
                        sender = msg.get('sender', 'Inconnu')
                        content = msg.get('content', '')
                        created_at = msg.get('created_at', '')
                        
                        # Style selon l'expéditeur
                        if sender == 'user':
                            msg_style = ParagraphStyle(
                                'UserMessage',
                                parent=normal_style,
                                leftIndent=20,
                                backgroundColor=colors.lightblue,
                                borderColor=colors.blue,
                                borderWidth=1,
                                borderPadding=5
                            )
                            sender_text = "Vous"
                        else:
                            msg_style = ParagraphStyle(
                                'AssistantMessage',
                                parent=normal_style,
                                leftIndent=20,
                                backgroundColor=colors.lightgrey,
                                borderColor=colors.grey,
                                borderWidth=1,
                                borderPadding=5
                            )
                            sender_text = "Assistant IA"
                        
                        story.append(Paragraph(f"<b>{sender_text}</b> ({created_at})", normal_style))
                        story.append(Paragraph(content, msg_style))
                        story.append(Spacer(1, 5))
                else:
                    story.append(Paragraph("Aucun message dans cette conversation.", normal_style))
                
                story.append(Spacer(1, 15))
        
        # Construire le PDF
        doc.build(story)
        return filepath
    
    def export_metrics_json(self, metrics: PerformanceMetrics, filename: Optional[str] = None) -> str:
        """Exporte les métriques en format JSON."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "format": "json",
            "metrics": metrics.dict()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        return filepath
    
    def export_metrics_csv(self, metrics: PerformanceMetrics, filename: Optional[str] = None) -> str:
        """Exporte les métriques en format CSV."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.csv"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        # Convertir les métriques en format tabulaire
        metrics_data = []
        metrics_dict = metrics.dict()
        
        # Métriques de base
        for key, value in metrics_dict.items():
            if isinstance(value, (int, float, str)):
                metrics_data.append({
                    'metric': key,
                    'value': value,
                    'type': 'basic'
                })
        
        # Sujets les plus demandés
        for subject, count in metrics_dict.get('most_asked_subjects', {}).items():
            metrics_data.append({
                'metric': f'subject_{subject}',
                'value': count,
                'type': 'subject'
            })
        
        # Usage des documents
        for doc, count in metrics_dict.get('documents_usage', {}).items():
            metrics_data.append({
                'metric': f'document_{doc}',
                'value': count,
                'type': 'document'
            })
        
        # Types de réponses
        for response_type, count in metrics_dict.get('precomputed_vs_documents', {}).items():
            metrics_data.append({
                'metric': f'response_type_{response_type}',
                'value': count,
                'type': 'response_type'
            })
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if metrics_data:
                writer = csv.DictWriter(f, fieldnames=['metric', 'value', 'type'])
                writer.writeheader()
                writer.writerows(metrics_data)
            else:
                writer = csv.writer(f)
                writer.writerow(['metric', 'value', 'type'])
        
        return filepath
    
    def create_full_backup(self, include_data: bool = True, include_metrics: bool = True) -> str:
        """Crée une sauvegarde complète du système."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"full_backup_{timestamp}"
        backup_path = os.path.join(self.exports_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        # Sauvegarder les documents
        if include_data and os.path.exists(self.data_dir):
            import shutil
            shutil.copytree(self.data_dir, os.path.join(backup_path, "data"))
        
        # Sauvegarder les métriques
        if include_metrics:
            metrics_file = os.path.join(self.data_dir, "metrics.json")
            if os.path.exists(metrics_file):
                shutil.copy2(metrics_file, os.path.join(backup_path, "metrics.json"))
            
            sessions_file = os.path.join(self.data_dir, "sessions.json")
            if os.path.exists(sessions_file):
                shutil.copy2(sessions_file, os.path.join(backup_path, "sessions.json"))
        
        # Créer un fichier de métadonnées
        metadata = {
            "backup_date": datetime.now().isoformat(),
            "backup_type": "full",
            "includes_data": include_data,
            "includes_metrics": include_metrics,
            "version": "1.0"
        }
        
        with open(os.path.join(backup_path, "metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # Créer une archive ZIP
        zip_path = f"{backup_path}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arcname)
        
        # Supprimer le dossier temporaire
        import shutil
        shutil.rmtree(backup_path)
        
        return zip_path
    
    def list_exports(self) -> List[Dict[str, Any]]:
        """Liste tous les fichiers d'export disponibles."""
        exports = []
        
        if not os.path.exists(self.exports_dir):
            return exports
        
        for filename in os.listdir(self.exports_dir):
            filepath = os.path.join(self.exports_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                exports.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": self._get_file_type(filename)
                })
        
        # Trier par date de modification (plus récent en premier)
        exports.sort(key=lambda x: x['modified'], reverse=True)
        return exports
    
    def _get_file_type(self, filename: str) -> str:
        """Détermine le type de fichier d'export."""
        if filename.endswith('.json'):
            return 'json'
        elif filename.endswith('.csv'):
            return 'csv'
        elif filename.endswith('.pdf'):
            return 'pdf'
        elif filename.endswith('.zip'):
            return 'backup'
        else:
            return 'unknown'
    
    def delete_export(self, filename: str) -> bool:
        """Supprime un fichier d'export."""
        filepath = os.path.join(self.exports_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def get_export_info(self, filename: str) -> Optional[Dict[str, Any]]:
        """Récupère les informations d'un fichier d'export."""
        filepath = os.path.join(self.exports_dir, filename)
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        return {
            "filename": filename,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "type": self._get_file_type(filename),
            "path": filepath
        }

