from langchain_core.tools import tool
from config import WEATHER_API
import requests

@tool
def weather(latitude: float, longitude: float):
    """Get current weather for the given latitude and longitude."""
    
    url = f"{WEATHER_API}&latitude={latitude}&longitude={longitude}"
    result = requests.get(url)
    data = result.json()
    current = data["current"]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "temperature": current["temperature_2m"],
        "units": "Celsius",
        "time": current["time"]
    }
