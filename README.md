<div align="center">

# Nexus AI Chatbot

### Intelligent Conversational AI Assistant

[![React](https://img.shields.io/badge/React-19.1.0-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.1.8-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

**A modern, full-stack AI chatbot powered by Google Gemini 2.0 with real-time responses, image analysis, and intelligent conversation memory.**

[Live Demo](https://your-chatbot.vercel.app) • [Report Bug](https://github.com/thisisusmanghani/chatbot/issues) • [Request Feature](https://github.com/thisisusmanghani/chatbot/issues)

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
- Production-optimized deployment

</td>
<td width="50%">

### **Persistent Data**
- Local storage for chat history
- Session management
- User preferences saved
- Export/import chat logs
- Offline-capable PWA ready

</td>
</tr>
</table>

---

## Screenshots

<div align="center">

### Dark Mode Interface
![Dark Mode](https://via.placeholder.com/800x450/1a1a1a/ffffff?text=Dark+Mode+Interface)

### Light Mode Interface
![Light Mode](https://via.placeholder.com/800x450/ffffff/000000?text=Light+Mode+Interface)

### AI Personalities
![AI Personalities](https://via.placeholder.com/800x450/4a5568/ffffff?text=Multiple+AI+Personalities)

</div>

---

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- Python 3.11+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# Clone the repository
git clone https://github.com/thisisusmanghani/chatbot.git
cd chatbot

# Install backend dependencies
cd Backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Install frontend dependencies
cd ../frontend
npm install
```

### Running Locally

**Terminal 1 - Backend:**
```bash
cd Backend
python app.py
# Backend runs on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

Visit `http://localhost:3000` and start chatting!

---

## Tech Stack

### Frontend
- **React 19.1.0** - Modern UI library
- **Tailwind CSS 4.1.8** - Utility-first styling
- **Heroicons** - Beautiful SVG icons
- **Local Storage** - Client-side persistence

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Google Generative AI** - Gemini 2.0 integration
- **Python-dotenv** - Environment management

### Deployment
- **Vercel** - Frontend hosting (FREE)
- **Render** - Backend hosting (FREE)
- **Git** - Version control

---

## Project Structure

```
chatbot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── App.js           # Main application component
│   │   ├── components/      # Reusable UI components
│   │   └── assets/          # Images, fonts, etc.
│   ├── public/              # Static files
│   └── package.json         # Frontend dependencies
│
├── Backend/                 # Flask backend API
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── runtime.txt         # Python version
│
├── render.yaml             # Render deployment config
├── DEPLOYMENT.md           # Detailed deployment guide
└── README.md               # You are here!
```

---

## Deployment

### Quick Deploy (5 minutes)

1. **Deploy Backend to Render:**
   - Push code to GitHub
   - Connect repo to [Render](https://render.com)
   - Add `GEMINI_API_KEY` environment variable
   - Deploy automatically via `render.yaml`

2. **Deploy Frontend to Vercel:**
   - Connect repo to [Vercel](https://vercel.com)
   - Set `REACT_APP_BACKEND_URL` environment variable
   - Deploy with one click

**Full deployment guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## Usage

### Basic Chat
```
User: Hello! What can you do?
Nexus: I'm Nexus, your AI assistant! I can help you with...
```

### Image Analysis
1. Click the image upload button
2. Select an image
3. Ask questions about it
4. Get intelligent analysis from Gemini Vision

### AI Personalities
- **Default Mode**: Balanced, helpful responses
- **Creative Mode**: Imaginative, out-of-the-box thinking
- **Technical Mode**: Precise, fact-based answers

---

## Configuration

### Environment Variables

#### Backend (`Backend/.env`)
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
FLASK_ENV=production
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
```

#### Frontend (`frontend/.env.production`)
```env
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

---

## Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Known Issues

- Backend may sleep on Render free tier (15min inactivity)
- First request after sleep takes ~30 seconds
- Large images may take longer to process

**Solutions in progress** - See [Issues](https://github.com/thisisusmanghani/chatbot/issues)

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) - Powerful AI engine
- [React](https://reactjs.org/) - Frontend framework
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [Tailwind CSS](https://tailwindcss.com/) - Styling framework
- [Heroicons](https://heroicons.com/) - Beautiful icons

---

<div align="center">

### Star this repo if you find it helpful!

Made with care by [Usman Ghani](https://github.com/thisisusmanghani)

[Back to Top](#nexus-ai-chatbot)

</div>
