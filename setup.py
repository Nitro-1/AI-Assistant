# AI Assistant Setup Script
import os
import sys
import subprocess
import platform

def print_step(step, description):
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def run_command(command, description):
    print(f"\n⚡ {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            return True
        else:
            print(f"❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} detected")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} detected - need 3.8+")
        return False

def main():
    print("🚀 AI ASSISTANT SETUP")
    print("=" * 40)

    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python():
        print("\n❌ Please install Python 3.8 or higher from python.org")
        return

    # Step 2: Install system dependencies
    print_step(2, "Installing system dependencies")
    system = platform.system().lower()

    if system == "windows":
        print("📦 Windows: You may need Visual C++ Build Tools")
        print("If pyaudio fails, try: pip install pipwin && pipwin install pyaudio")
    elif system == "darwin":
        print("📦 macOS: Installing portaudio...")
        run_command("brew install portaudio", "Installing portaudio")
    elif system == "linux":
        print("📦 Linux: Installing audio libraries...")
        run_command("sudo apt-get update && sudo apt-get install -y portaudio19-dev python3-pyaudio", "Installing audio")

    # Step 3: Install Python packages
    print_step(3, "Installing Python packages")

    packages = [
        "google-genai>=1.4.0",
        "SpeechRecognition>=3.10.0", 
        "pyttsx3>=2.90",
        "python-dotenv>=1.0.0",
        "pyaudio>=0.2.11"
    ]

    failed = []
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            failed.append(package)

    # Step 4: Create environment file
    print_step(4, "Creating configuration file")

    env_content = '''# AI Assistant Configuration
# Get your API key from: https://ai.google.dev/
GEMINI_API_KEY=your_api_key_here

# Voice settings
VOICE_ENABLED=true
'''

    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file")

    # Final instructions
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETE!")
    print("="*50)

    if failed:
        print(f"⚠️ Some packages failed: {failed}")
        print("Assistant may work in text-only mode")

    print("\n📝 NEXT STEPS:")
    print("1. Get API key from: https://ai.google.dev/")
    print("2. Edit .env file - replace 'your_api_key_here' with your key")
    print("3. Run: python ai_assistant.py")
    print("\n🚀 Enjoy your AI Assistant!")

if __name__ == "__main__":
    main()
