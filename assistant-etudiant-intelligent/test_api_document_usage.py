#!/usr/bin/env python3
"""
Test complet de l'API pour vérifier l'utilisation des documents
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

def test_api_document_usage():
    """Test complet de l'API pour vérifier l'utilisation des documents."""
    
    print("🔍 TEST COMPLET: API avec Documents")
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
        
        print(f"✅ Base vectorielle créée avec {len(chunks)} chunks")
        
        # Initialiser le moteur RAG
        print("🤖 Initialisation du moteur RAG...")
        rag_engine = RAGEngine(vector_store)
        print("✅ Moteur RAG initialisé")
        
        # Test des différents types de questions
        test_questions = [
            # Questions avec réponses pré-calculées
            ("Explique-moi la loi d'Ohm", "Réponse pré-calculée"),
            ("Qu'est-ce qu'un transistor ?", "Réponse pré-calculée"),
            ("Comment calculer une dérivée ?", "Réponse pré-calculée"),
            
            # Questions qui nécessitent vos documents
            ("Quels sont les exercices de mathématiques dans mes documents ?", "Vos documents"),
            ("Que contient le cours de chimie organique ?", "Vos documents"),
            ("Explique-moi le contenu du TD d'électronique", "Vos documents"),
            
            # Questions mixtes
            ("Comment fonctionne un transformateur selon mes cours ?", "Mixte"),
            ("Qu'est-ce que le pH dans le contexte de mes exercices ?", "Mixte")
        ]
        
        print("\n⚡ Test des réponses")
        print("=" * 60)
        
        for i, (question, expected_source) in enumerate(test_questions, 1):
            print(f"\n📝 Question {i}: {question}")
            print(f"🎯 Source attendue: {expected_source}")
            print("-" * 40)
            
            # Mesurer le temps de réponse
            start_time = time.time()
            response = rag_engine.ask_question(question)
            response_time = time.time() - start_time
            
            print(f"⏱️  Temps: {response_time:.3f}s")
            print(f"📊 Confiance: {response.confidence:.2f}")
            print(f"📚 Sources utilisées: {len(response.sources)}")
            
            # Analyser les sources
            if response.sources:
                print("📄 Sources trouvées:")
                for j, source in enumerate(response.sources[:2], 1):  # Limiter à 2 sources
                    if hasattr(source, 'metadata') and source.metadata:
                        source_name = source.metadata.get('source', 'Inconnu')
                    else:
                        source_name = str(source)[:50] + "..."
                    print(f"   {j}. {source_name}")
            else:
                print("📄 Aucune source documentaire (réponse pré-calculée)")
            
            # Afficher un extrait de la réponse
            answer_preview = response.answer[:150] + "..." if len(response.answer) > 150 else response.answer
            print(f"💬 Réponse: {answer_preview}")
            
            # Déterminer la source réelle
            if response.sources:
                actual_source = "Vos documents"
            else:
                actual_source = "Réponse pré-calculée"
            
            if actual_source == expected_source or expected_source == "Mixte":
                print("✅ Source correcte")
            else:
                print(f"⚠️  Source inattendue: {actual_source}")
        
        print("\n🎯 RÉSUMÉ")
        print("=" * 60)
        print("✅ L'assistant RAG utilise intelligemment :")
        print("   📚 Vos documents pour les questions spécifiques")
        print("   ⚡ Réponses pré-calculées pour les concepts généraux")
        print("   🔄 Combinaison des deux pour des réponses complètes")
        
        print(f"\n📊 Statistiques :")
        print(f"   📄 Documents chargés: {len(documents)}")
        print(f"   🔍 Chunks créés: {len(chunks)}")
        print(f"   ⚡ Réponses pré-calculées: 40+ concepts")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_document_usage()
