"""Alert rules: compares weather values against thresholds."""
from dataclasses import dataclass, asdict

from .config import Thresholds

SEVERITY_ORDER = {"CRITICAL": 3, "WARNING": 2, "INFO": 1}


@dataclass
class Alert:
    kind: str        # HEAT, COLD, RAIN, STORM, WIND, HUMIDITY, AQI
    severity: str    # INFO / WARNING / CRITICAL
    when: str        # "Now" or a forecast time
    message: str

    def to_dict(self):
        return asdict(self)


def _severity(value, threshold, margin=0.15):
    """CRITICAL if the value exceeds the threshold by 15%+, else WARNING."""
    return "CRITICAL" if value >= threshold * (1 + margin) else "WARNING"


def check_current(cur, aqi, t: Thresholds):
    """Check the current observation and return a list of Alerts."""
    alerts = []
    if cur["temp_c"] >= t.heat_temp_c:
        alerts.append(Alert("HEAT", _severity(cur["temp_c"], t.heat_temp_c), "Now",
                            f"High temperature {cur['temp_c']:.1f}°C (limit {t.heat_temp_c}°C). Stay hydrated, avoid midday sun."))
    if cur["temp_c"] <= t.cold_temp_c:
        alerts.append(Alert("COLD", "WARNING", "Now",
                            f"Low temperature {cur['temp_c']:.1f}°C (limit {t.cold_temp_c}°C). Dress warmly."))
    if cur["humidity_pct"] >= t.humidity_pct:
        alerts.append(Alert("HUMIDITY", "WARNING", "Now",
                            f"Humidity {cur['humidity_pct']:.0f}% (limit {t.humidity_pct}%). It will feel muggy."))
    if cur["wind_ms"] >= t.wind_speed_ms:
        alerts.append(Alert("WIND", _severity(cur["wind_ms"], t.wind_speed_ms), "Now",
                            f"Strong wind {cur['wind_ms']:.1f} m/s (limit {t.wind_speed_ms} m/s). Secure loose objects."))
    if cur["condition"] in ("Thunderstorm", "Tornado", "Squall"):
        alerts.append(Alert("STORM", "CRITICAL", "Now",
                            f"Storm conditions: {cur['description']}. Stay indoors."))
    elif cur["condition"] in ("Rain", "Drizzle"):
        alerts.append(Alert("RAIN", "INFO", "Now", f"It is raining now ({cur['description']}). Carry an umbrella."))
    if aqi and aqi["aqi"] >= t.aqi_level:
        alerts.append(Alert("AQI", "CRITICAL" if aqi["aqi"] == 5 else "WARNING", "Now",
                            f"Air quality is {aqi['label']} (AQI {aqi['aqi']}/5). Limit outdoor activity, wear a mask."))
    return alerts


def check_forecast(df, t: Thresholds):
    """Check each forecast slot; merge repeated alerts to keep output short."""
    found = {}  # kind -> (worst alert, number of slots)
    for _, row in df.iterrows():
        when = row["datetime"].strftime("%a %d %b %H:%M")
        slot = []
        if row["temp_c"] >= t.heat_temp_c:
            slot.append(Alert("HEAT", _severity(row["temp_c"], t.heat_temp_c), when,
                              f"Heat expected: {row['temp_c']:.1f}°C"))
        if row["temp_c"] <= t.cold_temp_c:
            slot.append(Alert("COLD", "WARNING", when, f"Cold expected: {row['temp_c']:.1f}°C"))
        if row["humidity_pct"] >= t.humidity_pct:
            slot.append(Alert("HUMIDITY", "INFO", when, f"High humidity expected: {row['humidity_pct']:.0f}%"))
        if row["wind_ms"] >= t.wind_speed_ms:
            slot.append(Alert("WIND", _severity(row["wind_ms"], t.wind_speed_ms), when,
                              f"Strong wind expected: {row['wind_ms']:.1f} m/s"))
        if row["condition"] == "Thunderstorm":
            slot.append(Alert("STORM", "CRITICAL", when, f"Thunderstorm expected ({row['rain_prob_pct']:.0f}% chance)"))
        elif row["rain_mm"] >= t.rain_mm:
            slot.append(Alert("RAIN", "CRITICAL", when, f"Heavy rain expected: {row['rain_mm']:.1f} mm in 3h"))
        elif row["rain_prob_pct"] >= t.rain_prob_pct:
            slot.append(Alert("RAIN", "WARNING", when, f"Rain likely: {row['rain_prob_pct']:.0f}% chance"))

        for a in slot:
            old = found.get(a.kind)
            if old is None:
                found[a.kind] = [a, 1]
            else:
                old[1] += 1
                if SEVERITY_ORDER[a.severity] > SEVERITY_ORDER[old[0].severity]:
                    old[0] = a
    alerts = []
    for a, n in found.values():
        extra = f" [{n} forecast slots affected]" if n > 1 else ""
        alerts.append(Alert(a.kind, a.severity, a.when, a.message + extra))
    return alerts


def sort_alerts(alerts):
    return sorted(alerts, key=lambda a: -SEVERITY_ORDER[a.severity])
