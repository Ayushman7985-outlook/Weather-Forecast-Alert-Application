# 7. How to Run

```bash
# Simulation mode
python main.py --mode simulation --city Varanasi
python main.py --mode simulation --city Mumbai --scenario storm

# API mode (needs .env with your key)
python main.py --mode api --city Delhi

# Custom thresholds
python main.py --city Delhi --scenario heatwave --heat 40 --rain-prob 70

# Email alert (needs EMAIL_* in .env)
python main.py --city Mumbai --scenario storm --email

# Dashboard
streamlit run dashboard.py

# Tests
python -m unittest discover tests
```

## Expected terminal output
A report with CURRENT WEATHER, FORECAST SUMMARY (daily table) and ALERTS, followed by a "Saved files" list.

## Generated files
- `outputs/<city>_<timestamp>_forecast.csv`, `_daily_summary.csv`, `_alerts.csv`, `_current.json`
- `reports/<city>_<timestamp>_report.txt`
- `images/<city>_forecast.png`, `images/<city>_alerts.png`
