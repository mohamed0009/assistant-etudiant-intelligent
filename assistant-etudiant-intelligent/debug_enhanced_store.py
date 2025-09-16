#!/usr/bin/env python3
"""
Debug script to test EnhancedVectorStore loading.
"""

import sys
import os
sys.path.append('src')

from src.vector_store import EnhancedVectorStore

def debug_enhanced_store():
    """Debug EnhancedVectorStore loading."""
    
    print("🔍 Debugging EnhancedVectorStore...")
    
    # Create EnhancedVectorStore instance
    vector_store = EnhancedVectorStore(
        embeddings_model="all-MiniLM-L6-v2",
        index_type="flat",
        store_path="enhanced_vector_store"
    )
    
    # Try to load existing store
    success = vector_store.load_vector_store()
    
    if success:
        print("✅ Successfully loaded EnhancedVectorStore")
        print(f"📊 Total vectors: {vector_store.stats['total_vectors']}")
        print(f"📄 Total documents: {vector_store.stats['total_documents']}")
        print(f"🗂️  Index type: {vector_store.stats['index_type']}")
        print(f"🤖 Embeddings model: {vector_store.stats['embeddings_model']}")
    else:
        print("❌ Failed to load EnhancedVectorStore")
        
        # Check if files exist
        import os
        from pathlib import Path
        
        store_path = Path("enhanced_vector_store")
        required_files = ["index.faiss", "documents.pkl", "lookup.json", "stats.json"]
        
        print("\n📁 Checking files:")
        for file_name in required_files:
            file_path = store_path / file_name
            exists = "✅" if file_path.exists() else "❌"
            size = file_path.stat().st_size if file_path.exists() else 0
            print(f"{exists} {file_name}: {size} bytes")
    
    return success

if __name__ == "__main__":
    debug_enhanced_store()