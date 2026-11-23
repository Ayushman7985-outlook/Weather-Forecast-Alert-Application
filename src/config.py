"""Configuration: loads the API key / email settings from the .env file."""
import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
IMAGE_DIR = BASE_DIR / "images"
REPORT_DIR = BASE_DIR / "reports"
DATA_DIR = BASE_DIR / "data"

try:  # python-dotenv is optional; plain environment variables still work
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


def get_api_key():
    """Return the OpenWeatherMap API key, or None if not set."""
    key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not key or key == "your_api_key_here":
        return None
    return key


def get_email_settings():
    """Return email settings dict, or None if not configured."""
    sender = os.getenv("EMAIL_SENDER", "").strip()
    password = os.getenv("EMAIL_PASSWORD", "").strip()
    receiver = os.getenv("EMAIL_RECEIVER", "").strip()
    if not (sender and password and receiver) or "your_" in password:
        return None
    return {
        "sender": sender,
        "password": password,
        "receiver": receiver,
        "server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
    }


@dataclass
class Thresholds:
    """Alert thresholds. Users can change these from the CLI or dashboard."""
    heat_temp_c: float = 38.0      # >= this -> heat alert
    cold_temp_c: float = 5.0       # <= this -> cold alert
    humidity_pct: float = 85.0     # >= this -> humidity alert
    wind_speed_ms: float = 10.0    # >= this (m/s) -> wind alert
    rain_prob_pct: float = 60.0    # >= this -> rain alert
    rain_mm: float = 10.0          # >= this mm per 3h -> heavy rain alert
    aqi_level: int = 4             # >= this (1 good ... 5 very poor) -> AQI alert
