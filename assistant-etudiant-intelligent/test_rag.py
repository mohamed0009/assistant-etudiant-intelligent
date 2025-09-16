#!/usr/bin/env python3
"""
Test script for RAG functionality
"""
import requests
import json

def test_rag_endpoint():
    """Test the RAG endpoint with various questions"""
    print("🧪 Testing RAG Endpoint")
    print("=" * 50)
    
    url = 'http://localhost:8000/api/rag/question'
    
    # Test questions in French
    questions = [
        "Quelle est la loi d'Ohm et comment l'utiliser ?",
        "Explique le théorème de Thévenin",
        "Qu'est-ce qu'un circuit RC ?",
        "Comment résoudre une équation différentielle ?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Testing: {question}")
        
        payload = {
            'question': question,
            'conversation_id': f'test_{i}'
        }
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   💬 Answer: {result.get('answer', 'No answer')[:200]}...")
            print(f"   📚 Sources: {len(result.get('sources', []))} documents")
            print(f"   🤖 Model: {result.get('model', 'Unknown')}")
            
            if result.get('sources'):
                print("   📖 Top sources:")
                for j, source in enumerate(result['sources'][:2], 1):
                    print(f"      {j}. {source.get('source', 'Unknown')[:50]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ RAG endpoint test completed!")

if __name__ == "__main__":
    test_rag_endpoint()