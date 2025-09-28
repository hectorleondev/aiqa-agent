#!/bin/bash

# FastAPI Development Server Startup Script
# This script provides an easy way to start the FastAPI application with optimal settings

set -e

echo "🚀 Starting AI QA Agent - FastAPI Application"
echo "=============================================="

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found in current directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Default values
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
RELOAD=${RELOAD:-"true"}

echo "📍 Host: $HOST"
echo "🔌 Port: $PORT"
echo "🔄 Auto-reload: $RELOAD"
echo ""

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "❌ FastAPI or uvicorn not found. Installing dependencies..."
    pip install -r dev-requirements.txt
}

echo "✅ Dependencies OK"
echo ""

# Start the server
echo "🌟 Starting FastAPI server..."
echo "📖 API will be available at: http://localhost:$PORT"
echo "📚 Documentation at: http://localhost:$PORT/docs"
echo "🔄 Interactive docs at: http://localhost:$PORT/redoc"
echo ""
echo "Press Ctrl+C to stop the server"

if [ "$RELOAD" = "true" ]; then
    echo "🔄 Auto-reload is enabled"
    uvicorn main:app --host "$HOST" --port "$PORT" --reload
else
    echo "🔄 Auto-reload is disabled"
    uvicorn main:app --host "$HOST" --port "$PORT"
fi