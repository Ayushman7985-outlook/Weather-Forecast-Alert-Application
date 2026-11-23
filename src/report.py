"""Saves CSV / JSON / text reports to the outputs/ and reports/ folders."""
import json
from datetime import datetime

import pandas as pd

from .config import OUTPUT_DIR, REPORT_DIR


def _stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_reports(result):
    """Write forecast CSV, daily summary CSV, alerts CSV and a text report.
    Returns a dict of file paths."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    city = result["current"]["city"].lower().replace(" ", "_")
    tag = f"{city}_{_stamp()}"

    forecast_csv = OUTPUT_DIR / f"{tag}_forecast.csv"
    daily_csv = OUTPUT_DIR / f"{tag}_daily_summary.csv"
    alerts_csv = OUTPUT_DIR / f"{tag}_alerts.csv"
    json_path = OUTPUT_DIR / f"{tag}_current.json"
    report_txt = REPORT_DIR / f"{tag}_report.txt"

    result["forecast_df"].drop(columns=["date"]).to_csv(forecast_csv, index=False)
    result["daily"].to_csv(daily_csv, index=False)
    pd.DataFrame([a.to_dict() for a in result["alerts"]],
                 columns=["kind", "severity", "when", "message"]).to_csv(alerts_csv, index=False)
    json_path.write_text(json.dumps({**result["current"], "aqi": result["aqi"]}, indent=2))
    report_txt.write_text(build_text_report(result), encoding="utf-8")
    return {"forecast_csv": forecast_csv, "daily_csv": daily_csv, "alerts_csv": alerts_csv,
            "json": json_path, "report": report_txt}


def build_text_report(result):
    """Human-readable report (also used for printing and e-mail)."""
    cur, stats = result["current"], result["stats"]
    line = "=" * 62
    out = [line,
           f" WEATHER FORECAST & ALERT REPORT - {cur['city']}, {cur['country']}",
           f" Mode: {result['mode'].upper()}   Generated: {datetime.now():%Y-%m-%d %H:%M}",
           line, "", "CURRENT WEATHER",
           f"  Condition   : {cur['condition']} ({cur['description']})",
           f"  Temperature : {cur['temp_c']:.1f}°C (feels like {cur['feels_like_c']:.1f}°C)",
           f"  Humidity    : {cur['humidity_pct']:.0f}%",
           f"  Wind        : {cur['wind_ms']:.1f} m/s"]
    if result["aqi"]:
        out.append(f"  Air Quality : {result['aqi']['label']} (AQI {result['aqi']['aqi']}/5)")
    out += ["", "FORECAST SUMMARY (next 5 days)",
            f"  Hottest     : {stats['hottest_temp_c']:.1f}°C on {stats['hottest_time']}",
            f"  Coldest     : {stats['coldest_temp_c']:.1f}°C",
            f"  Avg temp    : {stats['avg_temp_c']}°C   Avg humidity: {stats['avg_humidity_pct']}%",
            f"  Total rain  : {stats['total_rain_mm']} mm   Max wind: {stats['max_wind_ms']} m/s", "",
            "  Date        Min   Max  Hum%  Rain%  Rain mm  Condition"]
    for _, d in result["daily"].iterrows():
        out.append(f"  {str(d['date'])}  {d['min_temp_c']:>5.1f} {d['max_temp_c']:>5.1f} "
                   f"{d['avg_humidity_pct']:>4.0f} {d['max_rain_prob_pct']:>6.0f} "
                   f"{d['total_rain_mm']:>8.1f}  {d['main_condition']}")
    out += ["", f"ALERTS ({len(result['alerts'])})"]
    if result["alerts"]:
        for a in result["alerts"]:
            out.append(f"  [{a.severity:<8}] {a.kind:<8} {a.when}: {a.message}")
    else:
        out.append("  No alerts. Weather looks safe.")
    out.append(line)
    return "\n".join(out)
