#!/usr/bin/env python3
"""
Final test script for RAG functionality
"""
import requests
import json
import time

def test_rag_endpoints():
    """Test all RAG endpoints"""
    print("🧪 Testing RAG Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("\n1. Testing server health...")
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"   ✅ Docs endpoint: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing docs: {e}")
    
    # Test RAG question endpoint
    print("\n2. Testing RAG question endpoint...")
    
    # Test with /rag/question
    urls_to_test = [
        "/rag/question",
        "/api/rag/question"
    ]
    
    payload = {
        "question": "Quelle est la loi d'Ohm et comment l'utiliser ?",
        "conversation_id": 1
    }
    
    for url_path in urls_to_test:
        full_url = f"{base_url}{url_path}"
        print(f"\n   Testing: {full_url}")
        
        try:
            response = requests.post(full_url, json=payload, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   Answer preview: {result.get('answer', 'No answer')[:150]}...")
                print(f"   Sources: {len(result.get('sources', []))}")
                print(f"   Model: {result.get('metadata', {}).get('model_used', 'Unknown')}")
                break
            elif response.status_code == 404:
                print(f"   ❌ Endpoint not found")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test simple GET to check if server is responding
    print("\n3. Testing server connectivity...")
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   Base URL response: {response.status_code}")
    except Exception as e:
        print(f"   Base URL error: {e}")

if __name__ == "__main__":
    test_rag_endpoints()