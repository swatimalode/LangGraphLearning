from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
WEATHER_API = os.getenv("WEATHER_API")
GEOCODER_API = os.getenv("GEOCODER_API")
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES"))
SUMMERIZE_BATCH = int(os.getenv("SUMMERIZE_BATCH"))
MEMORY_PATH = os.getenv("MEMORY_PATH")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
THRESHOLD = float(os.getenv("THRESHOLD"))
UPDATE_THRESHOLD = float(os.getenv("UPDATE_THRESHOLD"))
USER_PATH = os.getenv("USER_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
OVERLAP_CHUNK_SIZE = int(os.getenv("OVERLAP_CHUNK_SIZE"))