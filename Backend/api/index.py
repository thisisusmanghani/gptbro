from http.server import BaseHTTPRequestHandler
import json
import os

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

MODEL_OPTIONS = ["gemini-2.0-flash-exp", "gemini-exp-1114", "gemini-pro-latest"]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Backend API is running!'}).encode())
        return

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            messages = data.get('messages', [])
            
            # Initialize Gemini
            API_KEY = os.getenv("GEMINI_API_KEY")
            if not API_KEY or not GENAI_AVAILABLE:
                raise Exception("API not configured")
            
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_OPTIONS[0])
            
            # Format messages
            contents = []
            for msg in messages:
                role = "user" if msg.get("sender") == "user" else "model"
                text = msg.get("text", "")
                contents.append({"role": role, "parts": [{"text": text}]})
            
            # Get response
            response = model.generate_content(contents)
            reply = response.text
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'reply': reply}).encode())
            
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'reply': 'Yo bro! 😅 Having some technical issues right now!'
            }).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
