"""Fetches live data from the OpenWeatherMap API (metric units)."""
import requests

BASE = "https://api.openweathermap.org"
TIMEOUT = 10


class WeatherAPIError(Exception):
    """Raised for any API / network problem, with a friendly message."""


def _get(url, params):
    try:
        resp = requests.get(url, params=params, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError("No internet connection. Try --mode simulation.")
    except requests.exceptions.Timeout:
        raise WeatherAPIError("The weather server timed out. Try again.")
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError(f"Request failed: {exc}")

    if resp.status_code == 401:
        raise WeatherAPIError("Invalid API key (401). New keys can take ~2 hours to activate.")
    if resp.status_code == 404:
        raise WeatherAPIError("City not found (404). Check the spelling.")
    if resp.status_code == 429:
        raise WeatherAPIError("Too many requests (429). Wait a bit and retry.")
    if resp.status_code != 200:
        raise WeatherAPIError(f"API error {resp.status_code}: {resp.text[:150]}")
    try:
        return resp.json()
    except ValueError:
        raise WeatherAPIError("API returned invalid JSON.")


def fetch_current(city, api_key):
    return _get(f"{BASE}/data/2.5/weather",
                {"q": city, "appid": api_key, "units": "metric"})


def fetch_forecast(city, api_key):
    """5-day forecast in 3-hour steps (40 entries)."""
    return _get(f"{BASE}/data/2.5/forecast",
                {"q": city, "appid": api_key, "units": "metric"})


def fetch_air_quality(lat, lon, api_key):
    """Return air-pollution JSON, or None if it fails (AQI is optional)."""
    try:
        return _get(f"{BASE}/data/2.5/air_pollution",
                    {"lat": lat, "lon": lon, "appid": api_key})
    except WeatherAPIError:
        return None


def fetch_all(city, api_key):
    """Fetch current + forecast + AQI and return the raw JSON as a dict."""
    current = fetch_current(city, api_key)
    forecast = fetch_forecast(city, api_key)
    coord = current.get("coord", {})
    aqi = fetch_air_quality(coord.get("lat"), coord.get("lon"), api_key)
    return {"current": current, "forecast": forecast, "aqi": aqi}
