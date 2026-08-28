# app/rag/api.py
"""
RAG API Service - Microservice for FAQ Retrieval
"""

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from typing import Optional, List
import sys
import os
import uvicorn

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.rag.service import get_rag

# ============================================
# Router
# ============================================
router = APIRouter()

print("=" * 60)
print("📚 Loading RAG Service...")
print("=" * 60)

RAG_READY = False
rag_service = None

try:
    rag_service = get_rag()
    # ✅ التحقق من أن rag_service ليس None وله attribute metadata
    if rag_service is not None and hasattr(rag_service, 'metadata'):
        RAG_READY = True
        print(f"✅ RAG Service ready! {len(rag_service.metadata)} FAQs loaded")
    else:
        print("⚠️ RAG Service returned None or missing metadata")
        RAG_READY = False
except Exception as e:
    print(f"❌ RAG Service failed: {e}")
    import traceback
    traceback.print_exc()
    RAG_READY = False

# ============================================
# Models
# ============================================

class RAGRequest(BaseModel):
    """Request model for RAG retrieval"""
    query: str
    k: Optional[int] = 2
    threshold: Optional[float] = 0.1

class RAGResponse(BaseModel):
    """Response model for RAG retrieval"""
    results: List[dict]

# ============================================
# Endpoints
# ============================================

@router.get("/health")
async def rag_health():
    """Health check endpoint for RAG service"""
    return {
        "status": "healthy" if RAG_READY else "degraded",
        "rag_ready": RAG_READY,
        "faqs": len(rag_service.metadata) if rag_service and hasattr(rag_service, 'metadata') else 0
    }

@router.post("/retrieve", response_model=RAGResponse)
async def retrieve(request: RAGRequest):
    """
    Retrieve relevant FAQs for a query using semantic search.
    
    Args:
        request: Query with k (number of results) and threshold
        
    Returns:
        List of relevant FAQ entries with similarity scores
    """
    if not RAG_READY or rag_service is None:
        return {"results": []}
    
    results = rag_service.retrieve(
        request.query,
        k=request.k,
        threshold=request.threshold
    )
    return {"results": results}

# ============================================
# FastAPI App
# ============================================

app = FastAPI(
    title="RAG Service",
    version="1.0.0",
    description="FAQ Retrieval Service using Sentence Transformers + FAISS"
)

app.include_router(router, prefix="/api/v1/rag")

# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    uvicorn.run(
        "app.rag.api:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )