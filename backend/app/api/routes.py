# app/api/routes.py
import logging
import os
import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.models import PredictionResponse, TicketRequest
from app.ml.pipeline import get_pipeline
from app.monitoring.metrics import get_metrics

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_ticket(ticket: TicketRequest):
    """
    Analyze a support ticket and return predictions
    """
    try:
        start_time = time.time()

        # ✅ جلب user_id من الـ Request
        user_id = ticket.user_id or "anonymous"

        logger.info(f"Predicting ticket for user: {user_id[:20]}...")

        pipeline = get_pipeline()
        if pipeline is None:
            raise HTTPException(status_code=503, detail="ML Pipeline not available")

        result = pipeline.predict(
            title=ticket.title, description=ticket.description, resolution_time=ticket.resolution_time
        )

        response_time_ms = (time.time() - start_time) * 1000
        metrics = get_metrics()
        ticket_id = metrics.log_prediction(
            user_id=user_id,
            title=ticket.title,
            description=ticket.description,
            category=result["category"],
            priority=result["priority"],
            sentiment=result["sentiment"],
            suggested_solution=result["suggested_solution"],
            source=result["source"],
            priority_confidence=result["priority_confidence"],
            rag_confidence=result.get("rag_confidence", 0.0),
            rag_results=result.get("rag_results", []),
            response_time_ms=response_time_ms,
        )

        logger.info(
            f"✅ Prediction complete: ticket_id={ticket_id} | "
            f"{result['category']} | {result['priority']} | {result['sentiment']}"
        )

        return PredictionResponse(
            category=result["category"],
            priority=result["priority"],
            priority_confidence=result["priority_confidence"],
            sentiment=result["sentiment"],
            suggested_solution=result["suggested_solution"],
            source=result["source"],
            rag_confidence=result.get("rag_confidence", 0.0),
            rag_results=None,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Prediction error: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# 📊 METRICS ENDPOINTS
# ============================================


@router.get("/metrics")
async def get_metrics_endpoint():
    """Get monitoring metrics for dashboard"""
    try:
        metrics = get_metrics()
        return metrics.get_summary()
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        return {
            "total_predictions": 0,
            "uptime_hours": 0,
            "priority_distribution": {},
            "sentiment_distribution": {},
            "source_distribution": {},
            "avg_priority_confidence": 0,
            "avg_rag_confidence": 0,
            "errors_count": 0,
            "last_prediction": None,
        }


@router.get("/metrics/tickets/recent")
async def get_recent_tickets(limit: int = 50, user_id: str = None):
    """Get recent tickets for a specific user"""
    try:
        metrics = get_metrics()

        # ✅ لو user_id موجود، جيب تذاكره بس
        if user_id:
            tickets = metrics.get_user_tickets(user_id, limit)
            logger.info(f"📜 Found {len(tickets)} tickets for user: {user_id[:20]}")
        else:
            tickets = metrics.get_recent_tickets(limit)
            logger.info(f"📜 Found {len(tickets)} tickets (all users)")

        return {"total": len(tickets), "tickets": tickets}
    except Exception as e:
        logger.error(f"Error fetching tickets: {e}")
        return {"total": 0, "tickets": []}


@router.get("/metrics/tickets/{ticket_id}")
async def get_ticket_by_id(ticket_id: str):
    """Get a specific ticket by ID"""
    try:
        metrics = get_metrics()
        ticket = metrics.get_prediction_by_id(ticket_id)
        if ticket:
            return ticket
        return {"error": "Ticket not found"}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}


@router.get("/metrics/export")
async def export_metrics():
    """Export all predictions as CSV"""
    try:
        metrics = get_metrics()
        filename = metrics.export_csv()
        if filename:
            return {"message": f"Exported to {filename}", "filename": filename}
        return {"message": "No data to export"}
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/download/{filename}")
async def download_export(filename: str):
    """Download exported CSV file"""
    try:
        file_path = f"./{filename}"
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="text/csv", filename=filename)
        return {"error": "File not found"}
    except Exception as e:
        logger.error(f"Download ثrror: {e}")
        return {"error": str(e)}
