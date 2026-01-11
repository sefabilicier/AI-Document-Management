import fitz
import os

class PDFOptimizer:
    def optimize(self, input_path: str, output_path: str) -> int:
        """Optimize PDF by compressing images and cleaning up"""
        try:
            doc = fitz.open(input_path)
            
            doc.save(output_path, 
                    garbage=4,    # Remove unused objects
                    deflate=True,  # Compress streams
                    clean=True)    # Clean document
            doc.close()
            
            optimized_size = os.path.getsize(output_path)
            print(f"PDF optimized: {os.path.getsize(input_path)} → {optimized_size} bytes")
            
            return optimized_size
        except Exception as e:
            print(f"PDF optimization failed, using copy: {e}")
            import shutil
            shutil.copy2(input_path, output_path)
            return os.path.getsize(output_path)