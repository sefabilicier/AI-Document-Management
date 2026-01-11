import os
import hashlib
import magic
from pathlib import Path
from datetime import datetime
import shutil
from sqlalchemy.orm import Session

from app.models import Document
from app.utils.file_utils import FileUtils

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.file_utils = FileUtils()
    
    def process_document(self, file_path: str, original_filename: str) -> Document:
        """Process a document with improved duplicate detection"""
        
        file_type = self.file_utils.detect_file_type(file_path)
        original_size = os.path.getsize(file_path)
        
        # BETTER DUPLICATE DETECTION
        file_hash = self.file_utils.calculate_file_hash(file_path)
        
        # Check ALL documents, not just by hash
        all_docs = self.db.query(Document).all()
        
        duplicate_of = None
        for doc in all_docs:
            # Multiple duplicate detection strategies:
            
            # 1. Same filename and similar size
            if (doc.original_filename == original_filename and 
                abs(doc.original_size - original_size) < 1024):  # Within 1KB
                duplicate_of = doc.id
                break
            
            # 2. Same hash (exact duplicate)
            if doc.text_hash == file_hash:
                duplicate_of = doc.id
                break
        
        if duplicate_of:
            original_doc = self.db.query(Document).filter(Document.id == duplicate_of).first()
            return self._create_duplicate_record(original_doc, original_filename, file_hash)
        
        # SIMPLE OPTIMIZATION: Don't increase file size
        optimized_path = f"uploads/optimized/{original_filename}"
        os.makedirs(os.path.dirname(optimized_path), exist_ok=True)
        
        # For demo, just copy but track original size
        shutil.copy2(file_path, optimized_path)
        optimized_size = original_size  # Claim no change for demo
        
        # Calculate savings (0% for now to avoid negative)
        reduction_percentage = 0.0  # Default to 0% savings
        
        # Only show savings if we actually reduced size
        actual_size = os.path.getsize(optimized_path)
        if actual_size < original_size:
            reduction_percentage = ((original_size - actual_size) / original_size) * 100
            optimized_size = actual_size
        
        # Create document
        document = Document(
            original_filename=original_filename,
            original_size=original_size,
            optimized_size=optimized_size,
            file_type=file_type,
            storage_path=optimized_path,
            reduction_strategy='safe_copy',
            reduction_percentage=reduction_percentage,
            tier='hot' if file_type in ['pdf', 'docx'] else 'warm',
            is_duplicate=False,
            text_hash=file_hash,
            extracted_text=f"Sample content from {file_type}",
            upload_date=datetime.utcnow()
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        print(f"📄 {original_filename}: {original_size/1024:.1f}KB → {optimized_size/1024:.1f}KB ({reduction_percentage:.1f}%)")
        
        return document
    
    def _handle_duplicate(self, existing_doc: Document, new_filename: str) -> Document:
        """Handle exact file duplicate"""
        duplicate_doc = Document(
            original_filename=new_filename,
            original_size=existing_doc.original_size,
            optimized_size=existing_doc.optimized_size,
            file_type=existing_doc.file_type,
            storage_path=existing_doc.storage_path,
            reduction_percentage=existing_doc.reduction_percentage,
            is_duplicate=True,
            original_document_id=existing_doc.id,
            tier=existing_doc.tier
        )
        
        self.db.add(duplicate_doc)
        self.db.commit()
        self.db.refresh(duplicate_doc)
        
        return duplicate_doc
    
    def _optimize_document(self, file_path: str, file_type: str, filename: str):
        """Optimize document based on file type"""
        from app.utils.optimizers import get_optimizer
        
        optimizer = get_optimizer(file_type)
        optimized_path = f"uploads/optimized/{filename}"
        
        # Apply optimization
        optimized_size = optimizer.optimize(file_path, optimized_path)
        
        return optimized_path, optimized_size
    
    def _calculate_text_hash(self, text: str) -> str:
        """Calculate hash of extracted text"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _check_content_duplicate(self, text: str):
        """Check for content-based duplicates"""
        # Placeholder - will be implemented in Week 3
        return None
    
    def _generate_thumbnail(self, file_path: str, file_type: str, filename: str):
        """Generate thumbnail for document preview"""
        # Placeholder
        return None
    
    def _determine_storage_tier(self, file_type: str) -> str:
        """Determine initial storage tier"""
        # Simple logic for now
        if file_type in ['pdf', 'docx']:
            return 'hot'
        elif file_type in ['jpg', 'png']:
            return 'warm'
        else:
            return 'cold'
    
    def _calculate_reduction_percentage(self, original: int, optimized: int) -> float:
        """Calculate percentage reduction"""
        if original == 0:
            return 0.0
        return ((original - optimized) / original) * 100
    
    def _update_storage_metrics(self):
        """Update storage metrics table"""
        # Will be implemented later
        pass
    
    def check_for_duplicates(self, file_path: str, file_type: str, extracted_text: str) -> Document:
        """Check for duplicates using multiple methods"""
        
        # Method 1: Exact file hash
        file_hash = self.file_utils.calculate_file_hash(file_path)
        exact_duplicate = self.db.query(Document).filter(
            Document.text_hash == file_hash
        ).first()
        
        if exact_duplicate:
            return exact_duplicate
        
        # Method 2: Content similarity (for PDFs, DOCX)
        if file_type in ['pdf', 'docx', 'txt'] and extracted_text:
            # Get first 1000 chars for quick comparison
            text_sample = extracted_text[:1000]
            text_hash = hashlib.md5(text_sample.encode()).hexdigest()
            
            similar_docs = self.db.query(Document).filter(
                Document.extracted_text.isnot(None)
            ).all()
            
            for doc in similar_docs:
                if doc.extracted_text:
                    doc_sample = doc.extracted_text[:1000]
                    doc_hash = hashlib.md5(doc_sample.encode()).hexdigest()
                    
                    # If first 1000 chars match, likely duplicate
                    if text_hash == doc_hash:
                        return doc
        
        return None

    def _handle_content_duplicate(self, original_doc, new_filename):
        """Handle content-based duplicate"""
        duplicate_doc = Document(
            original_filename=new_filename,
            original_size=original_doc.original_size,
            optimized_size=original_doc.optimized_size,
            file_type=original_doc.file_type,
            storage_path=original_doc.storage_path,
            reduction_percentage=original_doc.reduction_percentage,
            is_duplicate=True,
            original_document_id=original_doc.id,
            tier=original_doc.tier,
            extracted_text=original_doc.extracted_text,
            text_hash=self._calculate_text_hash(original_doc.extracted_text)
        )
        
        self.db.add(duplicate_doc)
        self.db.commit()
        self.db.refresh(duplicate_doc)
        
        return duplicate_doc
    
    def _get_reduction_strategy(self, file_type: str) -> str:
        """Determine reduction strategy based on file type"""
        strategies = {
            'pdf': 'compression + deduplication',
            'jpg': 'image optimization',
            'jpeg': 'image optimization',
            'png': 'image optimization',
            'docx': 'metadata removal',
            'txt': 'text compression',
        }
        return strategies.get(file_type, 'general compression')

# Create a function to get embedding service instance
def get_embedding_service():
    """Get or create embedding service instance"""
    from app.services.embedding_service import EmbeddingService
    return EmbeddingService()