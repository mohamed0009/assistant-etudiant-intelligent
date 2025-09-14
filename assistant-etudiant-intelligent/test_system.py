"""
Script de test pour l'assistant étudiant intelligent.
Teste le chargement des documents et les réponses du RAG.
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine


def test_document_loading():
    """Teste le chargement des documents."""
    print("🧪 Test du chargement des documents...")
    
    loader = DocumentLoader()
    documents = loader.load_documents()
    
    if documents:
        print(f"✅ {len(documents)} documents chargés")
        
        # Afficher les statistiques
        stats = loader.get_document_stats(documents)
        print(f"📊 Statistiques: {stats}")
        
        return documents
    else:
        print("❌ Aucun document chargé")
        return None


def test_vector_store(documents):
    """Teste la création de la base vectorielle."""
    print("\n🧪 Test de la base vectorielle...")
    
    if not documents:
        print("❌ Aucun document à traiter")
        return None
    
    # Segmenter les documents
    loader = DocumentLoader()
    chunks = loader.split_documents(documents)
    
    # Créer la base vectorielle
    vector_store = VectorStore()
    success = vector_store.create_vector_store(chunks)
    
    if success:
        print("✅ Base vectorielle créée avec succès")
        
        # Afficher les informations
        info = vector_store.get_vector_store_info()
        print(f"📈 Informations: {info}")
        
        return vector_store
    else:
        print("❌ Erreur lors de la création de la base vectorielle")
        return None


def test_rag_engine(vector_store):
    """Teste le moteur RAG."""
    print("\n🧪 Test du moteur RAG...")
    
    if not vector_store:
        print("❌ Base vectorielle non disponible")
        return None
    
    # Créer le moteur RAG
    rag_engine = RAGEngine(vector_store)
    
    # Vérifier le statut
    status = rag_engine.get_system_status()
    print(f"🔧 Statut du système: {status}")
    
    return rag_engine


def test_questions(rag_engine):
    """Teste quelques questions."""
    print("\n🧪 Test des questions...")
    
    if not rag_engine:
        print("❌ Moteur RAG non disponible")
        return
    
    # Questions de test
    test_questions = [
        "Explique-moi la loi d'Ohm.",
        "Qu'est-ce que le théorème de Thévenin ?",
        "Quelles sont les différences entre un transformateur idéal et réel ?",
        "Comment calculer la puissance dans un circuit électrique ?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Question {i}: {question} ---")
        
        try:
            response = rag_engine.ask_question(question)
            
            print(f"🤖 Réponse: {response.answer}")
            print(f"📊 Confiance: {response.confidence:.2f}")
            print(f"⏱️  Temps: {response.processing_time:.2f}s")
            
            if response.sources:
                print(f"📚 Sources utilisées: {len(response.sources)}")
                for j, source in enumerate(response.sources[:2]):
                    source_name = source.metadata.get("source", "Inconnu")
                    print(f"   {j+1}. {source_name}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")


def main():
    """Fonction principale de test."""
    print("🎓 Test de l'Assistant Étudiant Intelligent")
    print("=" * 50)
    
    # Test 1: Chargement des documents
    documents = test_document_loading()
    
    if not documents:
        print("\n❌ Impossible de continuer sans documents")
        return
    
    # Test 2: Base vectorielle
    vector_store = test_vector_store(documents)
    
    if not vector_store:
        print("\n❌ Impossible de continuer sans base vectorielle")
        return
    
    # Test 3: Moteur RAG
    rag_engine = test_rag_engine(vector_store)
    
    if not rag_engine:
        print("\n❌ Impossible de continuer sans moteur RAG")
        return
    
    # Test 4: Questions
    test_questions(rag_engine)
    
    print("\n✅ Tests terminés!")


if __name__ == "__main__":
    main()
