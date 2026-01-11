from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from app.database import get_db, init_db
from app.models import Document
from app.schemas import DocumentCreate, DocumentResponse
from app.services.document_service import DocumentService

app = FastAPI(title="DocSlim - AI Document Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/optimized", exist_ok=True)
    os.makedirs("uploads/thumbnails", exist_ok=True)
    os.makedirs("uploads/temp", exist_ok=True)
    
    from app.database import init_db, engine
    from app.models import Base
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

@app.get("/")
def read_root():
    return {"message": "DocSlim API is running"}

@app.post("/upload/", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document for processing and reduction"""
    document_service = DocumentService(db)
    
    try:
        temp_path = f"uploads/temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        document = await document_service.process_document(temp_path, file.filename)
        
        os.remove(temp_path)
        
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of all documents"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@app.get("/stats/")
def get_stats(db: Session = Depends(get_db)):
    """Get storage statistics"""
    from sqlalchemy import func
    
    total_docs = db.query(func.count(Document.id)).scalar()
    total_original = db.query(func.sum(Document.original_size)).scalar() or 0
    total_optimized = db.query(func.sum(Document.optimized_size)).scalar() or 0
    
    return {
        "total_documents": total_docs,
        "total_original_size": total_original,
        "total_optimized_size": total_optimized,
        "total_savings": total_original - total_optimized,
        "savings_percentage": ((total_original - total_optimized) / total_original * 100) if total_original > 0 else 0
    }
    
@app.get("/metrics/daily")
def get_daily_metrics(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get daily metrics for dashboard"""
    from app.services.metrics_service import MetricsService
    
    metrics_service = MetricsService(db)
    return metrics_service.get_savings_trend(days)

@app.get("/metrics/breakdown")
def get_breakdown(db: Session = Depends(get_db)):
    """Get breakdown by file type"""
    from app.services.metrics_service import MetricsService
    
    metrics_service = MetricsService(db)
    return metrics_service.get_file_type_breakdown()

@app.get("/documents/search")
def search_documents(
    query: str,
    db: Session = Depends(get_db)
):
    """Search documents by content"""
    from app.models import Document
    
    # Simple text search for now
    documents = db.query(Document).filter(
        Document.extracted_text.ilike(f"%{query}%"),
        Document.is_duplicate == False
    ).limit(50).all()
    
    return documents

@app.get("/metrics/daily")
def get_daily_metrics(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get daily metrics for dashboard"""
    from app.services.metrics_service import MetricsService
    
    metrics_service = MetricsService(db)
    return metrics_service.get_savings_trend(days)

@app.get("/metrics/breakdown")
def get_breakdown(db: Session = Depends(get_db)):
    """Get breakdown by file type"""
    from app.services.metrics_service import MetricsService
    
    metrics_service = MetricsService(db)
    return metrics_service.get_file_type_breakdown()

@app.get("/documents/search")
def search_documents(
    query: str,
    db: Session = Depends(get_db)
):
    """Search documents by content"""
    from app.models import Document
    
    documents = db.query(Document).filter(
        Document.extracted_text.ilike(f"%{query}%"),
        Document.is_duplicate == False
    ).limit(50).all()
    
    return documents

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)