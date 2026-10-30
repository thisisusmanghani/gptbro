import json
import os
from datetime import datetime

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
    print("✅ Google GenerativeAI imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    GENAI_AVAILABLE = False
    genai = None

# Initialize Gemini model with fallback options
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
    if not GENAI_AVAILABLE:
        print("❌ Google GenerativeAI library not available")
        raise Exception("Google GenerativeAI library not available")
    
    # Get API key
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        print("❌ GEMINI_API_KEY environment variable is not set!")
        raise Exception("GEMINI_API_KEY environment variable is not set!")
    
    print(f"✅ API key found: {API_KEY[:10]}...")
    
    try:
        genai.configure(api_key=API_KEY)
        print("✅ Genai configured successfully")
    except Exception as e:
        print(f"❌ Failed to configure genai: {e}")
        raise e
    
    for model_name in MODEL_OPTIONS:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✅ Initialized model: {model_name}")
            return model
        except Exception as e:
            print(f"❌ Model {model_name} failed: {str(e)[:100]}")
            continue
    
    raise Exception("No working Gemini model found! Please check your API key.")

# Don't initialize at import time
model = None

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

def handler(event, context=None):
    """Vercel serverless function handler
    
    Vercel passes HTTP event with structure:
    {
        'httpMethod': 'POST',
        'headers': {...},
        'body': '...',  # JSON string
        'path': '/api/chat',
        'queryStringParameters': {...}
    }
    """
    global model
    
    try:
        # Debug: Print event structure
        print(f"Event type: {type(event)}")
        print(f"Event keys: {list(event.keys()) if isinstance(event, dict) else 'Not a dict'}")
        
        # Handle Vercel HTTP event format
        method = event.get('httpMethod', event.get('method', 'GET')).upper()
        
        # Parse request body
        data = {}
        if method == 'POST':
            body = event.get('body', '')
            print(f"Body type: {type(body)}, Content: {str(body)[:200]}")
            
            if isinstance(body, str) and body:
                try:
                    data = json.loads(body)
                except Exception as parse_error:
                    print(f"JSON parse error: {parse_error}")
                    data = {}
            elif isinstance(body, dict):
                data = body
        
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Content-Type': 'application/json'
        }
        
        # Handle OPTIONS request
        if method == 'OPTIONS':
            return {
                'statusCode': 204,
                'headers': headers,
                'body': ''
            }
        
        # Handle GET request
        if method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'ChatBot API is running on Vercel! Use POST /api/chat to chat.'})
            }
        
        # Handle POST request
        if method == 'POST':
            # Initialize model if not already done
            global model
            if model is None:
                try:
                    model = get_working_model()
                except Exception as e:
                    print(f"AI initialization failed: {str(e)}")
                    # Return a fallback response instead of error
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({
                            'reply': 'Yo bro! 😎 GPT Bro is currently having some technical issues, but I\'m still here! The AI service is temporarily unavailable, but Ghani bhai is working on it. Try again in a few minutes! 🔥'
                        })
                    }
            
            messages = data.get('messages')
            
            if not messages or not isinstance(messages, list):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'No messages provided or invalid format'})
                }
            
            contents = []
            
            # Get current date and time
            current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
            
            # Add CV knowledge and current date as system context
            system_context = f"""IMPORTANT CONTEXT - You have knowledge about your creator Usman Ghani (Ghani bhai):

{CV_KNOWLEDGE}

CURRENT DATE & TIME: {current_datetime}

When asked about dates, time, current events, or "today", always use the current date/time provided above. When asked about Usman, Ghani bhai, your creator, or questions related to his experience, projects, skills, or background, use this knowledge confidently. Speak about him with pride and in your signature dramatic style!
"""
            
            # Add system context
            contents.append({"role": "user", "parts": [{"text": system_context}]})
            contents.append({"role": "model", "parts": [{"text": "Yo bro! I got all the intel about Ghani bhai locked and loaded in my memory! 🔥💀 Plus I know what time it is right now! Ask me anything about the legend himself or what's happening today!"}]})
            
            for msg in messages:
                role = "user" if msg.get("sender") == "user" else "model"
                text = msg.get("text", "")

                if role not in ["user", "model"]:
                    continue

                contents.append({"role": role, "parts": [{"text": text}]})

            max_retries = 2
            for attempt in range(max_retries):
                try:
                    response = model.generate_content(contents)
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'reply': response.text})
                    }
                except Exception as e:
                    error_msg = str(e)
                    print(f"Error calling Gemini API (attempt {attempt + 1}/{max_retries}): {error_msg[:200]}")
                    
                    # Try to reinitialize with a different model
                    if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                        if attempt < max_retries - 1:
                            print("🔄 Attempting to reinitialize with a different model...")
                            try:
                                model = get_working_model()
                                continue
                            except Exception as reinit_error:
                                print(f"Failed to reinitialize model: {reinit_error}")
                    
                    if attempt == max_retries - 1:
                        return {
                            'statusCode': 200,
                            'headers': headers,
                            'body': json.dumps({
                                'reply': 'Yo bro! 😅 I\'m having some connection issues with my AI brain right now. Ghani bhai is probably debugging something! Try asking me again in a moment! 🔧'
                            })
                        }
        
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
        
    except Exception as e:
        print(f"Handler error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }
