# imports for vector embeddings and similarity search
import numpy as np
import faiss
# from sentence_transformers import SentenceTransformer  # commented out - causing issues
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbedStore:
    """
    a vector embedding store that uses faiss for fast similarity search.
    stores text chunks as embeddings and allows semantic search through them.
    optimized for individual searches with model caching.
    """
    _instance = None
    
    def __init__(self, dim=1000, index_path="faiss.index", meta_path="faiss_meta.pkl"):
        # basic setup - using TF-IDF instead of sentence transformers
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path
        # use TF-IDF instead of sentence transformers (no lzma dependency)
        self._vectorizer = None
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
    def get_instance(cls, dim=1000, index_path="faiss.index", meta_path="faiss_meta.pkl"):
        """get singleton instance for reuse across searches"""
        if cls._instance is None:
            cls._instance = cls(dim, index_path, meta_path)
        return cls._instance
    
    @property
    def vectorizer(self):
        """lazy load the TF-IDF vectorizer"""
        if self._vectorizer is None:
            self._vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        return self._vectorizer
    
    def embed_texts(self, texts):
        """convert text to vector embeddings using TF-IDF"""
        if not hasattr(self, '_fitted') or not self._fitted:
            # fit on all texts first time
            all_texts = self.metadata + texts if self.metadata else texts
            vectors = self.vectorizer.fit_transform(all_texts).toarray()
            self._fitted = True
            # return only the new text vectors
            if self.metadata:
                return vectors[-len(texts):]
            return vectors
        else:
            # transform new texts using existing vocabulary
            return self.vectorizer.transform(texts).toarray()
    
    def add_texts(self, texts, save=True):
        """add new texts to the vector store"""
        vectors = self.embed_texts(texts)
        
        # create index with correct dimensions based on actual vector size
        if self.index is None or self.index.d != vectors.shape[1]:
            self.dim = vectors.shape[1]  # update dimension to match vectors
            self.index = faiss.IndexFlatL2(self.dim)
            print(f"Created new FAISS index with dimension: {self.dim}")
        
        # add vectors to faiss index and store original texts
        self.index.add(np.array(vectors).astype('float32'))
        self.metadata.extend(texts)
        if save:
            self.save_index()
    
    def save_index(self):
        # persist the faiss index and metadata to disk
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump({
                'metadata': self.metadata,
                'dim': self.dim,
                'vectorizer': self._vectorizer,
                'fitted': getattr(self, '_fitted', False)
            }, f)
    
    def load_index(self):
        # load existing faiss index and metadata from disk
        self.index = faiss.read_index(self.index_path)
        self.dim = self.index.d  # update dimension from loaded index
        with open(self.meta_path, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                self.metadata = data.get('metadata', [])
                self._vectorizer = data.get('vectorizer')
                self._fitted = data.get('fitted', False)
            else:
                # old format - just metadata list
                self.metadata = data
                self._fitted = False
    
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
        
        # debug dimension mismatch
        print(f"Index dimension: {self.index.d}")
        print(f"Query vector shape: {query_vector.shape}")
        print(f"Query vector dimension: {query_vector.shape[1] if query_vector.ndim > 1 else query_vector.shape[0]}")
        
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