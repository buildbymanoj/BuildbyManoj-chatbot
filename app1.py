import os
import secrets
import requests
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from flask_session import Session

# ─── Load API Key ────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found in .env")

# ─── Initialize Flask ────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")

# ─── Configure Session ────────────────────────────
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(16))
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False  # Session ends when browser is closed
Session(app)

# ─── Model Choice ────────────────────────────────
MODEL = "deepseek/deepseek-chat-v3-0324"

# ─── Smart Web Search Trigger ────────────────────
def needs_web_search(msg: str) -> bool:
    msg = msg.lower()
    skip_keywords = [
        "hi", "hello", "hey", "how are you",
        "who are you", "your name",
        "thank you", "bye", "joke", "math"
    ]
    force_keywords = [
        "latest", "today", "news", "current",
        "2025", "now", "update", "who won", "president"
    ]

    if any(k in msg for k in force_keywords):
        return True
    if any(k in msg for k in skip_keywords):
        return False
    return len(msg.split()) > 5

# ─── DuckDuckGo Web Scraper ──────────────────────
def search_web(query, max_results=3):
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        snippets = soup.select('.result__snippet')

        results = [s.text.strip() for s in snippets[:max_results]]
        return "\n".join(results) if results else "[No relevant info found.]"
    except Exception as e:
        return f"[Web search failed: {str(e)}]"

# ─── OpenRouter Chat Call Using Requests ─────────
def call_openrouter_chat(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"[OpenRouter Error] {res.status_code}: {res.text}"
    except Exception as e:
        return f"[Request Error] {str(e)}"

# ─── Routes ───────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please enter a message."})
    
    # Initialize conversation history if it doesn't exist
    if "conversation" not in session:
        session["conversation"] = []
    
    # Prepare the message content based on whether web search is needed
    if needs_web_search(user_msg):
        web_data = search_web(user_msg)
        system_message = {
            "role": "system", 
            "content": "You are a helpful AI assistant with knowledge up to 2024. Use the web search information provided to give accurate and updated responses."
        }
        user_content = f"""
My question: {user_msg}

Web search results:
{web_data}

Please answer my question using this information.
"""
    else:
        system_message = {
            "role": "system", 
            "content": "You are a helpful AI assistant. Respond to the user's messages in a friendly and informative way."
        }
        user_content = user_msg
    
    # Build message history for the API call
    messages = [system_message]
    
    # Add previous conversation context (up to 10 most recent messages)
    for msg in session["conversation"][-10:]:
        messages.append(msg)
    
    # Add the current user message
    current_user_message = {"role": "user", "content": user_content}
    messages.append(current_user_message)
    
    # Store the user message in the conversation history
    session["conversation"].append({"role": "user", "content": user_msg})
    
    # Get reply from API
    reply = call_openrouter_chat(messages)
    
    # Store the assistant's reply in the conversation history
    session["conversation"].append({"role": "assistant", "content": reply})
    session.modified = True
    
    return jsonify({"reply": reply})

@app.route("/history", methods=["GET"])
def get_history():
    """Get the current conversation history from the session"""
    conversation = session.get("conversation", [])
    return jsonify({
        "history": conversation
    })

@app.route("/clear", methods=["POST"])
def clear_history():
    """Clear the conversation history"""
    session["conversation"] = []
    session.modified = True
    return jsonify({
        "status": "success",
        "message": "Conversation history cleared"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "OK",
        "model": MODEL
    })

# ─── Run Server ───────────────────────────────────
if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 10000))
    print(f"🔵 Running DeepSeek Chatbot with RAG at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)

