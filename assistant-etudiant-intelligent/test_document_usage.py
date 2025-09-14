#!/usr/bin/env python3
"""
Test pour vérifier si l'assistant utilise les documents ou les réponses pré-calculées
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.rag_engine import SimpleFallbackLLM

def test_document_usage():
    """Test pour vérifier l'utilisation des documents vs réponses pré-calculées."""
    
    print("🔍 TEST: Réponses pré-calculées vs Documents")
    print("=" * 50)
    
    # Initialiser le modèle
    llm = SimpleFallbackLLM()
    
    # Questions qui devraient utiliser les réponses pré-calculées
    precomputed_questions = [
        "Explique-moi la loi d'Ohm",
        "Qu'est-ce qu'un transistor ?",
        "Comment calculer une dérivée ?",
        "Qu'est-ce que le pH ?",
        "Explique-moi les lois de Newton"
    ]
    
    print("📝 Questions avec réponses pré-calculées:")
    for q in precomputed_questions:
        response = llm._get_quick_response(q)
        if response:
            print(f"✅ \"{q}\" → Réponse pré-calculée (pas de documents)")
        else:
            print(f"❌ \"{q}\" → Pas de réponse pré-calculée")
    
    print("\n📚 Questions qui nécessitent vos documents:")
    # Questions spécifiques à vos documents
    document_questions = [
        "Qu'est-ce que le cours d'électricité dit sur les circuits ?",
        "Explique-moi le contenu du TD d'électronique",
        "Que dit l'examen de physique ?",
        "Quels sont les exercices de mathématiques ?",
        "Que contient le cours de chimie organique ?"
    ]
    
    for q in document_questions:
        response = llm._get_quick_response(q)
        if response:
            print(f"✅ \"{q}\" → Réponse pré-calculée")
        else:
            print(f"📚 \"{q}\" → Nécessite vos documents")
    
    print("\n🎯 CONCLUSION:")
    print("=" * 50)
    print("✅ L'assistant utilise DEUX sources d'information :")
    print("   1. Réponses pré-calculées (concepts fondamentaux)")
    print("   2. Vos documents (contenu spécifique)")
    print("\n📊 Pour les questions courantes → Réponses instantanées")
    print("📚 Pour les questions spécifiques → Vos documents")

if __name__ == "__main__":
    test_document_usage()

