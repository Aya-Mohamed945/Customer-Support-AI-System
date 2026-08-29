# app/ml/pipeline.py
"""
ML Pipeline - Updated with Priority Model (20 Clusters) + RAG Integration (via requests)
"""

import logging
from typing import Any, Dict, Optional

import numpy as np
import requests

logger = logging.getLogger(__name__)


# Lazy imports
def _get_model_manager():
    from app.core.dependencies import get_model_manager

    return get_model_manager()


def _preprocess_text(text):
    from app.ml.preprocessing import preprocess_text

    return preprocess_text(text)


class PredictionPipeline:
    """Complete ML prediction pipeline with RAG integration (via requests)"""

    def __init__(self):
        self.model_manager = _get_model_manager()
        self._load_components()
        self.rag_url = "http://127.0.0.1:8001"  # RAG Service URL

    def _load_components(self):
        """Load all ML components"""
        try:
            # Category
            self.cat_model = self.model_manager.get_model("category", "model")
            self.cat_vectorizer = self.model_manager.get_model("category", "vectorizer")
            self.cat_encoder = self.model_manager.get_model("category", "encoder")

            # Priority (20 Clusters, 98.84% CV Accuracy)
            self.pri_model = self.model_manager.get_model("priority", "model")
            self.pri_vectorizer = self.model_manager.get_model("priority", "vectorizer")
            self.pri_encoder = self.model_manager.get_model("priority", "encoder")

            # Sentiment (4 Classes)
            self.sen_model = self.model_manager.get_model("sentiment", "model")
            self.sen_vectorizer = self.model_manager.get_model("sentiment", "vectorizer")
            self.sen_encoder = self.model_manager.get_model("sentiment", "encoder")

            logger.info("✅ All models loaded (Priority: 98.84% CV, 20 Clusters)")

        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            raise

    def _get_rag_results(self, query: str, k: int = 3, threshold: float = 0.25) -> list:
        """
        Get RAG results from external service
        """
        try:
            logger.info(f"🔍 Calling RAG service with query: {query[:80]}...")
            response = requests.post(
                f"{self.rag_url}/api/v1/rag/retrieve", json={"query": query, "k": k, "threshold": threshold}, timeout=5
            )
            logger.info(f"📡 RAG response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                logger.info(f"✅ RAG returned {len(results)} results")
                return results
            else:
                logger.warning(f"⚠️ RAG service returned status {response.status_code}")
                return []

        except requests.exceptions.ConnectionError:
            logger.error("❌ RAG service not available (connection refused)")
            return []
        except requests.exceptions.Timeout:
            logger.error("❌ RAG service timeout")
            return []
        except Exception as e:
            logger.error(f"❌ RAG error: {e}")
            return []

    # app/ml/pipeline.py

    def predict(self, title: str, description: str, resolution_time: Optional[float] = None) -> Dict[str, Any]:
        """Complete prediction pipeline with RAG"""
        try:
            # Combine and preprocess text
            full_text = f"{title} {description}"
            processed_text = _preprocess_text(full_text)

            # ===== CATEGORY =====
            category = self._predict_category(processed_text)

            # ===== PRIORITY =====
            priority, pri_confidence = self._predict_priority(processed_text)

            # ===== SENTIMENT =====
            sentiment = self._predict_sentiment(processed_text)

            # ===== RULE-BASED OVERRIDE =====
            category, priority, sentiment = self._apply_rule_overrides(full_text, category, priority, sentiment)

            # ===== RAG =====
            rag_results, suggested_solution, source, rag_confidence = self._get_rag_solution(full_text)

            return {
                "category": category,
                "priority": priority,
                "priority_confidence": pri_confidence,
                "sentiment": sentiment,
                "suggested_solution": suggested_solution,
                "source": source,
                "rag_confidence": rag_confidence,
                "rag_results": rag_results,
            }

        except Exception as e:
            logger.error(f"Prediction pipeline error: {e}")
            import traceback

            traceback.print_exc()
            return self._fallback_response()

    def _predict_category(self, processed_text: str) -> str:
        """Predict category"""
        try:
            cat_features = self.cat_vectorizer.transform([processed_text])
            cat_pred = self.cat_model.predict(cat_features)[0]
            return self.cat_encoder.inverse_transform([cat_pred])[0]
        except Exception as e:
            logger.warning(f"Category prediction error: {e}")
            return "technical"

    def _predict_priority(self, processed_text: str) -> tuple:
        """Predict priority and confidence"""
        try:
            pri_features = self.pri_vectorizer.transform([processed_text])
            pri_pred = self.pri_model.predict(pri_features)[0]
            priority = self.pri_encoder.inverse_transform([pri_pred])[0]
            try:
                pri_probs = self.pri_model.predict_proba(pri_features)
                pri_confidence = float(np.max(pri_probs))
            except Exception:
                pri_confidence = 0.5
            return priority, pri_confidence
        except Exception as e:
            logger.warning(f"Priority prediction error: {e}")
            return "medium", 0.5

    def _predict_sentiment(self, processed_text: str) -> str:
        """Predict sentiment"""
        try:
            sen_features = self.sen_vectorizer.transform([processed_text])
            sen_pred = self.sen_model.predict(sen_features)[0]
            return self.sen_encoder.inverse_transform([sen_pred])[0]
        except Exception as e:
            logger.warning(f"Sentiment prediction error: {e}")
            return "neutral"

    def _apply_rule_overrides(self, full_text: str, category: str, priority: str, sentiment: str) -> tuple:
        """Apply rule-based overrides"""
        full_text_lower = full_text.lower()

        # Dark Mode Suggestion
        if "dark mode" in full_text_lower:
            if category != "technical":
                category = "technical"
                logger.info("🔄 Override: Dark Mode category changed to technical")
            if "suggestion" in full_text_lower or "nice" in full_text_lower or "great" in full_text_lower:
                if sentiment != "neutral" and sentiment != "positive":
                    sentiment = "neutral"
                    logger.info("🔄 Override: Dark Mode sentiment changed to neutral")

        # Urgent = Angry
        if any(word in full_text_lower for word in ["urgent", "immediately", "asap", "emergency", "critical"]):
            if sentiment == "negative":
                sentiment = "angry"
                logger.info("🔄 Override: Urgent sentiment changed to angry")

        # CSV/Import Issues
        if any(word in full_text_lower for word in ["csv", "import", "bulk", "upload", "export"]):
            if category == "billing" or category == "account":
                category = "technical"
                logger.info("🔄 Override: Import/Export issue category changed to technical")
            if any(word in full_text_lower for word in ["failing", "failed", "error", "corrupt", "invalid"]):
                if priority == "Medium" or priority == "Low":
                    priority = "High"
                    logger.info("🔄 Override: Import/Export issue priority changed to High")
                if sentiment == "neutral" or sentiment == "positive":
                    sentiment = "angry"
                    logger.info("🔄 Override: Import/Export issue sentiment changed to angry")

        return category, priority, sentiment

    def _get_rag_solution(self, full_text: str) -> tuple:
        """Get RAG solution"""
        rag_results = []
        suggested_solution = "We're looking into your issue. A support agent will contact you shortly."
        source = "General"
        rag_confidence = 0.0

        try:
            rag_results = self._get_rag_results(full_text, k=2, threshold=0.1)
            logger.info(f"RAG results: {len(rag_results) if rag_results else 0}")

            if rag_results:
                suggested_solution = rag_results[0]["answer"]
                source = "FAQ"
                rag_confidence = rag_results[0]["similarity"]
                logger.info(f"✅ RAG found {len(rag_results)} results")
            else:
                logger.info("ℹ️ No RAG results found")
        except Exception as e:
            logger.warning(f"RAG retrieval error: {e}")

        return rag_results, suggested_solution, source, rag_confidence

    def _fallback_response(self) -> Dict[str, Any]:
        """Return safe fallback response"""
        return {
            "category": "technical",
            "priority": "Medium",
            "priority_confidence": 0.5,
            "sentiment": "neutral",
            "suggested_solution": "We are investigating your issue. A support agent will contact you shortly.",
            "source": "General",
            "rag_confidence": 0.0,
            "rag_results": [],
        }


# ============================================
# Singleton
# ============================================
_pipeline = None


def get_pipeline() -> PredictionPipeline:
    global _pipeline
    if _pipeline is None:
        try:
            _pipeline = PredictionPipeline()
        except Exception as e:
            logger.error(f"❌ Failed to initialize pipeline: {e}")
            _pipeline = None
    return _pipeline
