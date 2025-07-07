#!/usr/bin/env python3
"""
Main Assistant Application with Integrated STT Communication
============================================================

This module implements the core assistant functionality with support for
receiving transcriptions from the standalone STT module through multiple
inter-process communication mechanisms.

Key Components:
- LLM processing using Ollama
- Text-to-Speech synthesis with KokoroTTS
- Multi-modal IPC receiver for STT data
- Real-time audio playback with pygame
- Web search integration for current information
"""

import ollama
import pytz
import requests
import threading
import time
import json
import socket
import os
import sys
import signal
import multiprocessing
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime
import soundfile as sf
import torch
import numpy as np
import pygame
import io
import logging

# Import KokoroTTS
from kokoro import KPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set environment variables for CPU-only execution
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["USE_CUDA"] = "0"
os.environ["FORCE_CPU"] = "1"

@dataclass
class STTMessage:
    """Data structure for STT communication messages"""
    timestamp: float
    text: str
    confidence: float
    is_final: bool
    device_info: str
    session_id: str

class STTReceiver:
    """
    Multi-modal receiver for STT transcriptions
    
    Supports multiple communication methods:
    - Socket-based networking for robust cross-process communication
    - Named pipes (FIFO) for high-performance local IPC
    - Message queues for guaranteed delivery
    """
    
    def __init__(self, method: str = "socket", port: int = 8888):
        """
        Initialize STT receiver interface
        
        Args:
            method: Communication protocol ('socket', 'pipe', 'queue')
            port: Network port for socket communication
        """
        self.method = method
        self.port = port
        self.pipe_path = "/tmp/stt_pipe"
        self.server_socket = None
        self.client_socket = None
        self.message_queue = None
        self.is_running = False
        self.callback_function = None
        
        # Threading for concurrent message handling
        self.receiver_thread = None
        self.message_buffer = []
        self.buffer_lock = threading.Lock()
        
    def set_callback(self, callback: Callable[[str], None]):
        """Set callback function for processing received transcriptions"""
        self.callback_function = callback
    
    def start_receiving(self):
        """Initialize receiver and start listening for STT messages"""
        try:
            if self.method == "socket":
                self._start_socket_server()
            elif self.method == "pipe":
                self._start_pipe_receiver()
            elif self.method == "queue":
                self._start_queue_receiver()
            else:
                raise ValueError(f"Unsupported communication method: {self.method}")
                
            self.is_running = True
            logger.info(f"STT receiver started with method: {self.method}")
            
        except Exception as e:
            logger.error(f"Failed to start STT receiver: {e}")
            raise
    
    def _start_socket_server(self):
        """Initialize socket server for network communication"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(1)
        
        logger.info(f"Socket server listening on port {self.port}")
        
        # Start receiver thread
        self.receiver_thread = threading.Thread(
            target=self._socket_receiver_loop,
            daemon=True
        )
        self.receiver_thread.start()
    
    def _socket_receiver_loop(self):
        """Main loop for socket-based message reception"""
        while self.is_running:
            try:
                logger.info("Waiting for STT module connection...")
                self.client_socket, addr = self.server_socket.accept()
                logger.info(f"STT module connected from {addr}")
                
                # Handle messages from connected client
                buffer = ""
                while self.is_running:
                    try:
                        data = self.client_socket.recv(1024).decode('utf-8')
                        if not data:
                            break
                        
                        buffer += data
                        
                        # Process complete messages (delimited by newlines)
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            if line.strip():
                                self._process_message(line.strip())
                                
                    except Exception as e:
                        logger.error(f"Error receiving socket data: {e}")
                        break
                
                # Close client connection
                if self.client_socket:
                    self.client_socket.close()
                    self.client_socket = None
                    logger.info("STT module disconnected")
                
            except Exception as e:
                logger.error(f"Socket server error: {e}")
                time.sleep(1)
    
    def _start_pipe_receiver(self):
        """Initialize named pipe receiver"""
        self.receiver_thread = threading.Thread(
            target=self._pipe_receiver_loop,
            daemon=True
        )
        self.receiver_thread.start()
    
    def _pipe_receiver_loop(self):
        """Main loop for pipe-based message reception"""
        while self.is_running:
            try:
                if os.path.exists(self.pipe_path):
                    with open(self.pipe_path, 'r') as pipe:
                        for line in pipe:
                            if line.strip():
                                self._process_message(line.strip())
                else:
                    time.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"Pipe receiver error: {e}")
                time.sleep(1)
    
    def _start_queue_receiver(self):
        """Initialize message queue receiver"""
        if not hasattr(self, 'message_queue') or self.message_queue is None:
            logger.error("Message queue not initialized")
            return
            
        self.receiver_thread = threading.Thread(
            target=self._queue_receiver_loop,
            daemon=True
        )
        self.receiver_thread.start()
    
    def _queue_receiver_loop(self):
        """Main loop for queue-based message reception"""
        while self.is_running:
            try:
                if self.message_queue:
                    message = self.message_queue.get(timeout=1)
                    self._process_stt_message(message)
            except:
                continue
    
    def _process_message(self, message_str: str):
        """Parse and process received message string"""
        try:
            message_data = json.loads(message_str)
            
            # Reconstruct STTMessage object
            stt_message = STTMessage(
                timestamp=message_data['timestamp'],
                text=message_data['text'],
                confidence=message_data['confidence'],
                is_final=message_data['is_final'],
                device_info=message_data['device_info'],
                session_id=message_data['session_id']
            )
            
            self._process_stt_message(stt_message)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse STT message: {e}")
        except Exception as e:
            logger.error(f"Error processing STT message: {e}")
    
    def _process_stt_message(self, message: STTMessage):
        """Process validated STT message"""
        # Log message details
        logger.info(f"Received STT: {message.text} (confidence: {message.confidence:.2f})")
        logger.debug(f"Device: {message.device_info}, Session: {message.session_id}")
        
        # Execute callback if available
        if self.callback_function and message.text.strip():
            try:
                self.callback_function(message.text)
            except Exception as e:
                logger.error(f"Error in STT callback: {e}")
    
    def stop_receiving(self):
        """Stop receiver and cleanup resources"""
        self.is_running = False
        
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        if self.message_queue:
            self.message_queue.close()
        
        # Wait for receiver thread to finish
        if self.receiver_thread and self.receiver_thread.is_alive():
            self.receiver_thread.join(timeout=2)
        
        logger.info("STT receiver stopped")

class Robo68Assistant:
    """
    Advanced AI Assistant with Multi-Modal Communication
    
    Core capabilities:
    - Natural language processing via Ollama LLM
    - High-quality speech synthesis using KokoroTTS
    - Real-time web search integration
    - Contextual time-based responses
    - Echo detection and feedback prevention
    """
    
    def __init__(self, stt_communication: str = "socket", stt_port: int = 8888):
        """
        Initialize assistant with comprehensive configuration
        
        Args:
            stt_communication: STT communication method
            stt_port: Network port for STT communication
        """
        # Core component initialization
        self.setup_kokoro_tts()
        self.setup_audio_playback()
        
        # Timezone configuration for contextual responses
        self.timezone = pytz.timezone('Asia/Kathmandu')  # UTC+5:45
        
        # Conversation state management
        self.conversation_active = True
        self.is_speaking = False
        self.last_response_text = ""
        
        # System prompt with comprehensive instructions
        self.system_prompt = """You are Vision, an advanced AI assistant with expertise in:
- General knowledge and educational content
- Emotional support and counseling guidance
- Health and wellness information
- Current events and real-time information
- Technical problem-solving and analysis

Communication guidelines:
- Provide concise, accurate responses (max 150 words)
- Maintain warm, empathetic tone
- Offer practical solutions and actionable advice
- Acknowledge limitations and suggest professional consultation when appropriate
- Adapt response style to user's emotional state and context"""
        
        # Device configuration for performance monitoring
        self.stt_device = "external_module"  # STT runs in separate process
        self.tts_device = "cpu"  # KokoroTTS forced to CPU
        self.llm_device = "cpu"  # Ollama server configuration
        
        # Initialize STT receiver
        self.stt_receiver = STTReceiver(stt_communication, stt_port)
        self.stt_receiver.set_callback(self.process_speech_input)
        
        # Performance metrics
        self.session_start_time = time.time()
        self.total_interactions = 0
        
    def setup_kokoro_tts(self):
        """Initialize KokoroTTS with optimized CPU configuration"""
        try:
            # Enforce CPU-only execution to prevent CUDA memory issues
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
            torch.set_default_device('cpu')
            
            # Clear any existing CUDA cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Initialize pipeline with explicit CPU specification
            self.kokoro_pipeline = KPipeline(
                lang_code='a',
                device='cpu'
            )
            
            # TTS configuration optimized for real-time performance
            self.tts_config = {
                'voice': 'af_sky',
                'sample_rate': 24000,
                'speed_factor': 1.0,
                'pitch_factor': 1.0,
                'device': 'cpu'
            }
            
            logger.info("KokoroTTS initialized successfully on CPU")
            
        except Exception as e:
            logger.error(f"KokoroTTS initialization failed: {e}")
            self.kokoro_pipeline = None
    
    def setup_audio_playback(self):
        """Initialize pygame mixer for high-quality audio playback"""
        try:
            pygame.mixer.init(
                frequency=24000,
                size=-16,
                channels=1,
                buffer=512
            )
            logger.info("Audio playback system initialized")
        except Exception as e:
            logger.error(f"Audio playback initialization failed: {e}")
    
    def get_current_time_greeting(self) -> str:
        """Generate contextual greeting based on current time"""
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
    
    def search_web(self, query: str) -> str:
        """
        Execute web search using DuckDuckGo API
        
        Args:
            query: Search query string
            
        Returns:
            Search results or error message
        """
        try:
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant information
                if data.get('Abstract'):
                    return data['Abstract']
                elif data.get('RelatedTopics') and len(data['RelatedTopics']) > 0:
                    return data['RelatedTopics'][0].get('Text', 'No relevant information found.')
                    
            return "I couldn't find current information on that topic."
            
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return f"Search functionality is currently unavailable: {str(e)}"
    
    def generate_llm_response(self, user_input: str) -> str:
        """
        Generate contextual response using Ollama LLM
        
        Args:
            user_input: User's input text
            
        Returns:
            Generated response from LLM
        """
        try:
            # Prepare enhanced prompt with context
            greeting = self.get_current_time_greeting()
            enhanced_prompt = f"{self.system_prompt}\n\nTime context: {greeting}\nUser input: {user_input}"
            
            # Generate response with optimized parameters
            response = ollama.generate(
                model='gemma3:1b',  # Lightweight model for real-time performance
                prompt=enhanced_prompt,
                options={
                    'temperature': 0.7,     # Balanced creativity/consistency
                    'top_p': 0.9,          # Nucleus sampling for quality
                    'max_tokens': 150,      # Concise responses
                    'repeat_penalty': 1.1   # Reduce repetition
                }
            )
            
            return response['response']
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return f"I'm having trouble processing that right now. Error: {str(e)}"
    
    def synthesize_speech(self, text: str) -> Optional[np.ndarray]:
        """
        Convert text to speech using KokoroTTS
        
        Args:
            text: Text to synthesize
            
        Returns:
            Audio data as numpy array or None if synthesis fails
        """
        if not self.kokoro_pipeline:
            logger.warning("KokoroTTS not available, skipping speech synthesis")
            return None
        
        try:
            # Clean and prepare text
            clean_text = text.strip()
            if not clean_text:
                return None
            
            # Ensure CPU-only execution context
            with torch.no_grad():
                torch.set_default_device('cpu')
                
                # Generate speech using Kokoro pipeline
                generator = self.kokoro_pipeline(
                    clean_text,
                    voice=self.tts_config['voice']
                )
                
                # Extract first generated audio segment
                for i, (gs, ps, audio) in enumerate(generator):
                    if i == 0:
                        # Convert to numpy array
                        if torch.is_tensor(audio):
                            audio = audio.cpu()
                            audio_data = audio.numpy().astype(np.float32)
                        else:
                            audio_data = np.array(audio, dtype=np.float32)
                        
                        # Apply speed adjustment if needed
                        if self.tts_config['speed_factor'] != 1.0:
                            audio_data = self.adjust_speech_speed(audio_data)
                        
                        # Clear CUDA cache
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
                        
                        return audio_data
                
                return None
            
        except Exception as e:
            logger.error(f"Speech synthesis error: {e}")
            return None
    
    def adjust_speech_speed(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Adjust speech speed using interpolation
        
        Args:
            audio_data: Original audio data
            
        Returns:
            Speed-adjusted audio data
        """
        speed_factor = self.tts_config['speed_factor']
        if speed_factor == 1.0:
            return audio_data
        
        # Resample for speed adjustment
        new_length = int(len(audio_data) / speed_factor)
        indices = np.linspace(0, len(audio_data) - 1, new_length)
        return np.interp(indices, np.arange(len(audio_data)), audio_data)
    
    def play_audio(self, audio_data: np.ndarray):
        """
        Play audio using pygame mixer
        
        Args:
            audio_data: Audio data to play
        """
        if audio_data is None:
            return
        
        try:
            # Convert to int16 for pygame compatibility
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Create audio buffer
            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, audio_int16, self.tts_config['sample_rate'], format='WAV')
            audio_buffer.seek(0)
            
            # Play audio
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()
            
            # Wait for playback completion
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
    
    def speak_text(self, text: str):
        """
        Complete text-to-speech pipeline
        
        Args:
            text: Text to speak
        """
        logger.info(f"Speaking: {text}")
        
        # Set speaking flag to prevent feedback
        self.is_speaking = True
        self.last_response_text = text.strip().lower()
        
        # Synthesize and play audio
        audio_data = self.synthesize_speech(text)
        self.play_audio(audio_data)
        
        # Wait for audio buffer to clear
        time.sleep(0.5)
        
        # Reset speaking flag
        self.is_speaking = False
    
    def is_echo_or_feedback(self, transcribed_text: str) -> bool:
        """
        Detect if transcribed text is echo from assistant's speech
        
        Args:
            transcribed_text: Text to analyze
            
        Returns:
            True if text appears to be echo/feedback
        """
        if not transcribed_text or not self.last_response_text:
            return False
            
        # Normalize texts for comparison
        clean_transcribed = transcribed_text.strip().lower()
        clean_last_response = self.last_response_text.strip().lower()
        
        # Calculate word overlap
        words_transcribed = set(clean_transcribed.split())
        words_response = set(clean_last_response.split())
        
        if len(words_transcribed) == 0:
            return False
            
        overlap = len(words_transcribed.intersection(words_response))
        overlap_ratio = overlap / len(words_transcribed)
        
        # Check for common echo patterns
        echo_patterns = [
            "good morning", "good afternoon", "good evening", "good night",
            "vision", "i'm here to help", "how can i assist",
            "take care", "goodbye", "self-care is important"
        ]
        
        pattern_matches = sum(1 for pattern in echo_patterns if pattern in clean_transcribed)
        
        return overlap_ratio > 0.7 or pattern_matches >= 2
    
    def process_speech_input(self, transcribed_text: str):
        """
        Process user speech input with comprehensive handling
        
        Args:
            transcribed_text: Transcribed speech text
        """
        # Skip if currently speaking or empty input
        if self.is_speaking or not transcribed_text.strip():
            return
            
        # Echo detection
        if self.is_echo_or_feedback(transcribed_text):
            logger.debug(f"Echo detected, ignoring: {transcribed_text[:50]}...")
            return
        
        logger.info(f"User said: {transcribed_text}")
        logger.info(f"[STT running on: {self.stt_device}]")
        
        # Increment interaction counter
        self.total_interactions += 1
        
        # Check for conversation termination
        termination_phrases = ['goodbye', 'bye', 'exit', 'stop', 'end conversation']
        if any(phrase in transcribed_text.lower() for phrase in termination_phrases):
            goodbye_message = "Goodbye! It was nice talking with you. Take care!"
            logger.info(f"Robo68: {goodbye_message}")
            self.speak_text(goodbye_message)
            self.conversation_active = False
            return
        
        # Determine if web search is needed
        search_keywords = ['current', 'latest', 'recent', 'today', 'news', 'weather']
        if any(keyword in transcribed_text.lower() for keyword in search_keywords):
            logger.info("Searching web for current information...")
            search_result = self.search_web(transcribed_text)
            llm_input = f"User question: {transcribed_text}\nCurrent information: {search_result}"
        else:
            llm_input = transcribed_text
        
        # Generate LLM response with timing
        logger.info(f"[LLM running on: {self.llm_device}]")
        llm_start = time.time()
        response = self.generate_llm_response(llm_input)
        llm_end = time.time()
        
        logger.info(f"Robo68: {response}")
        logger.info(f"LLM response time: {llm_end - llm_start:.2f} seconds")
        
        # Generate TTS response with timing
        logger.info(f"[TTS running on: {self.tts_device}]")
        tts_start = time.time()
        self.speak_text(response)
        tts_end = time.time()
        
        logger.info(f"TTS synthesis/playback time: {tts_end - tts_start:.2f} seconds")
    
    def start_session(self):
        """Start assistant session with STT communication"""
        logger.info("Initializing Robo68 Assistant with external STT module...")
        
        # Generate welcome message
        greeting = self.get_current_time_greeting()
        welcome_message = f"{greeting}! I'm Vision, your AI assistant. I'm here to help with questions, provide information, and offer support. How can I assist you today?"
        
        logger.info(f"Robo68: {welcome_message}")
        self.speak_text(welcome_message)
        
        # Start STT receiver
        try:
            self.stt_receiver.start_receiving()
            logger.info("STT receiver started successfully")
        except Exception as e:
            logger.error(f"Failed to start STT receiver: {e}")
            return False
        
        return True
    
    def run(self):
        """Main execution loop"""
        if not self.start_session():
            logger.error("Failed to start assistant session")
            return
        
        logger.info("Assistant ready. Listening for speech input...")
        logger.info("Press Ctrl+C to terminate session")
        
        try:
            # Main conversation loop
            while self.conversation_active:
                time.sleep(0.1)  # Prevent busy waiting
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources and display session summary"""
        logger.info("Cleaning up resources...")
        
        # Stop STT receiver
        if self.stt_receiver:
            self.stt_receiver.stop_receiving()
        
        # Cleanup pygame
        pygame.mixer.quit()
        
        # Display session summary
        session_duration = time.time() - self.session_start_time
        logger.info(f"Session duration: {session_duration:.2f} seconds")
        logger.info(f"Total interactions: {self.total_interactions}")
        
        logger.info("Robo68 Assistant session ended.")

def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown"""
    logger.info(f"Received signal {signum}, initiating shutdown...")
    sys.exit(0)

def main():
    """Main entry point with comprehensive error handling"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Robo68 AI Assistant")
    parser.add_argument("--stt-communication", default="socket",
                       choices=["socket", "pipe", "queue"],
                       help="STT communication method")
    parser.add_argument("--stt-port", type=int, default=8888,
                       help="STT communication port")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize assistant
        assistant = Robo68Assistant(
            stt_communication=args.stt_communication,
            stt_port=args.stt_port
        )
        
        # Run assistant
        assistant.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error("Make sure you have:")
        logger.error("1. Ollama installed and running with gemma3:1b model")
        logger.error("2. KokoroTTS installed: pip install kokoro-tts")
        logger.error("3. Required dependencies: pip install pygame soundfile pytz requests")
        logger.error("4. STT module running separately")
        sys.exit(1)

if __name__ == "__main__":
    main()