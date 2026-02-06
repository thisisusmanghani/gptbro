# GPT Bro 😎

AI Chatbot powered by Google Gemini with a clean ChatGPT-style interface.

**Live**: [gpt.usmanghani.dev](https://gpt.usmanghani.dev)

## Stack
- Frontend: React + Tailwind CSS
- Backend: Vercel Serverless Functions (Python)
- AI: Google Gemini API
- Deployment: Vercel + GitHub Actions

</div>

---

## Features

<table>
<tr>
<td width="50%">

### **Modern UI/UX**
- Sleek dark/light theme toggle
- Smooth animations & transitions
- Responsive design for all devices
- Real-time typing indicators
- Message history with timestamps

</td>
<td width="50%">

### **AI-Powered**
- Google Gemini 2.0 Flash integration
- Contextual conversation memory
- Multiple AI personalities (Default, Creative, Technical)
- Image upload & analysis support
- Smart response streaming

</td>
</tr>
<tr>
<td width="50%">

### **Secure & Scalable**
- Environment-based API key management
- CORS protection for production
- Secure backend communication
- Token-based authentication ready
## Deploy

```bash
# Deploy to Vercel
vercel --prod

# Or push to GitHub (auto-deploy)
git push origin main
```

## Development

### Option 1: GitHub Codespaces (Recommended) 🚀

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=thisisusmanghani/gptbro)

1. Click the badge above or go to the repository and click **Code > Codespaces > Create codespace**
2. Wait for the environment to set up (dependencies auto-install)
3. Run frontend: `cd frontend && npm start`
4. Run backend: `cd Backend && python app.py`

**Includes**: GitHub Copilot, pre-configured extensions, and all dependencies!

### Option 2: Local Development

```bash
# Install dependencies
cd frontend && npm install

# Run with Vercel dev server
cd .. && vercel dev
```

## Features
- Clean ChatGPT-style UI (no gradients, neutral colors)
- Dark/Light mode
- Real-time AI responses
- Chat history (localStorage)
- Mobile responsive

---

Made by [Usman Ghani](https://github.com/thisisusmanghani)
