import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Loads your .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

for m in models:
    print(m.name, "supports generation:" if "generateContent" in m.supported_generation_methods else "no generation support")
