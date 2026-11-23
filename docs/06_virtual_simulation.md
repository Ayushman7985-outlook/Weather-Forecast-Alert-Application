# 6. Virtual Simulation

No API key? Use `--mode simulation`.

- **Sample data:** `src/simulation.py` generates JSON in the exact OpenWeatherMap format (see `data/sample_weather_varanasi.json`).
- **City-wise data:** each city has a profile (base temperature, daily swing, humidity, rain chance). Unknown cities get a repeatable profile made from the name.
- **Thresholds:** the same `alerts.py` rules run on simulated data.
- **Scenarios** force situations so you can demonstrate every alert:

| Scenario | Triggers |
|---|---|
| normal | usually nothing or light rain |
| heatwave | HEAT |
| storm | STORM, WIND, RAIN, HUMIDITY |
| humid | HUMIDITY |
| polluted | AQI |
| cold | COLD |

- **Reports:** identical to API mode (CSV, JSON, TXT, PNG).
- **In real life:** swap simulation for the API call and schedule the script every few hours with cron or Windows Task Scheduler. Alerts go out by email/SMS/Telegram.

## Capture and upload
Screenshots: terminal output for normal + storm scenarios, forecast chart, CSV opened in Excel, dashboard.
Upload: screenshots, sample CSV/report files, charts.
**Never upload:** `.env`, API keys, email passwords, personal email addresses, `venv/`.
