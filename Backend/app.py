from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS properly for production
# Allow your frontend domain and localhost for development
ALLOWED_ORIGINS = [
    "https://gptbro-gldg5h8w8-usmans-projects-19e9822c.vercel.app",  # Vercel production frontend
    "https://gptbro.vercel.app",  # Vercel custom domain (if added)
    "http://localhost:3000",  # Local development
    "http://localhost:5173",  # Vite dev server
]

CORS(app, 
     resources={r"/*": {
         "origins": ALLOWED_ORIGINS,
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"],
         "supports_credentials": False
     }})

# Get API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set!")

genai.configure(api_key=API_KEY)  # type: ignore

# Initialize Gemini model with fallback options (all available models)
MODEL_OPTIONS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-2.5-pro",
    "gemini-2.0-pro-exp"
]

def get_working_model():
    """Try to find a working model from the available options"""
    is_production = os.getenv("FLASK_ENV") == "production"
    
    # Try predefined models (optimized order)
    for model_name in MODEL_OPTIONS:
        try:
            model = genai.GenerativeModel(model_name)  # type: ignore
            # Test the model with a simple request
            response = model.generate_content("Hi")
            if not is_production:
                print(f"✅ Successfully initialized model: {model_name}")
            return model
        except Exception as e:
            if not is_production:
                error_msg = str(e)[:100]  # Truncate long errors
                print(f"❌ Model {model_name} failed: {error_msg}")
            continue
    
    raise Exception("No working Gemini model found! Please check your API key and internet connection.")

model = get_working_model()

# Usman Ghani's CV Knowledge Base
CV_KNOWLEDGE = """
ABOUT USMAN GHANI (The Creator):
Usman Ghani is a versatile Backend Developer, Machine Learning Engineer, and Full-Stack Developer from Islamabad, Pakistan.

CONTACT:
Email: iamusmanbro@gmail.com
Phone: +92 321 6593094
LinkedIn: linkedin.com/in/iamusmanbro
GitHub: github.com/thisisusmanghani
Portfolio: usmanghani.dev

PROFESSIONAL SUMMARY:
Usman is a versatile software developer with expertise in backend systems, machine learning, and full-stack development. He has a proven track record of delivering production-ready applications for international clients across Germany, Bangladesh, and Pakistan. He specializes in rapid prototyping and AI-assisted development, with experience in mobile app publishing (Play Store and App Store), payment gateway integration, and cloud deployment.

WORK EXPERIENCE:
1. Project Manager/Team Lead at Richi Billings (2024-Present)
2. Software Developer at Anylead (2023-2024)
3. Freelance Developer for International Clients (2022-Present)

KEY PROJECTS:
CrowdWave: Flutter mobile app for crowd-sourced logistics (Germany client, on App Store and Play Store)
CodeBypass: Temporary phone numbers platform (Bangladesh client)
FindMyUni: University data scraper with AI chatbot (Azure deployed)
Restaurant QR Ordering System
GreenMan Products: Construction machinery e-commerce

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
Supervised Machine Learning (DeepLearning.AI/Stanford)
AI For Everyone (DeepLearning.AI)
Introduction to Docker (Google Cloud)
Data Analysis with Spreadsheets and SQL (Meta)
And more from Coursera

DEVELOPMENT PHILOSOPHY:
Usman specializes in "vibe coding" which means leveraging AI tools like GitHub Copilot to rapidly prototype, iterate, and deliver high-quality solutions.

ACHIEVEMENTS:
Published Flutter app on iOS App Store and Google Play Store
Integrated multiple payment gateways (Stripe, Cryptomus)
Managed international clients across 3 plus countries
Deployed 10 plus production applications

AVAILABILITY:
Open to full-time remote positions, contract work, or freelance projects worldwide or in Islamabad/Kashmir, Pakistan.

LANGUAGES: English (Professional), Urdu (Native)
"""

@app.route("/")
def home():
    return "Flask backend is running! Go to /api/chat to chat."

@app.route("/api/chat", methods=["POST", "OPTIONS"])
@cross_origin()
def chat():
    global model
    
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return "", 204
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

    is_production = os.getenv("FLASK_ENV") == "production"
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = model.generate_content(contents)
            return jsonify({"reply": response.text})
        except Exception as e:
            error_msg = str(e)
            if not is_production:
                print(f"Error calling Gemini API (attempt {attempt + 1}/{max_retries}): {error_msg[:200]}")
            
            # If model not found, try to reinitialize with a different model
            if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                if attempt < max_retries - 1:
                    if not is_production:
                        print("🔄 Attempting to reinitialize with a different model...")
                    try:
                        model = get_working_model()
                        continue  # Retry with the new model
                    except Exception as reinit_error:
                        if not is_production:
                            print(f"Failed to reinitialize model: {reinit_error}")
            
            # If last attempt, return error
            if attempt == max_retries - 1:
                return jsonify({"error": "Service temporarily unavailable. Please try again."}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
