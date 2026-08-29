# app/core/__init__.py
"""
Core Package - Configuration & Dependencies
"""

from app.core.config import settings
from app.core.dependencies import (
    create_access_token,
    get_current_user,
    get_model_manager,
    get_priority_encoder,
    get_priority_model,
    get_priority_vectorizer,
    get_sentiment_encoder,
    get_sentiment_model,
    get_sentiment_vectorizer,
    load_users,
    save_users,
    verify_token,
)

__all__ = [
    "settings",
    "get_model_manager",
    "get_sentiment_model",
    "get_sentiment_vectorizer",
    "get_sentiment_encoder",
    "get_priority_model",
    "get_priority_vectorizer",
    "get_priority_encoder",
    "create_access_token",
    "verify_token",
    "get_current_user",
    "load_users",
    "save_users",
]
