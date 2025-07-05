import ollama
import pyttsx3
import pytz
import requests
import threading
import time
from datetime import datetime
from RealtimeSTT import AudioToTextRecorder

class Robo68Assistant:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        self.timezone = pytz.timezone('Asia/Kathmandu')  # Nepal Standard Time (UTC+5:45)
        self.conversation_active = True
        self.system_prompt = """You are Robo68, a helpful AI assistant robot designed to provide engaging conversations, answer questions, and offer emotional support. You specialize in:
- General knowledge and information
- Emotional support and counseling guidance
- Health and wellness information
- Friendly, empathetic conversations

Always respond in a warm, supportive manner. Keep responses concise but helpful. If discussing health matters, remind users to consult healthcare professionals for serious concerns."""
        
    def setup_tts(self):
        # TTS engine configuration - modify voice properties here
        voices = self.tts_engine.getProperty('voices')
        if voices:
            self.tts_engine.setProperty('voice', voices[0].id)  # Change index for different voices
        self.tts_engine.setProperty('rate', 180)  # Adjust speech rate (150-200 recommended)
        self.tts_engine.setProperty('volume', 0.9)  # Adjust volume (0.0-1.0)
    
    def get_current_time_greeting(self):
        current_time = datetime.now(self.timezone)
        hour = current_time.hour
        
        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        elif 17 <= hour < 21:
            return "Good evening"
        else:
            return "Good night"
    
    def search_web(self, query):
        # Web search functionality - replace with preferred search API
        try:
            # Example using a simple search API (replace with actual API key/endpoint)
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('Abstract'):
                    return data['Abstract']
                elif data.get('RelatedTopics') and len(data['RelatedTopics']) > 0:
                    return data['RelatedTopics'][0].get('Text', 'No relevant information found.')
            return "I couldn't find current information on that topic."
        except:
            return "Search functionality is currently unavailable."
    
    def generate_llm_response(self, user_input):
        try:
            # Ollama LLM integration - ensure 'phi3:mini' model is available
            greeting = self.get_current_time_greeting()
            enhanced_prompt = f"{self.system_prompt}\n\nCurrent time context: {greeting}. User input: {user_input}"
            
            response = ollama.generate(
                model='phi3:mini',  # Change model name if using different model
                prompt=enhanced_prompt,
                options={
                    'temperature': 0.7,  # Adjust creativity (0.1-1.0)
                    'top_p': 0.9,
                    'max_tokens': 150  # Adjust response length
                }
            )
            return response['response']
        except Exception as e:
            return f"I'm having trouble processing that right now. Error: {str(e)}"
    
    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def process_speech_input(self, transcribed_text):
        print(f"User said: {transcribed_text}")
        
        # Check for conversation termination
        if any(phrase in transcribed_text.lower() for phrase in ['goodbye', 'bye', 'exit', 'stop', 'end conversation']):
            goodbye_message = "Goodbye! It was nice talking with you. Take care!"
            print(f"Robo68: {goodbye_message}")
            self.speak_text(goodbye_message)
            self.conversation_active = False
            return
        
        # Check if user is asking for current information that might need web search
        search_keywords = ['current', 'latest', 'recent', 'today', 'news', 'weather']
        if any(keyword in transcribed_text.lower() for keyword in search_keywords):
            search_result = self.search_web(transcribed_text)
            llm_input = f"User question: {transcribed_text}\nCurrent information: {search_result}"
        else:
            llm_input = transcribed_text
        
        # Generate LLM response
        response = self.generate_llm_response(llm_input)
        print(f"Robo68: {response}")
        
        # Convert to speech
        self.speak_text(response)
    
    def run(self):
        print("Initializing Robo68 Assistant...")
        greeting = self.get_current_time_greeting()
        welcome_message = f"{greeting}! I'm Robo68, your AI assistant. I'm here to help with questions, provide information, and offer support. How can I assist you today?"
        
        print(f"Robo68: {welcome_message}")
        self.speak_text(welcome_message)
        
        print("Listening... (Say 'goodbye' to end)")
        
        # Initialize real-time speech recognition
        recorder = AudioToTextRecorder(
            model="base",
            language="en",
            post_speech_silence_duration=2,
            min_length_of_recording=1,
            min_gap_between_recordings=0.5,
            device="cpu",              # <-- Force CPU usage
            compute_type="float32"     # <-- (optional) Use float32 for best compatibility
        )
        
        while self.conversation_active:
            try:
                # Record and process speech
                recorder.text(self.process_speech_input)
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            except KeyboardInterrupt:
                print("\nConversation interrupted by user.")
                break
            except Exception as e:
                print(f"Error in speech processing: {e}")
                continue
        
        print("Robo68 Assistant session ended.")

def main():
    try:
        assistant = Robo68Assistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to initialize Robo68 Assistant: {e}")
        print("Make sure you have:")
        print("1. Ollama installed and running with phi3:mini model")
        print("2. Required audio dependencies installed")
        print("3. Microphone access enabled")

if __name__ == "__main__":
    main()