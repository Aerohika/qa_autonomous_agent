import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# Gemini model name
GEMINI_MODEL_NAME = "gemini-1.5-flash"
