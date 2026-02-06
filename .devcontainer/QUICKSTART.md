# Quick Start Guide for GPT Bro Codespace

Welcome to your GPT Bro development environment! 🎉

## What's Ready

✅ Node.js 18 for React development  
✅ Python 3.11 for Flask backend  
✅ All dependencies auto-installed  
✅ GitHub Copilot enabled for AI assistance  
✅ VS Code pre-configured with useful extensions  

## Getting Started in 3 Steps

### 1. Set Up Environment Variables

**Backend API Key:**
```bash
# Edit Backend/.env and add your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > Backend/.env
```

### 2. Start the Backend (Terminal 1)
```bash
cd Backend
python app.py
# Backend runs on http://localhost:5000
```

### 3. Start the Frontend (Terminal 2)
```bash
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

## Common Tasks

### Running Tests
```bash
cd frontend
npm test
```

### Building for Production
```bash
cd frontend
npm run build
```

### Using GitHub Copilot

- **Inline suggestions**: Just start typing, Copilot will suggest code
- **Chat**: Press `Ctrl+I` (or `Cmd+I` on Mac) for inline chat
- **Sidebar**: Click the Copilot icon in the sidebar for longer conversations
- **Generate code from comments**: Write a comment describing what you want, press Enter

Example:
```javascript
// Create a function that validates email addresses

// Copilot will suggest the implementation!
```

### Useful VS Code Commands

- `Ctrl+Shift+P` - Command palette
- `Ctrl+` ` - Toggle terminal
- `Ctrl+P` - Quick file open
- `Ctrl+F` - Find in file
- `Ctrl+Shift+F` - Find in all files

## Project Structure

```
gptbro/
├── frontend/          # React application
│   ├── src/          # React components and logic
│   └── public/       # Static assets
├── Backend/          # Flask API
│   ├── api/         # API endpoints
│   └── app.py       # Main Flask app
└── .devcontainer/   # Codespace configuration
```

## Need Help?

- Check `.devcontainer/README.md` for detailed documentation
- Ask GitHub Copilot Chat for help
- Review the main README.md

Happy coding! 🚀
