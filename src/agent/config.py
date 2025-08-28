# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
