import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss



class EmbeddingService:
    def __init__(self, model_name: str, dimension: int):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(dimension)
        self.embedding_cache = {}

    def get_full_context(self, chunk: Dict[str, Any]) -> str:
        return f"{chunk['code']}\n{chunk['explanations']['code']}\n{chunk['explanations']['file']}\n{chunk['explanations']['pull_request']}\n{chunk['explanations']['repository']}"

    def embed_and_index_chunks(self, chunks: List[Dict[str, Any]]):
        for chunk in chunks:
            chunk_id = f"{chunk['metadata']['file']}_{chunk['metadata']['chunk_number']}"
            if chunk_id not in self.embedding_cache:
                text_to_embed = self.get_full_context(chunk)
                embedding = self.model.encode([text_to_embed])[0]
                self.embedding_cache[chunk_id] = embedding
                self.index.add(np.array([embedding]))

    def search_similar_chunks(self, query: str, k: int = 3) -> List[int]:
        query_vector = self.model.encode([query])
        D, I = self.index.search(query_vector, k)
        return I[0]