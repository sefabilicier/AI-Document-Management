from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    original_filename: str
    file_type: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    original_size: int
    optimized_size: int
    reduction_percentage: float
    upload_date: datetime
    tier: str
    is_duplicate: bool
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_documents: int
    total_original_size: int
    total_optimized_size: int
    total_savings: int
    savings_percentage: float