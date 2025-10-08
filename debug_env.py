import os
from dotenv import load_dotenv

print("=== DEBUGGING ENVIRONMENT VARIABLES ===")
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

print("\n--- Before loading .env ---")
print("API KEY before load_dotenv():", repr(os.getenv('GEMINI_API_KEY')))

# Load the .env file
load_dotenv()

print("\n--- After loading .env ---")
print("API KEY after load_dotenv():", repr(os.getenv('GEMINI_API_KEY')))

# Check if .env file exists and read its contents
print("\n--- Reading .env file directly ---")
try:
    with open('.env', 'r') as f:
        content = f.read()
        print("Contents of .env file:")
        print(repr(content))
except Exception as e:
    print("Error reading .env file:", e)

print("\n=== END DEBUG ===")
