# app/rag/__init__.py
"""
RAG Package - Retrieval Augmented Generation
"""

from app.rag.service import RAGService, get_rag

__all__ = [
    "get_rag",
    "RAGService",
]
