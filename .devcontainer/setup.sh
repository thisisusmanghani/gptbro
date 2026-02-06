#!/bin/bash

# Setup script for GPT Bro development environment
echo "🚀 Setting up GPT Bro development environment..."

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend && npm install && cd ..

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd Backend && pip install -r requirements.txt && cd ..

# Create environment files if they don't exist
if [ ! -f "Backend/.env" ]; then
    echo "📝 Creating Backend/.env from example..."
    cp Backend/.env.example Backend/.env 2>/dev/null || echo "GEMINI_API_KEY=your_api_key_here" > Backend/.env
fi

if [ ! -f "frontend/.env.development" ]; then
    echo "📝 Creating frontend/.env.development..."
    echo "REACT_APP_API_URL=http://localhost:5000" > frontend/.env.development
fi

echo "✅ Setup complete! You can now run:"
echo "   - Frontend: cd frontend && npm start"
echo "   - Backend: cd Backend && python app.py"
echo ""
echo "🤖 GitHub Copilot and Copilot Chat are enabled for AI-assisted development!"
