"""Turns raw API JSON into clean Python dicts and Pandas DataFrames."""
import pandas as pd

AQI_LABELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}


def parse_current(raw):
    """Extract the fields we need from the 'current weather' JSON."""
    try:
        return {
            "city": raw["name"],
            "country": raw.get("sys", {}).get("country", ""),
            "lat": raw.get("coord", {}).get("lat"),
            "lon": raw.get("coord", {}).get("lon"),
            "temp_c": float(raw["main"]["temp"]),
            "feels_like_c": float(raw["main"].get("feels_like", raw["main"]["temp"])),
            "humidity_pct": float(raw["main"]["humidity"]),
            "pressure_hpa": raw["main"].get("pressure"),
            "wind_ms": float(raw.get("wind", {}).get("speed", 0)),
            "condition": raw["weather"][0]["main"],
            "description": raw["weather"][0]["description"],
            "rain_mm": float(raw.get("rain", {}).get("1h", raw.get("rain", {}).get("3h", 0))),
        }
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ValueError(f"Unexpected current-weather format: {exc}")


def parse_forecast(raw):
    """Convert the forecast JSON into a DataFrame (one row per 3 hours)."""
    rows = []
    try:
        for item in raw["list"]:
            rows.append({
                "datetime": item["dt_txt"],
                "temp_c": float(item["main"]["temp"]),
                "humidity_pct": float(item["main"]["humidity"]),
                "wind_ms": float(item.get("wind", {}).get("speed", 0)),
                "rain_prob_pct": round(float(item.get("pop", 0)) * 100),
                "rain_mm": float(item.get("rain", {}).get("3h", 0)),
                "condition": item["weather"][0]["main"],
                "description": item["weather"][0]["description"],
            })
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ValueError(f"Unexpected forecast format: {exc}")
    df = pd.DataFrame(rows)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date
    return df


def parse_aqi(raw):
    """Return {'aqi': int, 'label': str, 'pm2_5': float} or None."""
    if not raw or not raw.get("list"):
        return None
    entry = raw["list"][0]
    level = int(entry["main"]["aqi"])
    return {"aqi": level, "label": AQI_LABELS.get(level, "Unknown"),
            "pm2_5": entry.get("components", {}).get("pm2_5")}
