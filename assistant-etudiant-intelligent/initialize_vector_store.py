#!/usr/bin/env python3
"""
Initialize the vector store with documents from the data directory.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from document_loader import EnhancedDocumentLoader
from vector_store import EnhancedVectorStore

def initialize_vector_store():
    """Initialize the vector store with all documents."""
    print("🔄 Initializing vector store with documents...")
    
    try:
        # Initialize components
        loader = EnhancedDocumentLoader()
        vector_store = EnhancedVectorStore(store_path="faiss_index")
        
        # Load documents from data directory
        data_dir = "data"
        if os.path.exists(data_dir):
            print(f"📁 Loading documents from {data_dir}...")
            documents = loader.load_documents()
            print(f"📄 Loaded {len(documents)} documents")
            
            if documents:
                # Split documents into chunks
                chunks = loader.split_documents(documents)
                print(f"✂️ Created {len(chunks)} chunks")
                
                # Create vector store
                success = vector_store.create_vector_store(chunks)
                if success:
                    print("✅ Vector store created successfully")
                    print(f"📊 Total documents: {vector_store.stats['total_documents']}")
                    print(f"📊 Total vectors: {vector_store.stats['total_vectors']}")
                    
                    # Test search
                    results = vector_store.search_documents("loi Ohm", k=2)
                    print(f"🔍 Search test: {len(results)} results found")
                    
                    return True
                else:
                    print("❌ Failed to create vector store")
                    return False
            else:
                print("❌ No documents found in data directory")
                return False
        else:
            print(f"❌ Data directory '{data_dir}' not found")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing vector store: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = initialize_vector_store()
    if success:
        print("🎉 Vector store initialization completed!")
    else:
        print("💥 Vector store initialization failed!")
        sys.exit(1)