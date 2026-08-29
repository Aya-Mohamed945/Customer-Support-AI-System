# backend/app/api/__init__.py
"""
API Routes Package
"""

from app.api.auth import router as auth_router
from app.api.routes import router as main_router

__all__ = [
    "main_router",
    "auth_router",
]
