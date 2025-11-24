# 🚀 Deployment Guide - ChatBot to Render + Vercel

## 📋 Prerequisites
- GitHub account
- Render account (render.com) - FREE
- Vercel account (vercel.com) - FREE
- Google Gemini API Key

---

## 🔐 Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key (keep it secret!)

---

## 🐙 Step 2: Push to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit - ChatBot with secure environment variables"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/chatbot.git
git branch -M main
git push -u origin main
```

---

## 🖥️ Step 3: Deploy Backend to Render (FREE)

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +" → "Blueprint"**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Set environment variables:
   - `GEMINI_API_KEY`: (paste your API key)
   - `ALLOWED_ORIGINS`: `https://your-frontend.vercel.app` (update after Vercel deployment)
6. Click **"Apply"**
7. Wait ~5 minutes for deployment
8. Copy your backend URL: `https://chatbot-backend-xxxx.onrender.com`

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +" → "Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `chatbot-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `Backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: `Free`
5. Add Environment Variables:
   - `GEMINI_API_KEY`: (your API key)
   - `PORT`: `10000`
   - `FLASK_ENV`: `production`
   - `ALLOWED_ORIGINS`: `http://localhost:3000` (update later)
6. Click **"Create Web Service"**
7. Copy your backend URL

---

## 🌐 Step 4: Update Frontend Configuration

Create `frontend/.env.production`:

```env
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

Update `frontend/src/App.js` to use backend instead of direct API calls:

```javascript
// Replace direct Gemini API calls with:
const apiUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:5000/api/chat";

const response = await fetch(apiUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ messages: chatHistoryForAPI }),
  signal,
});
```

---

## ⚡ Step 5: Deploy Frontend to Vercel (FREE)

1. Go to [Vercel Dashboard](https://vercel.com/new)
2. Click **"Import Project"**
3. Select your GitHub repository
4. Configure:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. Add Environment Variable:
   - `REACT_APP_BACKEND_URL`: `https://your-backend.onrender.com`
6. Click **"Deploy"**
7. Copy your frontend URL: `https://chatbot-xxxx.vercel.app`

---

## 🔄 Step 6: Update CORS Settings

1. Go back to Render Dashboard
2. Find your backend service
3. Update `ALLOWED_ORIGINS` environment variable:
   - Value: `https://your-frontend.vercel.app,http://localhost:3000`
4. Save and redeploy

---

## ✅ Step 7: Test Your Deployment

1. Visit your Vercel URL
2. Send a test message
3. Check if the bot responds
4. Monitor Render logs if issues occur

---

## 🐛 Troubleshooting

### Backend Issues
```bash
# View Render logs
# Go to Render Dashboard → Your Service → Logs
```

**Common Issues:**
- ❌ `GEMINI_API_KEY not set` → Add env variable in Render
- ❌ CORS error → Update `ALLOWED_ORIGINS` with your Vercel URL
- ❌ 503 Service Unavailable → Render free tier sleeps after 15min inactivity (wakes up automatically)

### Frontend Issues
- ❌ API call fails → Check backend URL in environment variables
- ❌ Build fails → Run `npm install` and `npm run build` locally first

---

## 💰 Cost Breakdown

| Service | Free Tier Limits | Cost |
|---------|------------------|------|
| **Render Backend** | 750 hrs/month, sleeps after 15min | $0 |
| **Vercel Frontend** | 100GB bandwidth, unlimited sites | $0 |
| **Google Gemini API** | 60 requests/min, 1500/day | $0 |
| **Total** | | **$0/month** ✅ |

---

## 🔒 Security Checklist

- ✅ API keys in environment variables
- ✅ .env files in .gitignore
- ✅ CORS configured for specific origins
- ✅ No hardcoded secrets in code

---

## 🎉 You're Done!

Your ChatBot is now live and secure! Share your Vercel URL with the world! 🚀

**Need help?** Check the logs in Render/Vercel dashboards.
