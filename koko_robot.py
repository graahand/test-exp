import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import pyttsx3
from RealtimeSTT import AudioToTextRecorder
try:
    from googlesearch import search
except ImportError:
    search = None

# --- Configuration (customize as needed) ---
MODEL_NAME = "phi3:mini"  # Ollama model name; change to the desired LLM
SYSTEM_PROMPT = "You are Robo68, a friendly helpful assistant providing answers and emotional support."  # System prompt
EXIT_PHRASES = ["exit", "quit", "goodbye", "bye"]  # Words to end conversation

# Initialize text-to-speech engine
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 25)       # Adjust speech rate if desired
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)   # Select voice index (0=male on many systems)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_llm_response(user_text):
    """Call local LLM via Ollama HTTP API and return the response."""
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
    }
    try:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
    except Exception as e:
        return f"Sorry, I couldn't get a response from the model ({e})."

def web_search(query):
    """Perform a web search and return top results."""
    if search is None:
        return "Search functionality is not available."
    try:
        results = list(search(query, num_results=3))
    except Exception:
        return "Search failed. Please check your internet connection or query."
    if not results:
        return "No results found."
    # Combine links or results for output; this could be improved to fetch summaries.
    reply = "Here are some search results: "
    reply += " ; ".join(results)
    return reply

def get_greeting():
    """Return a greeting based on Nepal Standard Time."""
    now = datetime.now(ZoneInfo("Asia/Kathmandu"))
    hour = now.hour
    if hour < 12:
        return "Good morning!"
    elif hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def process_text(text):
    """Handle the transcribed user text: check for exit or search, then respond."""
    user_text = text.strip()
    if not user_text:
        return
    print(f"User said: {user_text}")
    lower = user_text.lower()

    # Check for exit condition
    if any(phrase in lower for phrase in EXIT_PHRASES):
        farewell = "Goodbye! It was nice talking to you."
        print(f"Bot: {farewell}")
        speak(farewell)
        exit()

    # Check for search command
    if lower.startswith("search"):
        # Assume format: "search <query>"
        query = user_text[len("search"):].strip()
        answer = web_search(query)
    else:
        # Normal conversation via LLM
        answer = get_llm_response(user_text)

    print(f"Bot: {answer}")
    speak(answer)

if __name__ == "__main__":
    # Initial greeting
    greeting = get_greeting() + " I am Robo68. How can I assist you today?"
    print(greeting)
    speak(greeting)

    # Start listening loop (RealtimeSTT will prompt "speak now")
    recorder = AudioToTextRecorder()
    print("Say something (say 'goodbye' to exit).")
    while True:
        recorder.text(process_text)
