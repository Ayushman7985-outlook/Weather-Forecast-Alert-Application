"""Virtual simulation: generates realistic weather data in the SAME JSON format
as the OpenWeatherMap API, so the rest of the code works unchanged.

Scenarios let you trigger alerts on purpose:
  normal | heatwave | storm | humid | polluted | cold
"""
import math
import random
from datetime import datetime, timedelta

# city -> (lat, lon, country, base temp C, daily swing C, humidity %, rain chance)
CITY_PROFILES = {
    "varanasi": (25.32, 82.97, "IN", 30, 7, 60, 0.15),
    "delhi":    (28.61, 77.21, "IN", 32, 8, 50, 0.10),
    "mumbai":   (19.08, 72.88, "IN", 30, 3, 78, 0.35),
    "chennai":  (13.08, 80.27, "IN", 32, 4, 72, 0.25),
    "kolkata":  (22.57, 88.36, "IN", 31, 5, 75, 0.30),
    "london":   (51.51, -0.13, "GB", 12, 4, 75, 0.35),
    "new york": (40.71, -74.01, "US", 15, 6, 60, 0.25),
    "dubai":    (25.20, 55.27, "AE", 38, 6, 50, 0.02),
}
SCENARIOS = ["normal", "heatwave", "storm", "humid", "polluted", "cold"]


def available_cities():
    return [c.title() for c in CITY_PROFILES]


def _profile(city):
    key = city.strip().lower()
    if key in CITY_PROFILES:
        return CITY_PROFILES[key]
    # Unknown city: build a repeatable pseudo-random profile from its name
    rng = random.Random(key)
    return (rng.uniform(-40, 60), rng.uniform(-120, 120), "XX",
            rng.randint(10, 34), rng.randint(3, 8), rng.randint(40, 80),
            rng.uniform(0.05, 0.4))


def _slot(rng, hour, base, swing, hum, rain_chance, scenario):
    """Build one 3-hourly weather slot."""
    diurnal = math.cos(2 * math.pi * (hour - 15) / 24)   # warmest at 15:00
    temp = base + swing * diurnal + rng.uniform(-1.5, 1.5)
    humidity = hum - 0.8 * swing * diurnal + rng.uniform(-5, 5)
    wind = rng.uniform(1.5, 6.5)

    roll = rng.random()
    if roll < rain_chance:
        cond, desc = "Rain", "moderate rain"
        pop, rain = rng.uniform(0.6, 0.95), rng.uniform(1, 8)
    elif roll < rain_chance + 0.35:
        cond, desc = "Clouds", "scattered clouds"
        pop, rain = rng.uniform(0.0, 0.3), 0.0
    else:
        cond, desc = "Clear", "clear sky"
        pop, rain = rng.uniform(0.0, 0.1), 0.0

    if scenario == "heatwave":
        temp += 8
        humidity -= 15
        cond, desc, pop, rain = "Clear", "clear sky", 0.0, 0.0
    elif scenario == "cold":
        temp -= 25
    elif scenario == "humid":
        humidity = rng.uniform(88, 98)
    elif scenario == "storm":
        wind = rng.uniform(11, 20)
        humidity = rng.uniform(85, 97)
        if rng.random() < 0.6:
            cond, desc = "Thunderstorm", "thunderstorm with heavy rain"
            pop, rain = rng.uniform(0.8, 1.0), rng.uniform(10, 25)
        else:
            cond, desc = "Rain", "heavy intensity rain"
            pop, rain = rng.uniform(0.7, 1.0), rng.uniform(5, 15)

    humidity = max(5, min(100, humidity))
    return {
        "main": {"temp": round(temp, 1),
                 "feels_like": round(temp + (humidity - 50) / 25, 1),
                 "humidity": round(humidity),
                 "pressure": rng.randint(1000, 1020)},
        "weather": [{"main": cond, "description": desc}],
        "wind": {"speed": round(wind, 1)},
        "pop": round(pop, 2),
        "rain": {"3h": round(rain, 1)} if rain else {},
    }


def generate(city, scenario="normal", seed=42):
    """Return {'current', 'forecast', 'aqi'} shaped like real API responses."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario '{scenario}'. Choose from {SCENARIOS}")
    lat, lon, country, base, swing, hum, rain_chance = _profile(city)
    rng = random.Random(f"{city.lower()}-{scenario}-{seed}")

    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    start = now - timedelta(hours=now.hour % 3)

    current = {
        "name": city.strip().title(), "coord": {"lat": lat, "lon": lon},
        "sys": {"country": country}, "dt": int(now.timestamp()),
        **_slot(rng, now.hour, base, swing, hum, rain_chance, scenario),
    }

    items = []
    for i in range(1, 41):  # 40 x 3h = 5 days, same as the real API
        t = start + timedelta(hours=3 * i)
        slot = _slot(rng, t.hour, base, swing, hum, rain_chance, scenario)
        slot["dt"] = int(t.timestamp())
        slot["dt_txt"] = t.strftime("%Y-%m-%d %H:%M:%S")
        items.append(slot)

    aqi_val = 5 if scenario == "polluted" else rng.choice([1, 2, 2, 3])
    aqi = {"list": [{"main": {"aqi": aqi_val},
                     "components": {"pm2_5": round(aqi_val * 28 + rng.uniform(0, 10), 1),
                                    "pm10": round(aqi_val * 40 + rng.uniform(0, 15), 1)}}]}
    return {
        "current": current,
        "forecast": {"city": {"name": current["name"], "coord": current["coord"],
                              "country": country}, "list": items},
        "aqi": aqi,
    }
