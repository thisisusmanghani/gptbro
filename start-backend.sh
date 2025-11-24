#!/bin/bash
# Quick test script for local development

echo "🚀 Starting ChatBot Backend..."
echo ""

cd Backend

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Please create Backend/.env with your GEMINI_API_KEY"
    exit 1
fi

# Start the Flask server
echo "✅ Environment variables loaded"
echo "🌐 Backend will run on http://localhost:5000"
echo "📊 Press Ctrl+C to stop"
echo ""

python app.py
