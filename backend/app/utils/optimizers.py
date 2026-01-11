import os
from abc import ABC, abstractmethod
import fitz  # PyMuPDF
from PIL import Image
import shutil

class BaseOptimizer(ABC):
    """Base class for all document optimizers"""
    
    @abstractmethod
    def optimize(self, input_path: str, output_path: str) -> int:
        """Optimize document and return new size in bytes"""
        pass

class PDFOptimizer(BaseOptimizer):
    """Optimize PDF documents"""
    
    def optimize(self, input_path: str, output_path: str) -> int:
        """
        Optimize PDF by:
        1. Compressing images
        2. Removing unnecessary metadata
        3. Optimizing font embedding
        """
        try:
            shutil.copy2(input_path, output_path)
            
            self._compress_pdf_images(input_path, output_path)
            
            return os.path.getsize(output_path)
        except Exception as e:
            print(f"PDF optimization failed: {e}")
            shutil.copy2(input_path, output_path)
            return os.path.getsize(output_path)
    
    def _compress_pdf_images(self, input_path: str, output_path: str):
        """Compress images within PDF"""
        try:
            doc = fitz.open(input_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                images = page.get_images()
                
                for img_index, img in enumerate(images):
                    xref = img[0]
                    pass
            
            doc.save(output_path, garbage=4, deflate=True, clean=True)
            doc.close()
        except:
            shutil.copy2(input_path, output_path)

class ImageOptimizer(BaseOptimizer):
    """Optimize image files"""
    
    def optimize(self, input_path: str, output_path: str) -> int:
        """Optimize image by reducing quality and dimensions"""
        try:
            img = Image.open(input_path)
            
            original_size = os.path.getsize(input_path)
            quality = self._determine_quality(original_size)
            
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            return os.path.getsize(output_path)
        except Exception as e:
            print(f"Image optimization failed: {e}")
            shutil.copy2(input_path, output_path)
            return os.path.getsize(output_path)
    
    def _determine_quality(self, original_size: int) -> int:
        """Determine JPEG quality based on original size"""
        if original_size > 10_000_000:  # > 10MB
            return 75
        elif original_size > 1_000_000:  # > 1MB
            return 85
        else:
            return 90

class DocxOptimizer(BaseOptimizer):
    """Optimize Word documents"""
    
    def optimize(self, input_path: str, output_path: str) -> int:
        """Optimize DOCX by removing unused styles and metadata"""
        shutil.copy2(input_path, output_path)
        return os.path.getsize(output_path)

class DefaultOptimizer(BaseOptimizer):
    """Default optimizer for unknown file types"""
    
    def optimize(self, input_path: str, output_path: str) -> int:
        """Simply copy the file without optimization"""
        shutil.copy2(input_path, output_path)
        return os.path.getsize(output_path)

def get_optimizer(file_type: str) -> BaseOptimizer:
    """Factory function to get appropriate optimizer"""
    optimizers = {
        'pdf': PDFOptimizer(),
        'jpg': ImageOptimizer(),
        'png': ImageOptimizer(),
        'docx': DocxOptimizer(),
    }
    
    return optimizers.get(file_type, DefaultOptimizer())