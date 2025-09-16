#!/usr/bin/env python3
"""
Simple test to verify API functionality.
"""

import requests
import json
import time

def test_api():
    """Test basic API functionality."""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing API endpoints...")
    
    try:
        # Test status endpoint
        print("📊 Checking API status...")
        response = requests.get(f"{base_url}/api/status", timeout=5)
        
        if response.status_code == 200:
            status = response.json()
            print("✅ API Status:")
            print(f"   Documents loaded: {status.get('documents_loaded', False)}")
            print(f"   Total vectors: {status.get('total_vectors', 0)}")
            print(f"   Total documents: {status.get('total_documents', 0)}")
            print(f"   RAG engine ready: {status.get('rag_engine_ready', False)}")
            
            # Test documents endpoint
            print("\n📚 Checking documents...")
            response = requests.get(f"{base_url}/api/documents/stats", timeout=5)
            if response.status_code == 200:
                docs_stats = response.json()
                print(f"✅ Documents stats: {docs_stats}")
            else:
                print(f"❌ Documents endpoint returned {response.status_code}")
            
            return True
        else:
            print(f"❌ Status endpoint returned {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API - server may not be running")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == "__main__":
    test_api()