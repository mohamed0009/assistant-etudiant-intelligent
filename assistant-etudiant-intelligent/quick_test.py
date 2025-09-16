#!/usr/bin/env python3
"""
Quick test for RAG API functionality
"""

import requests
import json
import sys

def test_simple():
    """Simple test to verify RAG works."""
    try:
        # Test basic health check
        health = requests.get("http://localhost:8000/", timeout=5)
        print(f"Health check: {health.status_code}")
        
        # Test RAG endpoint
        response = requests.post(
            "http://localhost:8000/rag/question",
            json={"question": "Quelle est la loi d'Ohm?", "conversation_id": "test1"},
            timeout=30
        )
        
        print(f"RAG response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ RAG API is working!")
            print(f"Answer: {data.get('answer', 'No answer')[:200]}...")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple()
    sys.exit(0 if success else 1)