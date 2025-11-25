from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow frontend access
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://gpt-bro.onrender.com").split(",")
CORS(app, origins=ALLOWED_ORIGINS)

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=API_KEY)  # type: ignore

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")  # type: ignore

# Usman Ghani's CV Knowledge Base
CV_KNOWLEDGE = """
ABOUT USMAN GHANI (The Creator):
Usman Ghani is a versatile Backend Developer, Machine Learning Engineer, and Full-Stack Developer from Islamabad, Pakistan.

CONTACT:
- Email: iamusmanbro@gmail.com
- Phone: +92 321 6593094
- LinkedIn: linkedin.com/in/iamusmanbro
- GitHub: github.com/thisisusmanghani
- Portfolio: usmanghani.dev

PROFESSIONAL SUMMARY:
Usman is a versatile software developer with expertise in backend systems, machine learning, and full-stack development. He has a proven track record of delivering production-ready applications for international clients across Germany, Bangladesh, and Pakistan. He specializes in rapid prototyping and AI-assisted development, with experience in mobile app publishing (Play Store & App Store), payment gateway integration, and cloud deployment.

WORK EXPERIENCE:
1. Project Manager/Team Lead at Richi Billings (2024-Present)
2. Software Developer at Anylead (2023-2024)
3. Freelance Developer for International Clients (2022-Present)

KEY PROJECTS:
- CrowdWave: Flutter mobile app for crowd-sourced logistics (Germany client, on App Store & Play Store)
- CodeBypass: Temporary phone numbers platform (Bangladesh client)
- FindMyUni: University data scraper with AI chatbot (Azure deployed)
- Restaurant QR Ordering System
- GreenMan Products: Construction machinery e-commerce

TECHNICAL SKILLS:
Languages: Python, JavaScript/TypeScript, SQL, Dart, HTML/CSS
Frameworks: React, Next.js, Node.js, Express.js, Flutter, FastAPI, TailwindCSS
Databases: MongoDB, Firebase, PostgreSQL, MySQL
AI/ML: Scikit-learn, Pandas, NumPy, Beautiful Soup, Selenium, LangChain
DevOps: Docker, Azure, Vercel, Netlify, Heroku
Tools: Stripe, Cryptomus, REST APIs, GitHub Copilot

EDUCATION:
Bachelor of Science in Information Technology from Quaid-i-Azam University, Islamabad (Nov 2021 - June 2025)
CGPA: 3.0/4.0

CERTIFICATIONS:
- Supervised Machine Learning (DeepLearning.AI/Stanford)
- AI For Everyone (DeepLearning.AI)
- Introduction to Docker (Google Cloud)
- Data Analysis with Spreadsheets and SQL (Meta)
And more from Coursera

DEVELOPMENT PHILOSOPHY:
Usman specializes in "vibe coding" - leveraging AI tools like GitHub Copilot to rapidly prototype, iterate, and deliver high-quality solutions.

ACHIEVEMENTS:
- Published Flutter app on iOS App Store and Google Play Store
- Integrated multiple payment gateways (Stripe, Cryptomus)
- Managed international clients across 3+ countries
- Deployed 10+ production applications

AVAILABILITY:
Open to full-time remote positions, contract work, or freelance projects worldwide or in Islamabad/Kashmir, Pakistan.

LANGUAGES: English (Professional), Urdu (Native)
"""

@app.route("/")
def home():
    return "Flask backend is running! Go to /api/chat to chat."

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages")

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "No messages provided or invalid format"}), 400

    contents = []
    
    # Get current date and time
    from datetime import datetime
    current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    
    # Add CV knowledge and current date as system context at the start
    system_context = f"""IMPORTANT CONTEXT - You have knowledge about your creator Usman Ghani (Ghani bhai):

{CV_KNOWLEDGE}

CURRENT DATE & TIME: {current_datetime}

When asked about dates, time, current events, or "today", always use the current date/time provided above. When asked about Usman, Ghani bhai, your creator, or questions related to his experience, projects, skills, or background, use this knowledge confidently. Speak about him with pride and in your signature dramatic style!
"""
    
    # Add system context as first user message
    contents.append({"role": "user", "parts": [{"text": system_context}]})
    contents.append({"role": "model", "parts": [{"text": "Yo bro! I got all the intel about Ghani bhai locked and loaded in my memory! 🔥💀 Plus I know what time it is right now! Ask me anything about the legend himself or what's happening today!"}]})
    
    for msg in messages:
        role = "user" if msg.get("sender") == "user" else "model"
        text = msg.get("text", "")

        # Strictly filter out unsupported roles
        if role not in ["user", "model"]:
            continue  # Skip system or invalid roles

        contents.append({"role": role, "parts": [{"text": text}]})

    # Debug logging to inspect request before sending
    print("Sending request to Gemini API with CV context")

    try:
        response = model.generate_content(contents)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
