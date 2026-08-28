# run_rag.py
"""
🚀 RAG Service Entry Point
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🚀 Starting RAG Service")
print("="*60)

try:
    from app.rag.api import app
    print("✅ RAG Service loaded!")
    
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()