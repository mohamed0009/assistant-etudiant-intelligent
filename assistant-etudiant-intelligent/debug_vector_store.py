#!/usr/bin/env python3
"""
Debug script to test vector store functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from vector_store import EnhancedVectorStore as VectorStore

def debug_vector_store():
    """Debug the vector store initialization and functionality."""
    print("🔄 Testing vector store initialization...")
    
    try:
        # Initialize vector store
        vector_store = VectorStore(store_path="faiss_index")
        print("✅ Vector store initialized")
        
        # Check if index exists
        if hasattr(vector_store, 'index') and vector_store.index is not None:
            print(f"✅ FAISS index loaded: {type(vector_store.index)}")
            print(f"✅ Index dimension: {vector_store.dimension}")
            print(f"✅ Total vectors: {vector_store.stats['total_vectors']}")
            print(f"✅ Total documents: {vector_store.stats['total_documents']}")
        else:
            print("❌ No FAISS index found")
            
        # Test search
        if vector_store.stats['total_vectors'] > 0:
            print("🔄 Testing search...")
            results = vector_store.search_documents("test query", k=2)
            print(f"✅ Search returned {len(results)} results")
            
            if results:
                doc, score = results[0]
                print(f"✅ First result score: {score}")
                print(f"✅ First result content preview: {doc.page_content[:100]}...")
        else:
            print("⚠️ No documents loaded, skipping search test")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_vector_store()