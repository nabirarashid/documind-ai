import chromadb
from sentence_transformers import SentenceTransformer
import os

class EmbedStore:
    _instance = None

    def __init__(self, persist_dir="chroma_store"):
        # Updated client initialization for new ChromaDB
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="docs")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_texts(self, texts):
        embeddings = self.model.encode(texts).tolist()
        # Get current count for ID generation
        current_count = self.collection.count()
        ids = [f"doc-{i}" for i in range(current_count, current_count + len(texts))]
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids)

    def search(self, query, top_k=5):
        """Legacy search method for backward compatibility"""
        query_vec = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[query_vec], n_results=top_k)
        return results["documents"][0]
    
    def search_with_metadata(self, query, top_k=5):
        """Enhanced search that returns content with metadata structure"""
        query_vec = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[query_vec], n_results=top_k)
        
        # Transform results to include metadata structure
        search_results = []
        if results["documents"] and len(results["documents"]) > 0:
            documents = results["documents"][0]
            ids = results["ids"][0] if results["ids"] else []
            distances = results["distances"][0] if results["distances"] else []
            
            for i, doc in enumerate(documents):
                result = {
                    "content": doc,
                    "id": ids[i] if i < len(ids) else f"doc-{i}",
                    "distance": distances[i] if i < len(distances) else 0,
                }
                search_results.append(result)
        
        return search_results