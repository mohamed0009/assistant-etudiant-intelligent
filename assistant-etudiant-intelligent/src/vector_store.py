"""
Module de gestion de la base vectorielle pour l'assistant étudiant intelligent.
Utilise FAISS pour stocker et rechercher les embeddings des documents.
"""

import os
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path

import faiss
import numpy as np
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStore:
    """Classe pour gérer la base vectorielle des documents."""
    
    def __init__(self, embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialise la base vectorielle.
        
        Args:
            embeddings_model: Modèle d'embeddings à utiliser
        """
        self.embeddings_model = embeddings_model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embeddings_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
        self.index_path = "vector_store"
        
    def create_vector_store(self, documents: List[Document]) -> bool:
        """
        Crée la base vectorielle à partir des documents.
        
        Args:
            documents: Liste des documents à vectoriser
            
        Returns:
            True si la création a réussi, False sinon
        """
        if not documents:
            print("⚠️  Aucun document à vectoriser")
            return False
        
        try:
            print(f"🔧 Création de la base vectorielle avec {len(documents)} documents...")
            print(f"📊 Utilisation du modèle: {self.embeddings_model}")
            
            # Créer la base vectorielle FAISS
            self.vector_store = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            
            print(f"✅ Base vectorielle créée avec succès!")
            print(f"📈 Dimensions: {self.vector_store.index.ntotal} vecteurs")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la base vectorielle: {e}")
            return False
    
    def save_vector_store(self) -> bool:
        """
        Sauvegarde la base vectorielle sur disque.
        
        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        if self.vector_store is None:
            print("⚠️  Aucune base vectorielle à sauvegarder")
            return False
        
        try:
            print(f"💾 Sauvegarde de la base vectorielle...")
            self.vector_store.save_local(self.index_path)
            print(f"✅ Base vectorielle sauvegardée dans {self.index_path}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """
        Charge la base vectorielle depuis le disque.
        
        Returns:
            True si le chargement a réussi, False sinon
        """
        if not os.path.exists(self.index_path):
            print(f"⚠️  Base vectorielle non trouvée dans {self.index_path}")
            return False
        
        try:
            print(f"📂 Chargement de la base vectorielle...")
            self.vector_store = FAISS.load_local(
                folder_path=self.index_path,
                embeddings=self.embeddings
            )
            print(f"✅ Base vectorielle chargée ({self.vector_store.index.ntotal} vecteurs)")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def search_similar(self, query: str, k: int = 5, filter_dict: Optional[Dict] = None) -> List[Document]:
        """
        Recherche les documents les plus similaires à une requête.
        
        Args:
            query: Requête de recherche
            k: Nombre de résultats à retourner
            filter_dict: Filtres à appliquer (ex: {"subject": "Électricité"})
            
        Returns:
            Liste des documents les plus pertinents
        """
        if self.vector_store is None:
            print("⚠️  Base vectorielle non initialisée")
            return []
        
        try:
            # Recherche avec filtres optionnels
            if filter_dict:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter_dict
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k
                )
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche: {e}")
            return []
    
    def search_with_scores(self, query: str, k: int = 5) -> List[tuple]:
        """
        Recherche avec scores de similarité.
        
        Args:
            query: Requête de recherche
            k: Nombre de résultats à retourner
            
        Returns:
            Liste de tuples (document, score)
        """
        if self.vector_store is None:
            print("⚠️  Base vectorielle non initialisée")
            return []
        
        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k
            )
            return results
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche avec scores: {e}")
            return []
    
    def get_vector_store_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur la base vectorielle.
        
        Returns:
            Dictionnaire contenant les informations
        """
        if self.vector_store is None:
            return {
                "status": "Non initialisée",
                "total_vectors": 0,
                "dimensions": 0,
                "model": self.embeddings_model
            }
        
        return {
            "status": "Initialisée",
            "total_vectors": self.vector_store.index.ntotal,
            "dimensions": self.vector_store.index.d,
            "model": self.embeddings_model,
            "index_type": type(self.vector_store.index).__name__
        }
    
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Ajoute de nouveaux documents à la base vectorielle existante.
        
        Args:
            documents: Nouveaux documents à ajouter
            
        Returns:
            True si l'ajout a réussi, False sinon
        """
        if self.vector_store is None:
            print("⚠️  Base vectorielle non initialisée")
            return False
        
        if not documents:
            print("⚠️  Aucun document à ajouter")
            return False
        
        try:
            print(f"➕ Ajout de {len(documents)} nouveaux documents...")
            self.vector_store.add_documents(documents)
            print(f"✅ Documents ajoutés avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout des documents: {e}")
            return False
    
    def delete_vector_store(self) -> bool:
        """
        Supprime la base vectorielle du disque.
        
        Returns:
            True si la suppression a réussi, False sinon
        """
        try:
            if os.path.exists(self.index_path):
                import shutil
                shutil.rmtree(self.index_path)
                print(f"🗑️  Base vectorielle supprimée: {self.index_path}")
            
            self.vector_store = None
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            return False
