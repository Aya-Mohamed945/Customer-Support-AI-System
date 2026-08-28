# backend/run.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("🚀 Starting Customer Support AI API")
print("="*60)

try:
    from app.main import app
    print("✅ App loaded successfully!")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()