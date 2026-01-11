from datetime import datetime, timedelta
from sqlalchemy.orm import Session

class TieringService:
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_and_tier_documents(self):
        """Analyze all documents and update their tiers"""
        documents = self.db.query(Document).filter(
            Document.is_duplicate == False
        ).all()
        
        for doc in documents:
            new_tier = self._calculate_tier(doc)
            if new_tier != doc.tier:
                doc.tier = new_tier
        
        self.db.commit()
    
    def _calculate_tier(self, document) -> str:
        """Calculate appropriate tier for a document"""
        score = self._calculate_importance_score(document)
        
        if score >= 80:
            return "hot"
        elif score >= 60:
            return "warm"
        elif score >= 30:
            return "cold"
        else:
            return "archive"
    
    def _calculate_importance_score(self, document) -> float:
        """Calculate importance score from 0-100"""
        score = 0.0
        
        days_since_access = (datetime.utcnow() - document.last_accessed).days
        recency_score = max(0, 100 - (days_since_access * 2))
        score += recency_score * 0.4
        
        if document.access_count > 0:
            frequency_score = min(100, document.access_count * 10)
        else:
            frequency_score = 0
        score += frequency_score * 0.3
        
        type_score = self._get_file_type_score(document.file_type)
        score += type_score * 0.2
        
        if document.original_size < 1_000_000:  # < 1MB
            size_score = 80
        elif document.original_size < 10_000_000:  # < 10MB
            size_score = 50
        else:
            size_score = 20
        score += size_score * 0.1
        
        return min(100, score)
    
    def _get_file_type_score(self, file_type: str) -> float:
        """Get importance score based on file type"""
        type_scores = {
            'pdf': 90,    # Important documents
            'docx': 85,   # Editable documents
            'jpg': 60,    # Images
            'png': 60,    # Images
            'txt': 40,    # Plain text
            'other': 30   # Others
        }
        return type_scores.get(file_type, 30)
    
    def apply_tier_policies(self):
        """Apply compression based on tier"""
        documents = self.db.query(Document).all()
        
        for doc in documents:
            if doc.tier == "archive" and not doc.is_duplicate:
                self._compress_for_archive(doc)
    
    def _compress_for_archive(self, document):
        """Apply additional compression for archive tier"""
        pass