# app/rag/service.py
import logging
import os
import pickle

import faiss

logger = logging.getLogger(__name__)


class RAGService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_loaded") and self._loaded:
            return

        self.model = None
        self.index = None
        self.metadata = []
        self._loaded = False
        self._load_all()

    # app/rag/service.py

    def _load_all(self):
        try:
            print("📚 Loading RAG Service...")

            self._load_model()
            self._load_faiss_index()
            self._load_metadata()

            self._loaded = True
            print("✅ RAG Service ready!")

        except Exception as e:
            print(f"❌ RAG Error: {e}")
            self._loaded = False

    def _load_model(self):
        from sentence_transformers import SentenceTransformer

        """Load sentence transformer model"""
        self.model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        print("   ✅ Model loaded from cache")

    def _load_faiss_index(self):
        """Load FAISS index"""
        if os.path.exists("models/faq_index.faiss"):
            self.index = faiss.read_index("models/faq_index.faiss")
            print(f"   ✅ FAISS loaded: {self.index.ntotal} vectors")

    def _load_metadata(self):
        """Load FAQ metadata"""
        if os.path.exists("models/faq_metadata.pkl"):
            with open("models/faq_metadata.pkl", "rb") as f:
                self.metadata = pickle.load(f)
            print(f"   ✅ Metadata loaded: {len(self.metadata)} FAQs")

    def retrieve(self, query, k=2, threshold=0.1):
        if not self._loaded:
            print("⚠️ RAG Service not loaded, returning empty results")
            return []

        if self.model is None or self.index is None or len(self.metadata) == 0:
            print("⚠️ RAG components missing, returning empty results")
            return []

        try:
            q_emb = self.model.encode([query], normalize_embeddings=True)
            distances, indices = self.index.search(q_emb.astype("float32"), k)

            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata):
                    sim = float(distances[0][i])
                    if sim >= threshold:
                        results.append(
                            {
                                "question": self.metadata[idx].get("question", ""),
                                "answer": self.metadata[idx].get("answer", ""),
                                "category": self.metadata[idx].get("category", "general"),
                                "domain": self.metadata[idx].get("domain", "General"),
                                "similarity": sim,
                            }
                        )
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
