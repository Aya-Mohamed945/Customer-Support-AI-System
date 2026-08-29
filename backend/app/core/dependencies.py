# app/core/dependencies.py
"""
Model Manager - Professional model loading with version compatibility
Updated: Priority Model with 98.84% CV Accuracy (20 Clusters)
"""

import json
import logging
import os
import pickle
import sys
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Dict, Optional

import joblib
import jwt
import numpy as np
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security = HTTPBearer()

if not hasattr(np, "_core"):
    np._core = np.core
if "numpy._core" not in sys.modules:
    sys.modules["numpy._core"] = np.core
if "numpy.core" not in sys.modules:
    sys.modules["numpy.core"] = np.core

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Professional Model Manager with:
    - Version compatibility handling
    - Lazy loading
    - Error recovery
    - Model registry
    - Type safety
    """

    _instance: Optional["ModelManager"] = None
    _models: Dict[str, Any] = {}
    _loaded: bool = False
    _model_registry: Dict[str, Dict] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._loaded:
            self._register_models()
            self._load_models()
            self._loaded = True

    def _register_models(self):
        """Register all models with metadata - Updated with new Priority (20 Clusters)"""
        self._model_registry = {
            "sentiment": {
                "model_file": "sentiment_model_final.pkl",
                "vectorizer_file": "sentiment_vectorizer_final.pkl",
                "encoder_file": "sentiment_encoder.pkl",
                "classes": ["positive", "neutral", "negative", "angry"],
                "fallback_encoder": True,
            },
            "category": {
                "model_file": "category_model_final.pkl",
                "vectorizer_file": "category_vectorizer_final.pkl",
                "encoder_file": "category_encoder.pkl",
                "fallback_encoder": False,
            },
            "priority": {
                "model_file": "priority_model_final.pkl",
                "vectorizer_file": "priority_vectorizer_final.pkl",
                "encoder_file": "priority_encoder.pkl",
                "classes": ["High", "Low", "Medium"],
                "fallback_encoder": False,
                "description": "20 Clusters, 98.84% CV Accuracy",
            },
        }
        logger.info(f"📋 Registered {len(self._model_registry)} models")

    def _find_file(self, directory: str, filename: str) -> Optional[str]:
        """Find a file by trying different extensions and paths"""
        exact_path = os.path.join(directory, filename)
        if os.path.exists(exact_path):
            return exact_path

        base, ext = os.path.splitext(filename)
        for test_ext in [".pkl", ".joblib", ".pickle"]:
            if test_ext == ext:
                continue
            test_path = os.path.join(directory, base + test_ext)
            if os.path.exists(test_path):
                logger.info(f"   Found {filename} as {base + test_ext}")
                return test_path

        return None

    def _load_single_model(self, model_key: str, config: Dict) -> Dict:
        """Load a single model with all its components"""
        result = {"model": None, "vectorizer": None, "encoder": None}
        models_dir = "./models"

        try:
            # 1. Load Model
            model_path = self._find_file(models_dir, config["model_file"])
            if model_path:
                result["model"] = self._safe_load(model_path)
                logger.info(f"   ✅ {model_key} model loaded")
            else:
                logger.warning(f"   ⚠️ {model_key} model not found")

            # 2. Load Vectorizer
            vec_path = self._find_file(models_dir, config["vectorizer_file"])
            if vec_path:
                result["vectorizer"] = self._safe_load(vec_path)
                logger.info(f"   ✅ {model_key} vectorizer loaded")
            else:
                logger.warning(f"   ⚠️ {model_key} vectorizer not found")

            # 3. Load Encoder
            enc_path = self._find_file(models_dir, config["encoder_file"])
            if enc_path:
                try:
                    result["encoder"] = self._safe_load(enc_path)
                    logger.info(f"   ✅ {model_key} encoder loaded")
                    if hasattr(result["encoder"], "classes_"):
                        logger.info(f"   📊 {model_key} classes: {result['encoder'].classes_}")
                except Exception as e:
                    logger.warning(f"   ⚠️ Could not load encoder: {e}")
                    result["encoder"] = None
            else:
                logger.warning(f"   ⚠️ Encoder not found: {config['encoder_file']}")
                result["encoder"] = None

            return result

        except Exception as e:
            logger.error(f"   ❌ Error loading {model_key}: {e}")
            return result

    def _safe_load(self, path: str) -> Any:
        """Safe model loading with multiple fallback methods"""
        try:
            return joblib.load(path)
        except Exception as e1:
            logger.debug(f"   joblib failed: {e1}")

        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e2:
            logger.debug(f"   pickle failed: {e2}")

        try:
            if "numpy._core" not in sys.modules:
                sys.modules["numpy._core"] = np.core

            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e3:
            logger.error(f"   All loading methods failed: {e3}")
            raise ValueError(f"Could not load {path}")

    def _load_models(self):
        """Load all registered models"""
        logger.info("📥 Loading models...")

        for model_key, config in self._model_registry.items():
            logger.info(f"   Loading {model_key}...")
            self._models[model_key] = self._load_single_model(model_key, config)

        logger.info("✅ All models loaded!")

    def get_model(self, name: str, component: str = "model"):
        """Get a specific model component"""
        if name not in self._models:
            raise ValueError(f"Model '{name}' not found")

        if component not in self._models[name]:
            raise ValueError(f"Component '{component}' not found for '{name}'")

        return self._models[name][component]

    def get_sentiment_components(self):
        """Get all sentiment components at once (4 Classes)"""
        return (
            self.get_model("sentiment", "model"),
            self.get_model("sentiment", "vectorizer"),
            self.get_model("sentiment", "encoder"),
        )

    def get_category_components(self):
        """Get all category components at once"""
        return (
            self.get_model("category", "model"),
            self.get_model("category", "vectorizer"),
            self.get_model("category", "encoder"),
        )

    def get_priority_components(self):
        """Get all priority components at once (20 Clusters, 98.84% CV)"""
        return (
            self.get_model("priority", "model"),
            self.get_model("priority", "vectorizer"),
            self.get_model("priority", "encoder"),
        )

    @property
    def models(self) -> Dict:
        """Get all models"""
        return self._models

    def reload(self):
        """Reload all models (useful for development)"""
        self._loaded = False
        self._models = {}
        self._load_models()
        self._loaded = True


# Singleton instance
@lru_cache()
def get_model_manager() -> ModelManager:
    """Get the singleton ModelManager instance"""
    return ModelManager()


# Convenience functions
def get_sentiment_model():
    return get_model_manager().get_model("sentiment", "model")


def get_sentiment_vectorizer():
    return get_model_manager().get_model("sentiment", "vectorizer")


def get_sentiment_encoder():
    return get_model_manager().get_model("sentiment", "encoder")


def get_priority_model():
    return get_model_manager().get_model("priority", "model")


def get_priority_vectorizer():
    return get_model_manager().get_model("priority", "vectorizer")


def get_priority_encoder():
    return get_model_manager().get_model("priority", "encoder")


# ============================================
# JWT FUNCTIONS
# ============================================


def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify a JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    return payload


# ============================================
# USERS FUNCTIONS
# ============================================

USERS_FILE = "users.json"


def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to save users: {e}")
