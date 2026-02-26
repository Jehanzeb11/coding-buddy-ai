import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"
MAX_TOKENS = 4096

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not present in .env file")

client = Groq(api_key=GROQ_API_KEY)