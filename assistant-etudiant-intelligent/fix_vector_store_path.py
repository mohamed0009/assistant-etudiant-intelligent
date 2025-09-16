#!/usr/bin/env python3
"""
Fix vector store path issue by copying files to the correct directory.
"""

import shutil
import os
from pathlib import Path

def fix_vector_store_path():
    """Copy vector store files to the correct directory."""
    
    # Source directory (existing)
    source_dir = Path("faiss_index")
    
    # Target directory (where EnhancedVectorStore expects it)
    target_dir = Path("enhanced_vector_store")
    
    if not source_dir.exists():
        print("❌ Source directory 'faiss_index' not found")
        return False
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(exist_ok=True)
    
    # Copy all files
    files_to_copy = [
        "documents.pkl",
        "index.faiss", 
        "lookup.json",
        "stats.json"
    ]
    
    copied_files = []
    for file_name in files_to_copy:
        source_file = source_dir / file_name
        target_file = target_dir / file_name
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            copied_files.append(file_name)
            print(f"✅ Copied {file_name}")
        else:
            print(f"⚠️  {file_name} not found in source")
    
    if copied_files:
        print(f"✅ Successfully copied {len(copied_files)} files to {target_dir}")
        return True
    else:
        print("❌ No files were copied")
        return False

if __name__ == "__main__":
    fix_vector_store_path()