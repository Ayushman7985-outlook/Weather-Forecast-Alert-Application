"""Weather Forecast & Alert Application - command line entry point.

Examples:
  python main.py --mode simulation --city Varanasi
  python main.py --mode simulation --city Mumbai --scenario storm
  python main.py --mode api --city Delhi --heat 40 --email
"""
import argparse
import sys

from src import simulation
from src.config import Thresholds
from src.notifier import send_email_alert
from src.pipeline import run_pipeline
from src.report import build_text_report, save_reports
from src.visualizer import plot_alert_summary, plot_forecast
from src.weather_api import WeatherAPIError


def parse_args():
    p = argparse.ArgumentParser(description="Weather Forecast & Alert Application")
    p.add_argument("--city", help="City name (asked interactively if omitted)")
    p.add_argument("--mode", choices=["api", "simulation"], default="simulation",
                   help="api = live OpenWeatherMap data, simulation = built-in sample data")
    p.add_argument("--scenario", choices=simulation.SCENARIOS, default="normal",
                   help="Simulation only: force a weather situation to test alerts")
    p.add_argument("--heat", type=float, default=38.0, help="Heat alert threshold in °C")
    p.add_argument("--cold", type=float, default=5.0, help="Cold alert threshold in °C")
    p.add_argument("--humidity", type=float, default=85.0, help="Humidity alert threshold in %%")
    p.add_argument("--wind", type=float, default=10.0, help="Wind alert threshold in m/s")
    p.add_argument("--rain-prob", type=float, default=60.0, help="Rain probability threshold in %%")
    p.add_argument("--no-chart", action="store_true", help="Skip chart generation")
    p.add_argument("--email", action="store_true", help="Email the report if alerts exist")
    return p.parse_args()


def main():
    args = parse_args()
    city = args.city or input("Enter city name (e.g. Varanasi): ").strip()
    if not city:
        print("City name cannot be empty.")
        return 1

    thresholds = Thresholds(heat_temp_c=args.heat, cold_temp_c=args.cold,
                            humidity_pct=args.humidity, wind_speed_ms=args.wind,
                            rain_prob_pct=args.rain_prob)
    try:
        result = run_pipeline(city, args.mode, thresholds, args.scenario)
    except (WeatherAPIError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    print(build_text_report(result))
    paths = save_reports(result)
    print("\nSaved files:")
    for name, path in paths.items():
        print(f"  {name:<13}: {path}")
    if not args.no_chart:
        chart = plot_forecast(result["forecast_df"], result["current"]["city"], thresholds)
        summary = plot_alert_summary(result["alerts"], result["current"]["city"])
        print(f"  forecast chart: {chart}\n  alert chart   : {summary}")

    if args.email and result["alerts"]:
        ok, msg = send_email_alert(f"Weather alerts for {result['current']['city']}",
                                   build_text_report(result))
        print(f"\n{msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
