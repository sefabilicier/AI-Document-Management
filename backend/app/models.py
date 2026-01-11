from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    original_size = Column(Integer)  # Size in bytes
    optimized_size = Column(Integer)  # Size in bytes after reduction
    file_type = Column(String)  # pdf, docx, jpg, etc.
    upload_date = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)
    
    # Reduction info
    reduction_strategy = Column(String)
    reduction_percentage = Column(Float)  # 0.0 to 100.0
    is_duplicate = Column(Boolean, default=False)
    original_document_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    
    # Storage info
    storage_path = Column(String)
    thumbnail_path = Column(String, nullable=True)
    tier = Column(String, default="hot")  # hot, warm, cold, archive
    
    # Content info
    extracted_text = Column(Text, nullable=True)
    text_hash = Column(String, nullable=True)  # For exact duplicate detection
    embedding = Column(Text, nullable=True)  # JSON string of embedding vector
    
    # Relationships
    duplicates = relationship("Document", backref="original", remote_side=[id])
    versions = relationship("DocumentVersion", back_populates="document")

class DocumentVersion(Base):
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    version_number = Column(Integer, default=1)
    file_path = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="versions")

class StorageMetrics(Base):
    __tablename__ = "storage_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_original_size = Column(Integer, default=0)  # Bytes
    total_optimized_size = Column(Integer, default=0)  # Bytes
    total_documents = Column(Integer, default=0)
    total_duplicates_found = Column(Integer, default=0)
    
    # By file type
    pdf_count = Column(Integer, default=0)
    docx_count = Column(Integer, default=0)
    image_count = Column(Integer, default=0)
    other_count = Column(Integer, default=0)