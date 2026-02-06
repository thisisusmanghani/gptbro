# GitHub Codespaces Configuration

This directory contains the development container configuration for GitHub Codespaces.

## What's Included

- **Node.js 18**: For running the React frontend
- **Python 3.11**: For the Flask backend
- **VS Code Extensions**:
  - GitHub Copilot & Copilot Chat (AI-powered development assistance)
  - ESLint & Prettier (Code formatting)
  - Python & Pylance (Python development)
  - Tailwind CSS IntelliSense
  - React snippets

## Using This Codespace

### Opening in Codespaces

1. Go to the repository on GitHub
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on [branch name]**

The setup script will automatically install all dependencies.

### Running the Application

#### Frontend (React)
```bash
cd frontend
npm start
```
The frontend will be available at http://localhost:3000

#### Backend (Flask)
```bash
cd Backend
python app.py
```
The backend will be available at http://localhost:5000

### Environment Variables

Make sure to set your environment variables:

**Backend** (`Backend/.env`):
```
GEMINI_API_KEY=your_api_key_here
```

**Frontend** (`frontend/.env.development`):
```
REACT_APP_API_URL=http://localhost:5000
```

### AI-Assisted Development

This codespace comes with **GitHub Copilot** and **Copilot Chat** pre-installed:
- Press `Ctrl+I` (or `Cmd+I` on Mac) to open Copilot Chat inline
- Start typing code and Copilot will provide suggestions
- Use natural language comments to generate code

## Features

- ✅ Auto-installation of all dependencies
- ✅ Pre-configured VS Code settings
- ✅ Port forwarding for frontend (3000) and backend (5000)
- ✅ GitHub CLI for repository management
- ✅ AI-powered development with Copilot

## Troubleshooting

If you encounter issues:

1. **Dependencies not installed**: Run `bash .devcontainer/setup.sh`
2. **Port conflicts**: Codespaces will automatically suggest alternative ports
3. **Environment variables**: Check that `.env` files are properly configured
