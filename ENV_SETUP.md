# Environment Variables Setup

## Required for Vercel Deployment

### GEMINI_API_KEY
Your Google Gemini API key for the chatbot AI functionality.

**How to get it:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

**How to set in Vercel:**
1. Go to your Vercel project dashboard
2. Click **Settings** → **Environment Variables**
3. Add new variable:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `your-api-key-here`
   - **Environments**: Check all (Production, Preview, Development)
4. Click **Save**
5. **Redeploy** your project

## Optional Variables

### REACT_APP_BACKEND_URL
Frontend uses this to determine the API URL. 

**For Vercel:** Not needed (uses relative `/api/chat`)
**For local dev:** Set to `http://localhost:5000`

## Local Development

Create a `.env` file in the `ChatBot` directory:

```env
GEMINI_API_KEY=your-api-key-here
```

Then run:
```bash
# Backend
cd Backend
source ../.venv/Scripts/activate  # Windows
python app.py

# Frontend (separate terminal)
cd frontend
npm start
```

## Verification

After setting environment variables in Vercel, verify:

```bash
# Check if variables are set
vercel env ls

# Should show:
# GEMINI_API_KEY (Production, Preview, Development)
```

## Troubleshooting

**Error: "GEMINI_API_KEY environment variable is not set!"**
- ✅ Set the variable in Vercel Dashboard
- ✅ Redeploy after setting variables
- ✅ Check spelling (case-sensitive)

**API returns: "AI service temporarily unavailable"**
- Invalid or expired API key
- API quota exceeded
- Generate new key from Google AI Studio
