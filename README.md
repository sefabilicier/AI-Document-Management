# AI-Powered Document Management System

https://img.shields.io/badge/DocSlim-Data%2520Reduction-blue
https://img.shields.io/badge/Python-3.8+-green
https://img.shields.io/badge/FastAPI-0.104+-brightgreen
https://img.shields.io/badge/React-18.2-blue

This project is an intelligent document management system that demonstrates real-time **data reduction** techniques including **deduplication**, **compression**, and **intelligent tiering**. This project showcases how organizations can significantly **reduce storage costs** while maintaining data accessibility.

### UI

<img width="1589" height="955" alt="Image" src="https://github.com/user-attachments/assets/1d2594ad-3897-46df-a274-7c0bf3f0df80" />


### Prerequisites
- Python 3.8+
- Node.js 14+ (for React frontend)
- SQLite

1. Clone & Setup
```bash
# Clone repository
git clone https://github.com/yourusername/docslim.git
cd docslim

# Set up backend
cd backend
pip install -r requirements.txt

# Set up frontend
cd ../frontend
npm install
```

2. Start Backend Server
```bash
cd backend
python -m app.main
Backend will start at: http://localhost:8000
API Documentation: http://localhost:8000/docs
```
3. Start Frontend Server
```bash
cd frontend
npm start
Frontend will start at: http://localhost:3000
```


### Project Structure
```text
docslim/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── document_service.py     # Core processing
│   │   │   └── embedding_service.py    # AI similarity detection
│   │   └── utils/          # Utility functions
│   │       ├── file_utils.py           # File operations
│   │       └── optimizers.py           # Compression algorithms
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   └── App.css        # Styles
│   ├── public/
│   └── package.json
│
├── demo_files/            # Sample documents for demonstration
├── docker-compose.yml     # Docker orchestration
└── README.md             # This file
```

### How It Works
Data Reduction Pipeline

<img width="1266" height="1009" alt="Image" src="https://github.com/user-attachments/assets/ed0589df-bbfd-4f6b-b40b-510c8abd5307" />


### Technical Implementation
1. Duplicate Detection
```python
# Three levels of duplicate detection
def detect_duplicates(file):
    # 1. Exact hash match (MD5)
    # 2. Content similarity (text embeddings)
    # 3. Fuzzy matching (filename, size, type)
    return duplicate_type
```

2. Smart Compression
- PDFs: Image compression + metadata removal
- Images: Quality optimization + format conversion
- Documents: Style cleanup + redundant data removal
- Text: Efficient encoding

3. Intelligent Tiering
```python
def assign_tier(document):
    score = (recency * 0.4 + 
             frequency * 0.3 + 
             type_importance * 0.2 + 
             size_factor * 0.1)
    
    if score >= 80: return "hot"    # Frequently accessed
    elif score >= 60: return "warm" # Occasionally accessed
    else: return "cold"             # Rarely accessed
```

Performance Metrics
<img width="1800" height="639" alt="Image" src="https://github.com/user-attachments/assets/192ffc64-ec84-4163-b1eb-c56f5dd5dc2a" />

Demo Results
```text
Uploaded: 100 documents, 2.5 GB
After Processing: 100 documents, 1.1 GB
Total Savings: 1.4 GB (56%)
Duplicates Found: 15 (15% reduction)
Monthly Cost: $55 → $24 (56% savings)
```

🎯 Use Cases
Enterprise Document Management
- Problem: 10,000+ documents, 500GB storage, high costs
- Solution: DocSlim reduces to 200GB, saving $6,000/year
- Features Used: Deduplication, tiering, compression

Legal Firm Compliance
- Problem: Multiple versions of contracts, audit trails needed
- Solution: Version tracking + deduplication saves 70% storage
- Features Used: Content similarity, version control

Healthcare Records
- Problem: Scanned documents, HIPAA compliance, large files
- Solution: OCR + compression reduces storage by 80%
- Features Used: Image optimization, secure storage