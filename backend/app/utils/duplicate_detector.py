import hashlib
import os
from difflib import SequenceMatcher

class DuplicateDetector:
    def __init__(self):
        pass
    
    def detect_duplicates(self, file_path: str, existing_documents):
        """Detect duplicates using multiple strategies"""
        
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        for doc in existing_documents:
            if (doc.original_filename == filename and 
                abs(doc.original_size - file_size) < 1000):  # Within 1KB
                return doc, 'filename_size_match'
            
            similarity = SequenceMatcher(None, filename, doc.original_filename).ratio()
            if similarity > 0.9:
                return doc, 'name_similarity'
        
        return None, None