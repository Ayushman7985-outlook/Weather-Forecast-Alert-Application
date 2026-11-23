"""The full workflow in one function. Used by both main.py and the dashboard.

city -> fetch (API or simulation) -> parse -> analyse -> alerts -> result dict
"""
from . import alerts as alert_rules
from . import analyzer, parser, simulation, weather_api
from .config import Thresholds, get_api_key


def run_pipeline(city, mode="simulation", thresholds=None, scenario="normal"):
    thresholds = thresholds or Thresholds()

    # 1. Fetch raw data
    if mode == "api":
        key = get_api_key()
        if key is None:
            raise weather_api.WeatherAPIError(
                "No API key found. Add OPENWEATHER_API_KEY to your .env file, or use --mode simulation.")
        raw = weather_api.fetch_all(city, key)
    else:
        raw = simulation.generate(city, scenario)

    # 2. Parse JSON
    current = parser.parse_current(raw["current"])
    forecast_df = parser.parse_forecast(raw["forecast"])
    aqi = parser.parse_aqi(raw.get("aqi"))

    # 3. Analyse
    daily = analyzer.daily_summary(forecast_df)
    stats = analyzer.overall_stats(forecast_df)

    # 4. Alerts
    alerts = alert_rules.check_current(current, aqi, thresholds)
    alerts += alert_rules.check_forecast(forecast_df, thresholds)
    alerts = alert_rules.sort_alerts(alerts)

    return {"mode": mode, "scenario": scenario, "current": current, "aqi": aqi,
            "forecast_df": forecast_df, "daily": daily, "stats": stats,
            "alerts": alerts, "thresholds": thresholds}
