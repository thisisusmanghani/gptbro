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

# Gemini models, tried in order. Free-tier quotas are per model (gemini-2.5-flash allows
# only 20 requests/day), so when one fails - quota (429), removed, overloaded - the chat
# falls through to the next. No test call at startup, so booting doesn't spend quota.
MODEL_OPTIONS = [
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
]

# Index of the last model that worked, so later requests start there
current_model_index = 0

# Usman Ghani's CV Knowledge Base
CV_KNOWLEDGE = """
ABOUT USMAN GHANI (The Creator):
Usman Ghani is a Full-Stack Developer and Flutter & ML Engineer based in Islamabad, Pakistan.

CONTACT:
Email: iamusmanbro@gmail.com
Phone: +92 321 6593094
LinkedIn: linkedin.com/in/iamusmanbro
GitHub: github.com/thisisusmanghani
Portfolio: usmanghani.dev

PROFESSIONAL SUMMARY:
Usman has 3+ years of experience shipping production software and has delivered 50+ projects for clients in four countries: Germany, Japan, Bangladesh and Pakistan. His apps are live on the App Store and Google Play. He is currently the lead full-stack developer and sole engineer of AutoPort, a multilingual B2B SaaS for Japanese used-car exporters.

WORK EXPERIENCE:
1. Lead Full-Stack Developer and sole engineer at AutoPort (Feb 2025 - Present)
   AutoPort is a multilingual B2B SaaS for Japanese used-car exporters: vehicles, shipments, container/ETA tracking via ShipsGo, multi-currency append-only buyer ledgers with the FX rate captured per entry, and tenant- and buyer-scoped role-based access.
   Available in four languages: English, Japanese, Arabic and Urdu (Arabic and Urdu are right-to-left).
   Stack: Next.js 16 + React 19 web app, a standalone Hono 4 API, Supabase (Postgres, row-level security, Auth, Storage, Realtime), Turborepo monorepo, Vercel (web) + Heroku (API), OpenTelemetry tracing, PostHog analytics.
   Live at useautoport.com. Case study: usmanghani.dev/case-study/autoport
2. Full-Stack Developer & Collaborator at TechWebNinja, a web agency (Apr 2024 - Jan 2025)
   Custom CRMs, admin dashboards and business systems; deployments on Vercel, Hostinger and Azure.
3. Full-Stack Developer at GreenMan (Aug 2023 - May 2024)
   Construction-machinery e-commerce platform on Next.js, web-scraping pipelines, OCR and document processing.
4. Independent / Freelance Developer for International Clients (2021 - Present)

KEY PROJECTS:
CrowdWave (client in Germany): crowd-sourced package delivery. Flutter app on iOS and Android (Stripe payments, geolocation-based matching, realtime tracking with push notifications), plus the marketing site and an operations CRM (React + Firebase).
CodeBypass (client in Bangladesh): temporary US non-VoIP numbers for online verification. Node.js/Express/MongoDB, TellaBot and DaisySMS providers with automatic fallback, Cryptomus crypto payments, sub-200 ms API responses, admin CRM.
MMSC (client in Pakistan): group website for INDEX, NOVVES, GreenMan and MVL.
AutoPort (current work): see WORK EXPERIENCE above.

OTHER PROJECTS:
Richi Billings: invoicing with PDF export and tax handling
AnyLead: telemarketing CRM
UsmanCart: MERN storefront with Stripe
Nexus: admin dashboard
Healthcare platform with an AI assistant
Inventory ERP with barcode scanning
WebRTC video-conference app
Odyssey: Three.js portfolio experiment
FindMyUni: university data scraper with an AI chatbot (deployed on Azure)
Restaurant QR ordering system
GPT Bro: this chatbot

TECHNICAL SKILLS:
Languages: TypeScript, JavaScript, Python, Dart, SQL
Web: React, Next.js, Node.js, Hono, Express, Tailwind
Mobile: Flutter, React Native
Data: Supabase, PostgreSQL, MongoDB, Firebase, MySQL
ML & AI: FastAPI, scikit-learn, Pandas, NumPy, LangChain
Cloud & Ops: Docker, Vercel, Azure, Heroku, Turborepo, OpenTelemetry, Git
Payments: Stripe, Cryptomus

EDUCATION:
BS Information Technology, Quaid-i-Azam University, Islamabad (2021 - 2025)

CERTIFICATIONS:
Supervised Machine Learning (DeepLearning.AI/Stanford)
AI For Everyone (DeepLearning.AI)
Introduction to Docker (Google Cloud)
Data Analysis with Spreadsheets and SQL (Meta)
And more from Coursera

DEVELOPMENT PHILOSOPHY:
Usman uses AI tools such as GitHub Copilot to prototype and ship quickly.

ACHIEVEMENTS:
50+ projects delivered for clients in four countries (Germany, Japan, Bangladesh, Pakistan)
Apps live on the iOS App Store and Google Play Store
Sole engineer of AutoPort, a live multilingual B2B SaaS (useautoport.com)
Integrated multiple payment gateways (Stripe, Cryptomus)

AVAILABILITY:
Open to remote roles, contracts and freelance work.

LANGUAGES: English (Professional), Urdu (Native)
"""

@app.route("/")
def home():
    return "Flask backend is running! Go to /api/chat to chat."

@app.route("/api/chat", methods=["POST", "OPTIONS"])
@cross_origin()
def chat():
    global current_model_index

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

    for offset in range(len(MODEL_OPTIONS)):
        index = (current_model_index + offset) % len(MODEL_OPTIONS)
        model_name = MODEL_OPTIONS[index]
        try:
            response = genai.GenerativeModel(model_name).generate_content(contents)  # type: ignore
            current_model_index = index
            return jsonify({"reply": response.text})
        except Exception as e:
            # Logged in production too, so failures show up in the host's logs
            print(f"Gemini model {model_name} failed, trying next: {str(e)[:200]}", flush=True)

    return jsonify({"error": "Service temporarily unavailable. Please try again."}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug)
