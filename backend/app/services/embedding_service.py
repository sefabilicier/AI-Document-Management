from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import json

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = 384  # Dimension of this model's embeddings
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        if not text or len(text.strip()) == 0:
            return [0.0] * self.embedding_dim
        
        text_chunk = text[:10000]  # First 10k characters
        embedding = self.model.encode(text_chunk)
        return embedding.tolist()
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        if not embedding1 or not embedding2:
            return 0.0
        
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return float(similarity)
    
    def embeddings_to_json(self, embedding: List[float]) -> str:
        """Convert embedding list to JSON string for database storage"""
        return json.dumps(embedding)
    
    def json_to_embeddings(self, json_str: str) -> List[float]:
        """Convert JSON string back to embedding list"""
        if not json_str:
            return []
        return json.loads(json_str)