#!/bin/bash
# docker/entrypoint.sh

set -e

echo "============================================================"
echo "🚀 Starting Customer Support AI Services"
echo "============================================================"

# Wait for models to be available
echo "⏳ Waiting for models..."
while [ ! -f /app/models/priority_model_final.pkl ]; do
    echo "   Waiting for models..."
    sleep 5
done
echo "✅ Models found!"

# Start services
echo ""
echo "📊 Starting services..."

# Run API and RAG in parallel
python run_rag.py &
python run.py

# Wait for all processes
wait