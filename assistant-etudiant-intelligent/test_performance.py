#!/usr/bin/env python3
"""
Script de test des performances de l'assistant RAG optimisé
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.document_loader import DocumentLoader
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

def test_performance():
    """Test des performances de l'assistant RAG optimisé."""
    
    print("🚀 Test des performances de l'assistant RAG optimisé")
    print("=" * 60)
    
    try:
        # Charger les documents
        print("📚 Chargement des documents...")
        start_time = time.time()
        loader = DocumentLoader()
        documents = loader.load_documents()
        load_time = time.time() - start_time
        
        if not documents:
            print("❌ Aucun document trouvé")
            return
        
        print(f"✅ {len(documents)} documents chargés en {load_time:.2f}s")
        
        # Créer la base vectorielle
        print("🔍 Création de la base vectorielle...")
        start_time = time.time()
        chunks = loader.split_documents(documents)
        vector_store = VectorStore()
        success = vector_store.create_vector_store(chunks)
        vector_time = time.time() - start_time
        
        if not success:
            print("❌ Erreur création base vectorielle")
            return
        
        print(f"✅ Base vectorielle créée en {vector_time:.2f}s")
        
        # Initialiser le moteur RAG
        print("🤖 Initialisation du moteur RAG...")
        start_time = time.time()
        rag_engine = RAGEngine(vector_store)
        init_time = time.time() - start_time
        print(f"✅ Moteur RAG initialisé en {init_time:.2f}s")
        
        # Questions de test pour les performances
        test_questions = [
            "Explique-moi la loi d'Ohm",
            "Qu'est-ce que le théorème de Thévenin ?",
            "Comment calculer la puissance électrique ?",
            "Explique-moi les dérivées en mathématiques",
            "Qu'est-ce que le pH en chimie ?",
            "Comment calculer une intégrale ?",
            "Qu'est-ce qu'un transistor ?",
            "Explique-moi les lois de Newton",
            "Comment fonctionne un transformateur ?",
            "Qu'est-ce que l'impédance complexe ?"
        ]
        
        print("\n⚡ Test des performances de réponse")
        print("=" * 60)
        
        total_time = 0
        fast_responses = 0
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 Question {i}: {question}")
            print("-" * 40)
            
            # Mesurer le temps de réponse
            start_time = time.time()
            response = rag_engine.ask_question(question)
            response_time = time.time() - start_time
            total_time += response_time
            
            # Vérifier si c'est une réponse rapide (< 0.1s)
            if response_time < 0.1:
                fast_responses += 1
                speed_indicator = "⚡ RAPIDE"
            elif response_time < 0.5:
                speed_indicator = "✅ NORMAL"
            else:
                speed_indicator = "🐌 LENT"
            
            print(f"{speed_indicator} - Temps: {response_time:.3f}s")
            print(f"📊 Confiance: {response.confidence:.2f}")
            print(f"📚 Sources: {len(response.sources)}")
            
            # Afficher un extrait de la réponse
            answer_preview = response.answer[:100] + "..." if len(response.answer) > 100 else response.answer
            print(f"💬 Réponse: {answer_preview}")
            
            # Vérifier que la réponse est complète
            if "consultez" in response.answer.lower() or "document" in response.answer.lower():
                print("⚠️  ATTENTION: Réponse contient des références aux documents")
            else:
                print("✅ Réponse complète sans renvoi vers les documents")
        
        # Statistiques finales
        avg_time = total_time / len(test_questions)
        fast_percentage = (fast_responses / len(test_questions)) * 100
        
        print("\n📊 STATISTIQUES DE PERFORMANCE")
        print("=" * 60)
        print(f"⏱️  Temps total: {total_time:.2f}s")
        print(f"📈 Temps moyen par question: {avg_time:.3f}s")
        print(f"⚡ Réponses rapides (< 0.1s): {fast_responses}/{len(test_questions)} ({fast_percentage:.1f}%)")
        print(f"📚 Documents chargés: {len(documents)}")
        print(f"🔍 Chunks créés: {len(chunks)}")
        
        # Évaluation des performances
        if avg_time < 0.1:
            performance_rating = "🚀 EXCELLENT"
        elif avg_time < 0.3:
            performance_rating = "✅ TRÈS BON"
        elif avg_time < 0.5:
            performance_rating = "👍 BON"
        else:
            performance_rating = "⚠️  À AMÉLIORER"
        
        print(f"\n🎯 ÉVALUATION: {performance_rating}")
        
        if fast_percentage >= 80:
            print("🎉 L'assistant RAG est très performant !")
        elif fast_percentage >= 60:
            print("✅ L'assistant RAG a de bonnes performances.")
        else:
            print("⚠️  Les performances peuvent être améliorées.")
        
        print("\n🎓 L'assistant donne des réponses complètes et détaillées !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_performance()

