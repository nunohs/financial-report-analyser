# test_models.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in client.models.list():
    if "flash" in model.name.lower() or "pro" in model.name.lower():
        print(model.name)