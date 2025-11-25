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

## Security Best Practices

### Implemented
- Environment-based secrets
- CORS whitelisting
- Input validation
- Error message sanitization
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
