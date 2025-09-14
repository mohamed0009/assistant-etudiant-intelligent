"""
Module de chargement des documents pour l'assistant étudiant intelligent.
Gère le chargement des fichiers PDF et Word.
"""

import os
from typing import List, Dict, Any
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class DocumentLoader:
    """Classe pour charger et traiter les documents d'étude."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialise le chargeur de documents.
        
        Args:
            data_dir: Répertoire contenant les documents
        """
        self.data_dir = Path(data_dir)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_documents(self) -> List[Document]:
        """
        Charge tous les documents du répertoire data.
        
        Returns:
            Liste des documents chargés et segmentés
        """
        documents = []
        
        if not self.data_dir.exists():
            print(f"⚠️  Le répertoire {self.data_dir} n'existe pas.")
            print("📁 Créez le répertoire et ajoutez vos documents PDF/Word.")
            return documents
        
        # Charger les fichiers PDF
        pdf_files = list(self.data_dir.glob("*.pdf"))
        for pdf_file in pdf_files:
            try:
                print(f"📄 Chargement de {pdf_file.name}...")
                loader = PyPDFLoader(str(pdf_file))
                pdf_docs = loader.load()
                
                # Ajouter des métadonnées
                for doc in pdf_docs:
                    doc.metadata.update({
                        "source": pdf_file.name,
                        "file_type": "pdf",
                        "subject": self._extract_subject_from_filename(pdf_file.name)
                    })
                
                documents.extend(pdf_docs)
                print(f"✅ {pdf_file.name} chargé ({len(pdf_docs)} pages)")
                
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {pdf_file.name}: {e}")
        
        # Charger les fichiers Word
        docx_files = list(self.data_dir.glob("*.docx")) + list(self.data_dir.glob("*.doc"))
        for docx_file in docx_files:
            try:
                print(f"📄 Chargement de {docx_file.name}...")
                loader = Docx2txtLoader(str(docx_file))
                docx_docs = loader.load()
                
                # Ajouter des métadonnées
                for doc in docx_docs:
                    doc.metadata.update({
                        "source": docx_file.name,
                        "file_type": "word",
                        "subject": self._extract_subject_from_filename(docx_file.name)
                    })
                
                documents.extend(docx_docs)
                print(f"✅ {docx_file.name} chargé")
                
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {docx_file.name}: {e}")
        
        # Charger les fichiers texte
        txt_files = list(self.data_dir.glob("*.txt"))
        for txt_file in txt_files:
            try:
                print(f"📄 Chargement de {txt_file.name}...")
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Créer un document LangChain
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": txt_file.name,
                        "file_type": "text",
                        "subject": self._extract_subject_from_filename(txt_file.name)
                    }
                )
                
                documents.append(doc)
                print(f"✅ {txt_file.name} chargé")
                
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {txt_file.name}: {e}")
        
        if not documents:
            print("⚠️  Aucun document trouvé dans le répertoire data/")
            print("📋 Ajoutez vos cours, TD et examens corrigés au format PDF, Word ou texte")
        
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Segmente les documents en chunks plus petits.
        
        Args:
            documents: Liste des documents à segmenter
            
        Returns:
            Liste des chunks de documents
        """
        if not documents:
            return []
        
        print(f"✂️  Segmentation de {len(documents)} documents...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"✅ {len(chunks)} chunks créés")
        
        return chunks
    
    def _extract_subject_from_filename(self, filename: str) -> str:
        """
        Extrait le sujet/matière du nom de fichier.
        
        Args:
            filename: Nom du fichier
            
        Returns:
            Sujet extrait ou "Général"
        """
        filename_lower = filename.lower()
        
        # Mapping des mots-clés vers les matières
        subject_keywords = {
            "électricité": "Électricité",
            "electronique": "Électronique",
            "electronique": "Électronique",
            "physique": "Physique",
            "math": "Mathématiques",
            "mathematiques": "Mathématiques",
            "cours": "Cours",
            "td": "Travaux Dirigés",
            "tp": "Travaux Pratiques",
            "examen": "Examen",
            "corrige": "Corrigé",
            "correction": "Corrigé"
        }
        
        for keyword, subject in subject_keywords.items():
            if keyword in filename_lower:
                return subject
        
        return "Général"
    
    def get_document_stats(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Génère des statistiques sur les documents chargés.
        
        Args:
            documents: Liste des documents
            
        Returns:
            Dictionnaire contenant les statistiques
        """
        if not documents:
            return {"total_documents": 0, "subjects": {}, "file_types": {}}
        
        subjects = {}
        file_types = {}
        total_chars = 0
        
        for doc in documents:
            # Compter par sujet
            subject = doc.metadata.get("subject", "Général")
            subjects[subject] = subjects.get(subject, 0) + 1
            
            # Compter par type de fichier
            file_type = doc.metadata.get("file_type", "inconnu")
            file_types[file_type] = file_types.get(file_type, 0) + 1
            
            # Compter les caractères
            total_chars += len(doc.page_content)
        
        return {
            "total_documents": len(documents),
            "subjects": subjects,
            "file_types": file_types,
            "total_characters": total_chars,
            "average_chars_per_doc": total_chars // len(documents) if documents else 0
        }
