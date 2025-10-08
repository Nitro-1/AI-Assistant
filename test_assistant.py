# Simple test for the AI Assistant
import os
from dotenv import load_dotenv
load_dotenv()

def test_assistant():
    print("🧪 Testing AI Assistant...")

    # Check if main file exists
    if not os.path.exists('ai_assistant.py'):
        print("❌ ai_assistant.py not found!")
        return False

    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Please set your API key in .env file")
        return False

    # Try to import and create assistant
    try:
        import sys
        sys.path.append('.')
        from ai_assistant import AIAssistant

        # Create assistant (text-only for testing)
        assistant = AIAssistant(api_key=api_key, voice_enabled=False)

        # Test a simple query
        response = assistant.get_ai_response("Hello, can you hear me?")
        if response:
            print("✅ AI Assistant is working!")
            print(f"Test response: {response[:100]}...")
            return True
        else:
            print("❌ No response from AI")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_assistant():
        print("\n🎉 Your AI Assistant is ready to use!")
        print("Run: python ai_assistant.py")
    else:
        print("\n❌ Setup needs attention. Check the errors above.")
