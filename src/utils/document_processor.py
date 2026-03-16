import pandas as pd
from typing import List, Dict, Any
import numpy as np

class DocumentProcessor:
    """
    Handles document ingestion, chunking, and metadata extraction.
    Designed for scalable data processing pipelines.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Chunks the input text into smaller segments for embedding.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "page_content": chunk_text,
                "metadata": metadata or {}
            })
            start += (self.chunk_size - self.chunk_overlap)
        return chunks

    def compute_embeddings(self, chunks: List[Dict[str, Any]], embedding_model: Any) -> List[Dict[str, Any]]:
        """
        Computes embeddings for each chunk using the provided model.
        """
        for chunk in chunks:
            chunk["embedding"] = embedding_model.embed(chunk["page_content"])
        return chunks

if __name__ == "__main__":
    # Quick test
    processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    sample_text = "ELI-Core is a scalable RAG framework designed for enterprise GenAI deployment. It handles complex retrieval tasks with ease."
    processed_chunks = processor.process_text(sample_text, {"source": "test_doc"})
    print(f"Number of chunks created: {len(processed_chunks)}")
    for i, c in enumerate(processed_chunks):
        print(f"Chunk {i}: {c['page_content']}")
