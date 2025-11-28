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
