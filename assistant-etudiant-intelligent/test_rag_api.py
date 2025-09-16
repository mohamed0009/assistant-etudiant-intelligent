#!/usr/bin/env python3
"""
Test script to verify RAG API functionality
"""

import requests
import json
import time

def test_rag_api():
    """Test the RAG API with sample questions."""
    
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/rag/question"
    
    # Test questions
    questions = [
        "Quelle est la loi d'Ohm?",
        "Explique le théorème de Thévenin",
        "Qu'est-ce que la thermodynamique?",
        "Comment calculer une dérivée?"
    ]
    
    print("🧪 Testing RAG API...")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Testing: {question}")
        
        try:
            payload = {
                "question": question,
                "conversation_id": f"test_{i}"
            }
            
            response = requests.post(endpoint, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Response time: {data.get('response_time', 'N/A')}s")
                print(f"   📄 Answer preview: {data.get('answer', 'No answer')[:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Request timed out")
        except requests.exceptions.ConnectionError:
            print("   🔌 Connection error - is the server running?")
        except Exception as e:
            print(f"   💥 Unexpected error: {e}")
        
        time.sleep(1)  # Brief pause between requests
    
    print("\n" + "=" * 50)
    print("✅ RAG API test completed!")

if __name__ == "__main__":
    test_rag_api()