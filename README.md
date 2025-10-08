# AI Assistant

A **Python-based AI Assistant** that can chat via text or voice, remember conversation context, and generate intelligent responses using Google’s Gemini AI. Compatible with Windows, Mac, and Linux.

## Features

- **Text and Voice Interaction**: Choose between typing or speaking your queries.
- **Context Memory**: Maintains conversation context for follow-up questions.
- **Google Gemini Integration**: Leverages Google’s Gemini API for advanced AI responses.
- **Cross-Platform**: Runs on Windows, macOS, and Linux.
- **Easy Setup**: Automated installer script to get you up and running quickly.

## Prerequisites

- Python 3.8 or newer installed and added to your PATH.
- A Google Gemini API key.

## Installation

1. **Clone or Download** this repository into a folder named `AI_Assistant` on your Desktop.
2. Ensure the following files are present in the `AI_Assistant` folder:
   ```
   ├── ai_assistant.py
   ├── setup.py
   ├── requirements.txt
   ├── test_assistant.py
   └── .env
   ```

3. Open a terminal or Command Prompt and navigate to the project directory:
   ```bash
   # Windows
   cd Desktop\AI_Assistant
   
   # macOS/Linux
   cd Desktop/AI_Assistant
   ```

4. Run the setup script to install required Python packages:
   ```bash
   python setup.py
   ```

## Configuration

1. Obtain your Gemini API key from https://ai.google.dev/.
2. Open the `.env` file in the project folder.
3. Replace the placeholder with your actual API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
4. Save and close the file.

## Running Tests

Verify the setup:
```bash
python test_assistant.py
```
You should see a success message indicating the assistant is working correctly.

## Usage

Start the AI Assistant:
```bash
python ai_assistant.py
```

Upon launch, select interaction mode:

- **1**: Voice input (speak your questions)
- **2**: Text input (type your questions)

### Commands

- `help`: Show available commands.
- `clear`: Reset conversation memory.
- `exit` or `quit`: End the session.

### Example Queries

- "Hello, how are you?"
- "What can you help me with?"
- "Tell me about artificial intelligence"
- "What's 15 times 23?"

## Project Structure

- **ai_assistant.py**: Main application handling AI requests, voice input/output, and memory.
- **setup.py**: Installs dependencies automatically.
- **requirements.txt**: Lists required Python packages:  
  - `google-genai>=1.4.0`  
  - `SpeechRecognition>=3.10.0`  
  - `pyttsx3>=2.90`  
  - `pyaudio>=0.2.11`  
  - `python-dotenv>=1.0.0`  
  - `colorama>=0.4.6`
- **test_assistant.py**: Simple script to validate the environment and API key.
- **.env**: Stores sensitive configuration like the Gemini API key.

## Troubleshooting

- **`python` not recognized**: Add Python to PATH or use `python3`.
- **Audio errors (`pyaudio`)**:  
  - **Windows**: `pip install pipwin` then `pipwin install pyaudio`  
  - **macOS**: `brew install portaudio` then `pip install pyaudio`  
  - **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev`
- **API key issues**: Ensure `.env` has the correct key and no extra spaces.
- **Microphone not detected**: Check system permissions or switch to text mode.

## License

Distributed under the MIT License. See `LICENSE` for more information.
