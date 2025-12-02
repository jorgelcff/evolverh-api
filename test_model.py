import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Listar modelos disponíveis
for model in genai.list_models():
    print(f"Modelo: {model.name}")
    print(f"  Suportado: {model.supported_generation_methods}")
    print()