# imports for vector embeddings and similarity search
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
import pickle

class EmbedStore:
    """
    a vector embedding store that uses faiss for fast similarity search.
    stores text chunks as embeddings and allows semantic search through them.
    optimized for individual searches with model caching.
    """
    _instance = None
    
    def __init__(self, dim=384, index_path="faiss.index", meta_path="faiss_meta.pkl"):
        # basic setup - dimension matches the sentence transformer model
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path
        # lazy load model for better performance on individual searches
        self._model = None
        self.index = None
        self.metadata = []
        # cache for query embeddings to avoid re-computing
        self.query_cache = {}
        
        # load existing index if files exist, otherwise create new one
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.load_index()
        else:
            self.index = faiss.IndexFlatL2(self.dim)
    
    @classmethod
    def get_instance(cls, dim=384, index_path="faiss.index", meta_path="faiss_meta.pkl"):
        """get singleton instance for reuse across searches"""
        if cls._instance is None:
            cls._instance = cls(dim, index_path, meta_path)
        return cls._instance
    
    @property
    def model(self):
        """lazy load the sentence transformer model"""
        if self._model is None:
            self._model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        return self._model
    
    def embed_texts(self, texts):
        """convert text to vector embeddings using sentence transformer"""
        # disable progress bar for faster processing
        return self.model.encode(texts, show_progress_bar=False)
    
    def add_texts(self, texts, save=True):
        """add new texts to the vector store"""
        vectors = self.embed_texts(texts)
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dim)
        
        # add vectors to faiss index and store original texts
        self.index.add(np.array(vectors).astype('float32'))
        self.metadata.extend(texts)
        if save:
            self.save_index()
    
    def save_index(self):
        # persist the faiss index and metadata to disk
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
    
    def load_index(self):
        # load existing faiss index and metadata from disk
        self.index = faiss.read_index(self.index_path)
        with open(self.meta_path, "rb") as f:
            self.metadata = pickle.load(f)
    
    def search(self, query, top_k=5):
        # search for similar texts based on semantic similarity
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # check cache first to avoid re-embedding the same query
        if query in self.query_cache:
            query_vector = self.query_cache[query]
        else:
            query_vector = self.embed_texts([query]).astype('float32')
            # cache the result for future use
            self.query_cache[query] = query_vector
        
        # ensure query_vector has the right shape for FAISS
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        
        distances, indices = self.index.search(query_vector, top_k)
        
        # retrieve the original text chunks for the found indices
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata) and idx >= 0:  # Also check for negative indices
                results.append(self.metadata[idx])
        return results

if __name__ == "__main__":
    # example usage - use singleton for better performance
    store = EmbedStore.get_instance()
    test_texts = [
        "The Stripe API is organized around REST.",
        "You can use the Stripe API in test mode.",
        "The API key determines live or test mode."
    ]
    store.add_texts(test_texts)
    
    # these searches will be fast since model is already loaded
    results = store.search("How do I test Stripe API?")
    print(results)
    
    # subsequent searches reuse the same instance
    store2 = EmbedStore.get_instance()  # same instance as store
    results2 = store2.search("What about API keys?")
    print(results2)