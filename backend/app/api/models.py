# app/api/models.py
from typing import List, Optional

from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    """Request model for ticket prediction"""

    title: str = Field(..., description="Ticket title", min_length=1, max_length=200)
    description: str = Field(..., description="Ticket description", min_length=1, max_length=5000)
    resolution_time: Optional[float] = Field(None, description="Resolution time in hours", ge=0, le=168)
    user_id: Optional[str] = Field(None, description="User ID")


class RAGResult(BaseModel):
    """RAG retrieval result model"""

    question: str
    answer: str
    category: str
    domain: str
    similarity: float


class PredictionResponse(BaseModel):
    """Response model for ticket prediction"""

    category: str = Field(..., description="Predicted category")
    priority: str = Field(..., description="Predicted priority")
    priority_confidence: float = Field(..., description="Confidence score for priority prediction")
    sentiment: str = Field(..., description="Predicted sentiment (4 classes: positive, neutral, negative, angry)")
    suggested_solution: str = Field(..., description="Suggested solution")
    source: str = Field(..., description="Source of the solution (FAQ/General)")
    rag_confidence: float = Field(..., description="Confidence score for RAG retrieval")
    rag_results: Optional[List[RAGResult]] = Field(None, description="Related FAQ results")
