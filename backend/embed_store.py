import chromadb
from typing import List, Dict, Any

class EmbedStore:
    _instance = None

    def __init__(self, persist_dir="chroma_store"):
        # ChromaDB client with default embeddings (no external API needed)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="docs")
        print("EmbedStore initialized with ChromaDB default embeddings")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_texts(self, texts: List[str]) -> bool:
        """Add texts using ChromaDB's built-in embeddings"""
        if not texts:
            return False
            
        # Filter valid texts
        valid_texts = [text.strip() for text in texts if text and text.strip() and len(text.strip()) > 10]
        if not valid_texts:
            return False
        
        print(f"Adding {len(valid_texts)} texts to embedding store...")
        
        try:
            # Generate IDs
            current_count = self.collection.count()
            ids = [f"doc-{current_count + i}" for i in range(len(valid_texts))]
            
            # Add documents - ChromaDB will automatically generate embeddings
            self.collection.add(
                documents=valid_texts,
                ids=ids
            )
            
            print(f"Successfully added {len(valid_texts)} texts to ChromaDB")
            return True
            
        except Exception as e:
            print(f"Error adding texts: {e}")
            return False

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Search using ChromaDB's built-in embeddings"""
        if not query or not query.strip():
            return []
            
        try:
            # Use query_texts - ChromaDB handles embedding automatically
            results = self.collection.query(
                query_texts=[query.strip()],
                n_results=top_k
            )
            return results["documents"][0] if results["documents"] else []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_with_metadata(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Enhanced search with metadata"""
        if not query or not query.strip():
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query.strip()],
                n_results=top_k
            )
            
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
            
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        try:
            count = self.collection.count()
            return {
                "document_count": count,
                "collection_name": self.collection.name,
                "embedding_type": "ChromaDB default",
                "status": "ready" if count > 0 else "empty"
            }
        except Exception as e:
            return {"status": f"error: {e}"}

    def clear_collection(self) -> bool:
        """Clear all documents"""
        try:
            all_data = self.collection.get()
            if all_data["ids"]:
                self.collection.delete(ids=all_data["ids"])
                print(f"Cleared {len(all_data['ids'])} documents")
            return True
        except Exception as e:
            print(f"Error clearing: {e}")
            return False