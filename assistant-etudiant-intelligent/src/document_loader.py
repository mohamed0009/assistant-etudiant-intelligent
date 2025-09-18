"""
Enhanced Document Loader for Professional RAG System
Handles multiple document formats with advanced processing and caching.
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
import json
import logging
from datetime import datetime

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    DirectoryLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader
)

class EnhancedDocumentLoader:
    """Professional document loader with advanced features."""
    
    def __init__(
        self,
        data_dir: str = "data",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        enable_cache: bool = True,
        cache_dir: str = "cache"
    ):
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.enable_cache = enable_cache
        self.cache_dir = Path(cache_dir)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        if enable_cache:
            self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize stats
        self.stats = {
            "total_documents": 0,
            "total_chunks": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "processing_errors": []
        }
    
    def load_documents(self) -> List[Document]:
        """Load all documents from the data directory with caching."""
        self.logger.info("Loading documents...")
        
        try:
            all_documents = []
            
            # Load different file types
            loaders = {
                "**/*.pdf": (PyPDFLoader, {}),
                "**/*.txt": (TextLoader, {"encoding": "utf-8"}),
                "**/*.docx": (Docx2txtLoader, {}),
                "**/*.md": (UnstructuredMarkdownLoader, {})
            }
            
            for glob_pattern, (loader_class, loader_args) in loaders.items():
                try:
                    # Use DirectoryLoader for each file type
                    loader = DirectoryLoader(
                        str(self.data_dir),
                        glob=glob_pattern,
                        loader_cls=loader_class,
                        loader_kwargs=loader_args
                    )
                    
                    docs = self._load_with_cache(loader, glob_pattern)
                    all_documents.extend(docs)
                    
                except Exception as e:
                    self.logger.error(f"Error loading {glob_pattern}: {e}")
                    self.stats["processing_errors"].append(
                        f"Error with {glob_pattern}: {str(e)}"
                    )
            
            self.stats["total_documents"] = len(all_documents)
            self.logger.info(f"Loaded {len(all_documents)} documents")
            
            return all_documents
            
        except Exception as e:
            self.logger.error(f"Error loading documents: {e}")
            raise
    
    def _load_with_cache(self, loader, pattern: str) -> List[Document]:
        """Load documents using cache if enabled."""
        if not self.enable_cache:
            return loader.load()
        
        # Create cache key based on files and their modification times
        files = list(self.data_dir.glob(pattern[3:]))  # Remove **/ prefix
        if not files:
            return []
        
        cache_key = self._create_cache_key(files)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        # Try to load from cache
        if cache_file.exists():
            try:
                cached_data = json.loads(cache_file.read_text())
                docs = [
                    Document(
                        page_content=d["page_content"],
                        metadata=d["metadata"]
                    )
                    for d in cached_data
                ]
                self.stats["cache_hits"] += 1
                return docs
            except:
                self.stats["cache_misses"] += 1
        
        # Load and cache if not found
        docs = loader.load()
        if docs:
            cache_data = [
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
            cache_file.write_text(json.dumps(cache_data))
        
        return docs
    
    def _create_cache_key(self, files: List[Path]) -> str:
        """Create a unique cache key based on files and their modification times."""
        content = []
        for file in sorted(files):
            mtime = os.path.getmtime(file)
            content.append(f"{file}:{mtime}")
        
        return hashlib.md5("|".join(content).encode()).hexdigest()
    
    def split_documents(
        self,
        documents: List[Document],
        custom_chunk_size: Optional[int] = None,
        custom_chunk_overlap: Optional[int] = None
    ) -> List[Document]:
        """Split documents into chunks with metadata preservation."""
        self.logger.info("Splitting documents...")
        
        chunk_size = custom_chunk_size or self.chunk_size
        chunk_overlap = custom_chunk_overlap or self.chunk_overlap
        
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = []
            for doc in documents:
                try:
                    doc_chunks = splitter.split_documents([doc])
                    
                    # Add enhanced metadata
                    for i, chunk in enumerate(doc_chunks):
                        chunk.metadata.update({
                            "chunk_id": i,
                            "total_chunks": len(doc_chunks),
                            "chunk_size": chunk_size,
                            "source_length": len(doc.page_content),
                            "processing_date": datetime.now().isoformat()
                        })
                    
                    chunks.extend(doc_chunks)
                    
                except Exception as e:
                    self.logger.error(f"Error splitting document {doc.metadata.get('source', 'unknown')}: {e}")
                    self.stats["processing_errors"].append(
                        f"Splitting error: {str(e)}"
                    )
            
            self.stats["total_chunks"] = len(chunks)
            self.logger.info(f"Created {len(chunks)} chunks")
            
            return chunks
            
        except Exception as e:
            self.logger.error(f"Error splitting documents: {e}")
            raise
    
    def validate_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Validate document quality and completeness."""
        validation_results = {
            "total_documents": len(documents),
            "valid_documents": 0,
            "empty_documents": 0,
            "issues": [],
            "statistics": {
                "avg_length": 0,
                "total_words": 0,
                "languages": set()
            }
        }
        
        total_length = 0
        
        for doc in documents:
            # Basic validation
            if not doc.page_content.strip():
                validation_results["empty_documents"] += 1
                validation_results["issues"].append({
                    "file": doc.metadata.get("source", "unknown"),
                    "issue": "Empty content"
                })
                continue
            
            # Content checks
            content_length = len(doc.page_content)
            total_length += content_length
            
            if content_length < 100:
                validation_results["issues"].append({
                    "file": doc.metadata.get("source", "unknown"),
                    "issue": "Very short content"
                })
            
            # Count valid documents
            validation_results["valid_documents"] += 1
            
            # Update statistics
            validation_results["statistics"]["total_words"] += len(
                doc.page_content.split()
            )
        
        # Calculate averages
        if validation_results["valid_documents"] > 0:
            validation_results["statistics"]["avg_length"] = (
                total_length / validation_results["valid_documents"]
            )
        
        return validation_results
    
    def get_processing_report(self, documents: List[Document]) -> str:
        """Generate a detailed processing report."""
        report = [
            "📊 Document Processing Report",
            "=" * 30,
            f"Total Documents: {self.stats['total_documents']}",
            f"Total Chunks: {self.stats['total_chunks']}",
            f"Cache Hits: {self.stats['cache_hits']}",
            f"Cache Misses: {self.stats['cache_misses']}",
            "\nDocument Types:",
        ]
        
        # Count document types
        doc_types = {}
        for doc in documents:
            doc_type = doc.metadata.get("source", "unknown").split(".")[-1]
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        for doc_type, count in doc_types.items():
            report.append(f"  - {doc_type}: {count}")
        
        # Add errors if any
        if self.stats["processing_errors"]:
            report.extend([
                "\nProcessing Errors:",
                *[f"  - {error}" for error in self.stats["processing_errors"]]
            ])
        
        return "\n".join(report)
    
    def clear_cache(self):
        """Clear the document processing cache."""
        if self.enable_cache and self.cache_dir.exists():
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_file.unlink()
                except Exception as e:
                    self.logger.error(f"Error deleting cache file {cache_file}: {e}")
            
            self.logger.info("✨ Cache cleared successfully")
