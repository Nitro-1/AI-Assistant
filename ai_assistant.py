
import os
import sys
import time
import threading
from datetime import datetime
from typing import Optional
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()


# Check for required libraries
try:
    import speech_recognition as sr
    import pyttsx3
    from google import genai
    VOICE_AVAILABLE = True
except ImportError as e:
    print(f"Some voice libraries missing: {e}")
    print("Assistant will run in text-only mode")
    VOICE_AVAILABLE = False

class AIAssistant:
    """
    AI Assistant with Gemini API and Voice Support
    """

    def __init__(self, api_key: str = None, voice_enabled: bool = True):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set GEMINI_API_KEY or pass api_key parameter.")

        self.voice_enabled = voice_enabled and VOICE_AVAILABLE
        self.conversation_history = []

        # Initialize Gemini
        self._initialize_gemini()

        # Initialize voice components
        if self.voice_enabled:
            self._initialize_voice()

    def _initialize_gemini(self):
        """Initialize Gemini API client"""
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.model = "gemini-2.5-flash"
            print("✅ Gemini API connected successfully")
        except Exception as e:
            print(f"❌ Gemini API connection failed: {e}")
            raise

    def _initialize_voice(self):
        """Initialize speech recognition and text-to-speech"""
        try:
            # Speech Recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.pause_threshold = 0.8

            # Text-to-Speech
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)

            # Try to set a pleasant voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break

            print("✅ Voice components initialized")

        except Exception as e:
            print(f"⚠️ Voice initialization failed: {e}")
            self.voice_enabled = False

    def speak(self, text: str):
        """Convert text to speech"""
        if not self.voice_enabled:
            return

        try:
            print(f"🤖 Assistant: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Speech error: {e}")

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input"""
        if not self.voice_enabled:
            return input("👤 You: ")

        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏱️ No speech detected")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None

    def get_ai_response(self, user_input: str) -> str:
        """Get response from Gemini AI"""
        try:
            # Build context from conversation history
            context = ""
            if self.conversation_history:
                context = "Previous conversation:\n"
                for user_msg, ai_msg in self.conversation_history[-3:]:  # Last 3 exchanges
                    context += f"User: {user_msg}\nAssistant: {ai_msg}\n"
                context += "\nCurrent question: "

            # System prompt
            system_prompt = """You are a helpful, friendly AI assistant. 
            Provide clear, concise responses. Be conversational and engaging.
            Keep responses reasonably short unless asked for detailed information."""

            full_prompt = f"{system_prompt}\n\n{context}{user_input}"

            # Get response from Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt
            )

            ai_response = response.text.strip()

            # Store in conversation history
            self.conversation_history.append((user_input, ai_response))

            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            return ai_response

        except Exception as e:
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            print(f"❌ AI Error: {e}")
            return error_msg

    def handle_commands(self, user_input: str) -> Optional[str]:
        """Handle special commands"""
        user_input = user_input.lower().strip()

        if any(cmd in user_input for cmd in ['exit', 'quit', 'goodbye', 'bye']):
            return "exit"

        elif any(cmd in user_input for cmd in ['help', 'what can you do']):
            return """I'm your AI assistant! I can:
            • Answer questions on various topics
            • Help with problem-solving
            • Engage in conversations
            • Remember our chat context

            Commands:
            • 'help' - Show this message
            • 'exit' or 'quit' - End conversation
            • 'clear' - Reset conversation history

            Just ask me anything!"""

        elif 'clear' in user_input:
            self.conversation_history.clear()
            return "Conversation history cleared! Starting fresh."

        return None

    def run_interactive_mode(self):
        """Run the interactive assistant"""
        print("\n" + "="*50)
        print("🤖 AI ASSISTANT STARTED")
        print("="*50)

        if self.voice_enabled:
            print("🎤 Voice mode available - you can speak or type")
        else:
            print("💬 Text mode only")

        print("📝 Say 'help' for commands or 'exit' to quit")
        print("="*50)

        # Greeting
        greeting = "Hello! I'm your AI assistant. How can I help you today?"
        self.speak(greeting)

        while True:
            try:
                # Get user input
                if self.voice_enabled:
                    print("\nChoose input method:")
                    print("1. 🎤 Voice")
                    print("2. 💬 Text")
                    choice = input("Your choice (1/2): ").strip()

                    if choice == '1':
                        user_input = self.listen()
                    else:
                        user_input = input("👤 Type your message: ")
                else:
                    user_input = input("\n👤 You: ")

                if not user_input:
                    continue

                # Handle commands
                command_response = self.handle_commands(user_input)
                if command_response == "exit":
                    farewell = "Goodbye! It was great chatting with you!"
                    self.speak(farewell)
                    break
                elif command_response:
                    self.speak(command_response)
                    continue

                # Get AI response
                print("\n🤔 Thinking...")
                ai_response = self.get_ai_response(user_input)

                # Respond
                self.speak(ai_response)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                self.speak("I encountered an error. Let's try again.")

def main():
    """Main function"""
    print("🚀 Starting AI Assistant...")

    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n❌ API key not found!")
        print("Please:")
        print("1. Get your API key from: https://ai.google.dev/")
        print("2. Create a .env file in this folder")
        print("3. Add: GEMINI_API_KEY=your_api_key_here")

        # Allow manual entry
        api_key = input("\nOr enter your API key now: ").strip()
        if not api_key:
            print("❌ API key required. Exiting.")
            return

    try:
        # Create and run assistant
        assistant = AIAssistant(api_key=api_key, voice_enabled=True)
        assistant.run_interactive_mode()

    except Exception as e:
        print(f"❌ Failed to start assistant: {e}")
        print("\nTroubleshooting:")
        print("• Check your internet connection")
        print("• Verify your API key is correct")
        print("• Make sure all libraries are installed")

if __name__ == "__main__":
    main()
