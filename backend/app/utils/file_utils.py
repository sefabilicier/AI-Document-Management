import os
import hashlib
from pathlib import Path
from typing import Optional

class FileUtils:
    def __init__(self):
        pass  # No magic initialization
    
    def detect_file_type(self, file_path: str) -> str:
        """Detect file type based on extension"""
        # Get file extension
        ext = Path(file_path).suffix.lower()
        
        # Map extensions to our file types
        extension_map = {
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.doc': 'docx',
            '.jpg': 'jpg',
            '.jpeg': 'jpg',
            '.png': 'png',
            '.tiff': 'tiff',
            '.tif': 'tiff',
            '.txt': 'txt',
            '.csv': 'csv',
            '.xlsx': 'xlsx',
            '.xls': 'xlsx',
            '.pptx': 'pptx',
            '.ppt': 'pptx'
        }
        
        return extension_map.get(ext, 'other')
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate MD5 hash of file content"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from document based on file type"""
        try:
            if file_type == 'pdf':
                return self._extract_text_from_pdf(file_path)
            elif file_type == 'docx':
                return self._extract_text_from_docx(file_path)
            elif file_type == 'txt':
                return self._extract_text_from_txt(file_path)
            else:
                return f"Content from {file_type} file"
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Simple PDF text extraction placeholder"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read(1000)
                # Try to decode as text
                try:
                    return content.decode('utf-8', errors='ignore')
                except:
                    return "Binary PDF content"
        except:
            return "PDF content"
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Simple DOCX text extraction placeholder"""
        try:
            try:
                from docx import Document as DocxDocument
                doc = DocxDocument(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                return "Word document content"
        except:
            return "Word document"
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return ""
    
    def get_file_info(self, file_path: str) -> dict:
        """Get comprehensive file information"""
        stats = os.stat(file_path)
        
        return {
            'size': stats.st_size,
            'created': stats.st_ctime,
            'modified': stats.st_mtime,
            'accessed': stats.st_atime,
        }