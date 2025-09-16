#!/usr/bin/env python3
"""
Test script for vector store functionality
"""
import sys
import os
sys.path.insert(0, 'src')

from src.vector_store import EnhancedVectorStore
from src.document_loader import EnhancedDocumentLoader

def test_vector_store():
    """Test the vector store with document loading"""
    print("🧪 Testing Vector Store Functionality")
    print("=" * 50)
    
    # Initialize components
    loader = EnhancedDocumentLoader(data_dir='data')
    vector_store = EnhancedVectorStore(store_path='faiss_index')
    
    # Check initial status
    print("📊 Initial Status:")
    print(f"   Documents: {vector_store.stats.get('total_documents', 0)}")
    print(f"   Vectors: {vector_store.stats.get('total_vectors', 0)}")
    
    # Load documents if needed
    if vector_store.stats.get('total_documents', 0) == 0:
        print("\n🔄 Loading documents...")
        documents = loader.load_documents()
        print(f"   Loaded {len(documents)} documents")
        
        if documents:
            # Split documents into chunks
            chunks = loader.split_documents(documents)
            print(f"   Created {len(chunks)} chunks")
            
            # Create vector store
            success = vector_store.create_vector_store(chunks)
            print(f"   Vector store created: {success}")
            print(f"   Final documents: {vector_store.stats.get('total_documents', 0)}")
            print(f"   Final vectors: {vector_store.stats.get('total_vectors', 0)}")
    else:
        print("\n✅ Documents already loaded")
    
    # Test search functionality
    print("\n🔍 Testing search...")
    queries = [
        "loi Ohm",
        "théorème de Thévenin",
        "électronique",
        "algèbre linéaire"
    ]
    
    for query in queries:
        results = vector_store.search_documents(query, k=2)
        print(f"   '{query}' → {len(results)} results")
        if results:
            # Handle both tuple and dict formats
            first_result = results[0]
            if isinstance(first_result, tuple):
                doc, score = first_result
                source = doc.metadata.get('source', 'Unknown') if hasattr(doc, 'metadata') else 'Unknown'
                print(f"     Top result: {source}")
            else:
                source = first_result.get('source', 'Unknown') if isinstance(first_result, dict) else 'Unknown'
                print(f"     Top result: {source}")
    
    print("\n✅ Vector store test completed!")

if __name__ == "__main__":
    test_vector_store()