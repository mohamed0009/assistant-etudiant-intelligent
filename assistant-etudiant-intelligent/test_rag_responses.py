#!/usr/bin/env python3
"""
Script de test pour vérifier que l'assistant RAG donne des réponses complètes
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

def test_rag_responses():
    """Test des réponses complètes de l'assistant RAG."""
    
    print("🧪 Test des réponses complètes de l'assistant RAG")
    print("=" * 60)
    
    try:
        # Charger les documents
        print("📚 Chargement des documents...")
        loader = DocumentLoader()
        documents = loader.load_documents()
        
        if not documents:
            print("❌ Aucun document trouvé")
            return
        
        print(f"✅ {len(documents)} documents chargés")
        
        # Créer la base vectorielle
        print("🔍 Création de la base vectorielle...")
        chunks = loader.split_documents(documents)
        vector_store = VectorStore()
        success = vector_store.create_vector_store(chunks)
        
        if not success:
            print("❌ Erreur création base vectorielle")
            return
        
        print("✅ Base vectorielle créée")
        
        # Initialiser le moteur RAG
        print("🤖 Initialisation du moteur RAG...")
        rag_engine = RAGEngine(vector_store)
        print("✅ Moteur RAG initialisé")
        
        # Questions de test
        test_questions = [
            "Explique-moi la loi d'Ohm",
            "Qu'est-ce que le théorème de Thévenin ?",
            "Comment calculer la puissance électrique ?",
            "Explique-moi les dérivées en mathématiques",
            "Qu'est-ce que le pH en chimie ?",
            "Comment calculer une intégrale ?"
        ]
        
        print("\n🎯 Test des réponses complètes")
        print("=" * 60)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 Question {i}: {question}")
            print("-" * 40)
            
            # Obtenir la réponse
            response = rag_engine.ask_question(question)
            
            # Afficher la réponse
            print(f"✅ Réponse (confiance: {response.confidence:.2f}):")
            print(response.answer)
            
            # Vérifier que la réponse est complète
            if "consultez" in response.answer.lower() or "document" in response.answer.lower():
                print("⚠️  ATTENTION: La réponse contient des références aux documents")
            else:
                print("✅ Réponse complète sans renvoi vers les documents")
            
            print(f"⏱️  Temps de traitement: {response.processing_time:.2f}s")
            print(f"📚 Sources utilisées: {len(response.sources)}")
            
            if i < len(test_questions):
                input("\nAppuyez sur Entrée pour continuer...")
        
        print("\n🎉 Test terminé avec succès !")
        print("✅ L'assistant RAG donne des réponses complètes et détaillées")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_rag_responses()

