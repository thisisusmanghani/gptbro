<div align="center">

# Nexus AI Backend

### Flask API for AI Chatbot

[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)](https://python.org)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render)](https://render.com)

**Secure, scalable Flask API powered by Google Gemini 2.0**

</div>

---

## Features

### **API Capabilities**
- **RESTful Endpoints** - Clean, documented API structure
- **Gemini 2.0 Integration** - Latest AI model from Google
- **Conversation Memory** - Context-aware responses
- **Image Processing** - Vision capabilities for image analysis
- **Error Handling** - Robust error management

### **Security**
- **Environment Variables** - Secure API key management
- **CORS Protection** - Configurable origin whitelisting
- **Input Validation** - Request data sanitization
- **Rate Limiting Ready** - Easy to add rate limits
- **Production Hardened** - Security best practices

### **Performance**
- **Lightweight** - Minimal dependencies
- **Fast Response** - Optimized request handling
- **Streaming Ready** - Support for response streaming
- **Scalable** - Easy horizontal scaling

---

## Quick Start

### Prerequisites
```bash
Python 3.11+
pip (Python package manager)
Google Gemini API Key
```

### Installation

```bash
# Navigate to backend directory
cd Backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running Locally

```bash
# Make sure virtual environment is activated
python app.py

# Server runs on http://localhost:5000
# Debug mode enabled for development
```

---

## Dependencies

```txt
flask                # Web framework
flask-cors          # Cross-origin resource sharing
google-genai        # Google Gemini AI integration
python-dotenv       # Environment variable management
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Backend/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version for deployment
├── .env.example           # Environment template
├── .env                   # Local environment (gitignored)
├── .gitignore            # Git ignore rules
│
└── (future structure)
    ├── routes/            # API route handlers
    │   ├── chat.py
    │   └── health.py
    │
    ├── services/          # Business logic
    │   ├── ai_service.py
    │   └── auth_service.py
    │
    ├── models/            # Data models
    ├── utils/             # Helper functions
    └── tests/             # Unit tests
```

---

## API Endpoints

### `GET /`
**Health check endpoint**

**Response:**
```json
{
  "message": "Flask backend is running! Go to /api/chat to chat."
}
```

### `POST /api/chat`
**Main chat endpoint for AI conversation**

**Request:**
```json
{
  "messages": [
    {
      "sender": "user",
      "text": "Hello, how are you?"
    },
    {
      "sender": "bot",
      "text": "I'm doing great! How can I help you?"
    }
  ]
}
```

**Response (Success):**
```json
{
  "reply": "I'm doing well, thank you! I'm here to help you with any questions you have."
}
```

**Response (Error):**
```json
{
  "error": "Error message description"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error

---

## Configuration

### Environment Variables

**`.env` file:**
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (with defaults)
PORT=5000
FLASK_ENV=development
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

### Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

### CORS Configuration

Modify allowed origins in `app.py`:

```python
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://your-frontend.vercel.app"
).split(",")
```

---

## Deployment

### Deploy to Render (Recommended - FREE)

#### Option 1: Blueprint (Automated)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Backend ready for deployment"
   git push
   ```

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect GitHub repository
   - Render auto-detects `render.yaml`
   - Add environment variable: `GEMINI_API_KEY`
   - Click "Apply"

3. **Done** Backend deploys in ~5 minutes

#### Option 2: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name:** `nexus-backend`
   - **Region:** Choose closest
   - **Branch:** `main`
   - **Root Directory:** `Backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Plan:** `Free`

5. Environment Variables:
   ```
   GEMINI_API_KEY = your_actual_key
   PORT = 10000
   FLASK_ENV = production
   ALLOWED_ORIGINS = https://your-frontend.vercel.app
   ```

6. Click "Create Web Service"

### Deploy to Railway (Alternative - FREE)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

---

## Testing

### Manual Testing

```bash
# Health check
curl http://localhost:5000/

# Chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"sender": "user", "text": "Hello!"}
    ]
  }'
```

### Unit Tests (Future)

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## Security Best Practices

### Implemented
- Environment-based secrets
- CORS whitelisting
- Input validation
- Error message sanitization

### Recommended Additions
```python
# Rate limiting
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr
)

@app.route("/api/chat", methods=["POST"])
@limiter.limit("10 per minute")
def chat():
    # ...
```

### API Key Rotation
- Rotate Gemini API keys regularly
- Use separate keys for dev/prod
- Monitor usage in Google AI Studio

---

## Monitoring & Logging

### View Logs (Render)
```bash
# In Render Dashboard:
Your Service → Logs tab
```

### Custom Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("User message received")
```

---

## Troubleshooting

### Common Issues

**Issue:** `GEMINI_API_KEY not set`
```bash
# Solution: Check .env file
cat .env | grep GEMINI_API_KEY

# Or set directly
export GEMINI_API_KEY=your_key_here
```

**Issue:** `Port already in use`
```bash
# Solution: Kill process or use different port
PORT=5001 python app.py
```

**Issue:** CORS error
```bash
# Solution: Add frontend URL to ALLOWED_ORIGINS
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

**Issue:** Import error
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Performance Tips

### 1. Caching (Future Enhancement)
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.cached(timeout=300)
def get_cached_response():
    # ...
```

### 2. Database for Chat History
```python
# Use PostgreSQL on Render
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
```

### 3. Async Processing
```python
from flask import jsonify
import asyncio

async def async_ai_call():
    # ...

@app.route("/api/chat", methods=["POST"])
async def chat():
    result = await async_ai_call()
    return jsonify({"reply": result})
```

---

## API Documentation (Swagger - Future)

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Nexus AI API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

---

## Contributing

### Backend Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Include type hints
- Write unit tests
- Update API documentation

### Example Contribution
```python
def process_message(message: str) -> dict:
    """
    Process user message and return AI response.
    
    Args:
        message (str): User input text
        
    Returns:
        dict: Response containing AI reply
        
    Raises:
        ValueError: If message is empty
    """
    # Implementation
```

---

## License

Part of the Nexus AI Chatbot project - MIT License

---

<div align="center">

### Powered by Flask & Google Gemini 2.0

[Back to Top](#nexus-ai-backend)

</div>
