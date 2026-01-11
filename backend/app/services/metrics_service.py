from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import StorageMetrics

class MetricsService:
    def __init__(self, db: Session):
        self.db = db
    
    def update_daily_metrics(self):
        """Update daily storage metrics"""
        from app.models import Document
        
        today = datetime.utcnow().date()
        
        # Check if metrics already exist for today
        existing = self.db.query(StorageMetrics).filter(
            func.date(StorageMetrics.date) == today
        ).first()
        
        if existing:
            return existing
        
        # Calculate metrics
        total_docs = self.db.query(func.count(Document.id)).scalar()
        total_original = self.db.query(func.sum(Document.original_size)).scalar() or 0
        total_optimized = self.db.query(func.sum(Document.optimized_size)).scalar() or 0
        
        # Count by file type
        pdf_count = self.db.query(func.count(Document.id)).filter(
            Document.file_type == 'pdf'
        ).scalar()
        
        docx_count = self.db.query(func.count(Document.id)).filter(
            Document.file_type == 'docx'
        ).scalar()
        
        image_count = self.db.query(func.count(Document.id)).filter(
            Document.file_type.in_(['jpg', 'png', 'tiff'])
        ).scalar()
        
        other_count = total_docs - (pdf_count + docx_count + image_count)
        
        # Create new metrics record
        metrics = StorageMetrics(
            date=datetime.utcnow(),
            total_documents=total_docs,
            total_original_size=total_original,
            total_optimized_size=total_optimized,
            pdf_count=pdf_count,
            docx_count=docx_count,
            image_count=image_count,
            other_count=other_count
        )
        
        self.db.add(metrics)
        self.db.commit()
        
        return metrics
    
    def get_savings_trend(self, days: int = 30):
        """Get savings trend over time"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        metrics = self.db.query(StorageMetrics).filter(
            StorageMetrics.date >= start_date
        ).order_by(StorageMetrics.date).all()
        
        trend_data = []
        for metric in metrics:
            savings = metric.total_original_size - metric.total_optimized_size
            savings_percent = (savings / metric.total_original_size * 100) if metric.total_original_size > 0 else 0
            
            trend_data.append({
                'date': metric.date.isoformat(),
                'original_size': metric.total_original_size,
                'optimized_size': metric.total_optimized_size,
                'savings': savings,
                'savings_percent': savings_percent,
                'document_count': metric.total_documents
            })
        
        return trend_data
    
    def get_file_type_breakdown(self):
        """Get breakdown by file type"""
        from app.models import Document
        from sqlalchemy import func
        
        result = self.db.query(
            Document.file_type,
            func.count(Document.id).label('count'),
            func.sum(Document.original_size).label('total_original'),
            func.sum(Document.optimized_size).label('total_optimized')
        ).group_by(Document.file_type).all()
        
        breakdown = []
        for row in result:
            savings = row.total_original - row.total_optimized
            savings_percent = (savings / row.total_original * 100) if row.total_original > 0 else 0
            
            breakdown.append({
                'file_type': row.file_type or 'unknown',
                'count': row.count,
                'original_size': row.total_original,
                'optimized_size': row.total_optimized,
                'savings': savings,
                'savings_percent': savings_percent
            })
        
        return breakdown