# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# 1. Import
# ============================================
from app.api.routes import router
from app.api.auth import router as auth_router  # ✅ أضيفي ده
from app.core.config import settings
from app.core.dependencies import get_model_manager

print("="*60)
print("📥 LOADING MODELS...")
print("="*60)

MODELS_LOADED = False

try:
    model_manager = get_model_manager()
    sent_model, sent_vec, sent_enc = model_manager.get_sentiment_components()
    cat_model, cat_vec, cat_enc = model_manager.get_category_components()
    pri_model, pri_vec, pri_enc = model_manager.get_priority_components()
    
    MODELS_LOADED = True
    print(f"✅ ALL MODELS LOADED SUCCESSFULLY!")
    print(f"   - Sentiment: {len(sent_enc.classes_)} classes ({sent_enc.classes_})")
    print(f"   - Category: {len(cat_enc.classes_)} classes")
    print(f"   - Priority: {len(pri_enc.classes_)} classes (98.84% CV)")
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    import traceback
    traceback.print_exc()
    MODELS_LOADED = False

# ============================================
# 2. FastAPI App
# ============================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered Customer Support System with RAG"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routes
app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")  # ✅ أضيفي ده

# ============================================
# 3. Health Check
# ============================================
@app.get("/")
async def root():
    return {
        "message": "Customer Support AI API",
        "version": settings.VERSION,
        "status": "running",
        "models_loaded": MODELS_LOADED
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "models_loaded": MODELS_LOADED,
        "sentiment_classes": list(sent_enc.classes_) if MODELS_LOADED else []
    }

# ============================================
# 4. Entry Point
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )