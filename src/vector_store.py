"""
Enhanced Vector Store for Professional RAG System
Advanced vector storage and retrieval with FAISS and optimizations.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
import json
import pickle
import logging
from datetime import datetime
from pathlib import Path

from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

class EnhancedVectorStore:
    """Professional vector store with advanced features."""
    
    def __init__(
        self,
        embeddings_model: str = "all-MiniLM-L6-v2",
        index_type: str = "flat",
        dimension: int = 384,
        store_path: str = "enhanced_vector_store",
        enable_optimization: bool = True
    ):
        self.embeddings_model = embeddings_model
        self.index_type = index_type
        self.dimension = dimension
        self.store_path = Path(store_path)
        self.enable_optimization = enable_optimization
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embeddings_model,
            model_kwargs={'device': 'cpu'}
        )
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Create directory
        self.store_path.mkdir(exist_ok=True)
        
        # Initialize storage
        self.index = None
        self.documents = []
        self.document_lookup = {}
        
        # Initialize statistics
        self.stats = {
            "total_vectors": 0,
            "total_documents": 0,
            "last_updated": None,
            "index_type": index_type,
            "embeddings_model": embeddings_model
        }
        
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index based on type."""
        if self.index_type == "flat":
            self.index = faiss.IndexFlatL2(self.dimension)
        elif self.index_type == "ivf":
            quantizer = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIVFFlat(
                quantizer, self.dimension, min(100, self.stats["total_vectors"] + 1)
            )
        elif self.index_type == "hnsw":
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
    
    def create_vector_store(self, documents: List[Document]) -> bool:
        """Create vector store from documents."""
        self.logger.info("🔍 Creating vector store...")
        
        try:
            # Reset storage
            self._initialize_index()
            self.documents = []
            self.document_lookup = {}
            
            # Process documents
            embeddings_list = []
            for i, doc in enumerate(documents):
                try:
                    # Generate embedding
                    embedding = self.embeddings.embed_documents(
                        [doc.page_content]
                    )[0]
                    
                    # Store document and mapping
                    self.documents.append(doc)
                    self.document_lookup[i] = {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    embeddings_list.append(embedding)
                    
                except Exception as e:
                    self.logger.error(f"Error processing document {i}: {e}")
                    continue
            
            if not embeddings_list:
                self.logger.error("❌ No valid embeddings generated")
                return False
            
            # Convert to numpy array and add to index
            embeddings_array = np.array(embeddings_list).astype('float32')
            self.index.add(embeddings_array)
            
            # Update statistics
            self.stats.update({
                "total_vectors": len(embeddings_list),
                "total_documents": len(self.documents),
                "last_updated": datetime.now().isoformat()
            })
            
            self.logger.info(f"✅ Created vector store with {len(embeddings_list)} vectors")
            
            # Save immediately
            self.save_vector_store()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error creating vector store: {e}")
            return False
    
    def search_documents(
        self,
        query: str,
        k: int = 5,
        use_reranking: bool = True
    ) -> List[Tuple[Document, float]]:
        """Search for similar documents with optional reranking."""
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in FAISS index
            distances, indices = self.index.search(
                np.array([query_embedding]).astype('float32'),
                k * 2 if use_reranking else k
            )
            
            results = []
            for score, idx in zip(distances[0], indices[0]):
                if idx >= 0 and idx < len(self.documents):
                    doc = self.documents[idx]
                    results.append((doc, float(score)))
            
            if use_reranking:
                results = self._rerank_results(query, results)[:k]
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching documents: {e}")
            return []
    
    def _rerank_results(
        self,
        query: str,
        results: List[Tuple[Document, float]]
    ) -> List[Tuple[Document, float]]:
        """Rerank results using semantic similarity."""
        try:
            # Get semantic scores
            query_embedding = self.embeddings.embed_query(query)
            
            reranked = []
            for doc, score in results:
                doc_embedding = self.embeddings.embed_documents(
                    [doc.page_content]
                )[0]
                
                # Calculate semantic similarity
                semantic_score = np.dot(query_embedding, doc_embedding)
                
                # Combine with original score
                combined_score = (semantic_score + (1 - score)) / 2
                reranked.append((doc, combined_score))
            
            # Sort by combined score
            return sorted(reranked, key=lambda x: x[1], reverse=True)
            
        except Exception as e:
            self.logger.error(f"Error reranking results: {e}")
            return results
    
    def optimize_index(self):
        """Optimize the vector store index."""
        if not self.enable_optimization:
            return
        
        self.logger.info("🔧 Optimizing vector store...")
        
        try:
            if self.index_type == "ivf":
                # Train IVF index
                if not self.index.is_trained and self.stats["total_vectors"] > 0:
                    self.index.train(
                        np.array([
                            self.embeddings.embed_documents([doc.page_content])[0]
                            for doc in self.documents
                        ]).astype('float32')
                    )
            
            elif self.index_type == "hnsw":
                # Optimize HNSW parameters
                if self.stats["total_vectors"] > 10000:
                    self.index.hnsw.efConstruction = 40
                    self.index.hnsw.efSearch = 32
            
            self.logger.info("✅ Index optimization complete")
            
        except Exception as e:
            self.logger.error(f"❌ Error optimizing index: {e}")
    
    def save_vector_store(self) -> bool:
        """Save vector store to disk."""
        try:
            # Save FAISS index
            faiss.write_index(
                self.index,
                str(self.store_path / "index.faiss")
            )
            
            # Save documents and metadata
            with open(self.store_path / "documents.pkl", "wb") as f:
                pickle.dump(self.documents, f)
            
            with open(self.store_path / "lookup.json", "w") as f:
                json.dump(self.document_lookup, f)
            
            # Save statistics
            with open(self.store_path / "stats.json", "w") as f:
                json.dump(self.stats, f)
            
            self.logger.info("✅ Vector store saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving vector store: {e}")
            return False
    
    def load_vector_store(self) -> bool:
        """Load vector store from disk."""
        try:
            index_path = self.store_path / "index.faiss"
            documents_path = self.store_path / "documents.pkl"
            lookup_path = self.store_path / "lookup.json"
            stats_path = self.store_path / "stats.json"
            
            if not all(p.exists() for p in [index_path, documents_path, lookup_path, stats_path]):
                return False
            
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load documents and metadata
            with open(documents_path, "rb") as f:
                self.documents = pickle.load(f)
            
            with open(lookup_path) as f:
                self.document_lookup = json.load(f)
            
            # Load statistics
            with open(stats_path) as f:
                self.stats = json.load(f)
            
            self.logger.info(f"✅ Loaded vector store with {self.stats['total_vectors']} vectors")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error loading vector store: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive vector store statistics."""
        stats = self.stats.copy()
        
        # Add memory usage
        if self.index:
            stats["index_memory_usage"] = self.index.getNumVectors() * self.dimension * 4  # 4 bytes per float
        
        # Add index type specific stats
        if self.index_type == "ivf":
            stats["ivf_trained"] = getattr(self.index, "is_trained", False)
        elif self.index_type == "hnsw":
            stats["hnsw_ef_construction"] = getattr(self.index, "hnsw.efConstruction", 0)
        
        return stats
    
    def get_vector_store_info(self) -> Dict[str, Any]:
        """Get basic vector store information."""
        return {
            "total_vectors": self.stats["total_vectors"],
            "total_documents": self.stats["total_documents"],
            "index_type": self.index_type,
            "embeddings_model": self.embeddings_model,
            "dimension": self.dimension,
            "last_updated": self.stats["last_updated"]
        }
