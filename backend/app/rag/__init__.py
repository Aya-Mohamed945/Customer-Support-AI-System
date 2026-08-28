# app/rag/__init__.py
"""
RAG Package - Retrieval Augmented Generation
"""

from app.rag.service import get_rag, RAGService

__all__ = [
    "get_rag",
    "RAGService",
]