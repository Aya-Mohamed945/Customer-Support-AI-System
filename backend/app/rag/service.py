# app/rag/service.py
import pickle
import numpy as np
import faiss
import os
import time
import logging

logger = logging.getLogger(__name__)

class RAGService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_loaded') and self._loaded:
            return
        
        self.model = None
        self.index = None
        self.metadata = []
        self._loaded = False
        self._load_all()
    
    def _load_all(self):
        try:
            from sentence_transformers import SentenceTransformer
            
            print("📚 Loading RAG Service...")
            
            # Load model
            try:
                self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
                print("   ✅ Model loaded from cache")
            except Exception as e:
                print(f"   ⚠️ Failed to load primary model: {e}")
                try:
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                    print("   ✅ Fallback model loaded")
                except Exception as e2:
                    print(f"   ❌ Failed to load fallback model: {e2}")
                    self.model = None
            
            # Load FAISS index
            if os.path.exists("models/faq_index.faiss"):
                try:
                    self.index = faiss.read_index("models/faq_index.faiss")
                    print(f"   ✅ FAISS loaded: {self.index.ntotal} vectors")
                except Exception as e:
                    print(f"   ❌ Failed to load FAISS index: {e}")
                    self.index = None
            else:
                print("   ⚠️ FAISS index not found at models/faq_index.faiss")
                # Try alternative path
                if os.path.exists("models/faq_index_optimized.faiss"):
                    try:
                        self.index = faiss.read_index("models/faq_index_optimized.faiss")
                        print(f"   ✅ FAISS loaded (optimized): {self.index.ntotal} vectors")
                    except Exception as e:
                        print(f"   ❌ Failed to load FAISS index: {e}")
                        self.index = None
                else:
                    self.index = None
            
            # Load metadata
            if os.path.exists("models/faq_metadata.pkl"):
                try:
                    with open("models/faq_metadata.pkl", 'rb') as f:
                        self.metadata = pickle.load(f)
                    print(f"   ✅ Metadata loaded: {len(self.metadata)} FAQs")
                except Exception as e:
                    print(f"   ❌ Failed to load metadata: {e}")
                    self.metadata = []
            else:
                print("   ⚠️ Metadata not found at models/faq_metadata.pkl")
                self.metadata = []
            
            # Check if everything loaded properly
            if self.model is not None and self.index is not None and len(self.metadata) > 0:
                self._loaded = True
                print("✅ RAG Service ready!")
            else:
                print("⚠️ RAG Service loaded with errors (some components missing)")
                # Still mark as loaded if we have at least model and index
                if self.model is not None and self.index is not None:
                    self._loaded = True
                else:
                    self._loaded = False
            
        except Exception as e:
            print(f"❌ RAG Error: {e}")
            import traceback
            traceback.print_exc()
            self._loaded = False
    
    def retrieve(self, query, k=2, threshold=0.1):
        if not self._loaded:
            print("⚠️ RAG Service not loaded, returning empty results")
            return []
        
        if self.model is None or self.index is None or len(self.metadata) == 0:
            print("⚠️ RAG components missing, returning empty results")
            return []
        
        try:
            q_emb = self.model.encode([query], normalize_embeddings=True)
            distances, indices = self.index.search(q_emb.astype('float32'), k)
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata):
                    sim = float(distances[0][i])
                    if sim >= threshold:
                        results.append({
                            'question': self.metadata[idx].get('question', ''),
                            'answer': self.metadata[idx].get('answer', ''),
                            'category': self.metadata[idx].get('category', 'general'),
                            'domain': self.metadata[idx].get('domain', 'General'),
                            'similarity': sim
                        })
            return results
        except Exception as e:
            print(f"❌ RAG retrieval error: {e}")
            return []


_rag = None

def get_rag():
    """Get singleton RAG service instance"""
    global _rag
    if _rag is None:
        try:
            _rag = RAGService()
        except Exception as e:
            print(f"❌ Failed to create RAG service: {e}")
            # Create a dummy instance with _loaded = False
            _rag = RAGService.__new__(RAGService)
            _rag._loaded = False
            _rag.model = None
            _rag.index = None
            _rag.metadata = []
    return _rag  