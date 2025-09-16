#!/usr/bin/env python3
"""
Test RAG system directly without API.
"""

import sys
import os
sys.path.append('src')

from src.vector_store import EnhancedVectorStore
from src.rag_engine import ProfessionalRAGEngine

def test_rag_system():
    """Test RAG system functionality directly."""
    
    print("🧪 Testing RAG system directly...")
    
    try:
        # Initialize vector store
        print("📊 Initializing vector store...")
        vector_store = EnhancedVectorStore(
            embeddings_model="all-MiniLM-L6-v2",
            index_type="flat",
            store_path="enhanced_vector_store"
        )
        
        # Load existing vector store
        if vector_store.load_vector_store():
            print("✅ Vector store loaded successfully")
            print(f"📊 Total vectors: {vector_store.stats['total_vectors']}")
            print(f"📄 Total documents: {vector_store.stats['total_documents']}")
            
            # Initialize RAG engine
            print("🤖 Initializing RAG engine...")
            rag_engine = ProfessionalRAGEngine(
                vector_store=vector_store,
                model_type="ollama",
                use_reranking=True
            )
            
            # Test search functionality
            print("\n🔍 Testing search functionality...")
            test_queries = [
                "Qu'est-ce que la loi d'Ohm ?",
                "Explique le théorème de Thévenin",
                "Comment calculer la résistance équivalente ?"
            ]
            
            for query in test_queries:
                print(f"\n❓ Query: {query}")
                try:
                    results = vector_store.search_documents(query, k=3)
                    if results:
                        print(f"✅ Found {len(results)} relevant documents")
                        for i, (doc, score) in enumerate(results, 1):
                            print(f"   {i}. Score: {score:.4f} - {doc.page_content[:100]}...")
                    else:
                        print("❌ No results found")
                except Exception as e:
                    print(f"❌ Search error: {e}")
            
            # Test RAG functionality
            print("\n🎯 Testing RAG functionality...")
            try:
                response = rag_engine.ask_question("Qu'est-ce que la loi d'Ohm ?")
                print(f"✅ RAG Response: {response.answer}")
                print(f"📊 Confidence: {response.confidence:.2f}")
                print(f"⚡ Processing time: {response.processing_time:.2f}s")
                print(f"📚 Sources used: {len(response.sources)}")
            except Exception as e:
                print(f"❌ RAG error: {e}")
            
            return True
            
        else:
            print("❌ Failed to load vector store")
            return False
            
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_rag_system()