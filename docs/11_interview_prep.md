# 11. Interview Preparation

## 1. Explain your project.
**HR version:** "I built a Weather Forecast & Alert Application in Python. It takes a city, fetches live weather from the OpenWeatherMap API, analyses the 5-day forecast, and warns the user about risks like heavy rain, heat, strong wind or poor air quality. It saves reports and charts, has an optional dashboard, and works offline through a simulation mode."
**Technical version:** "A modular pipeline: `weather_api` calls REST endpoints with `requests`; `parser` converts JSON to dicts and a Pandas DataFrame; `analyzer` builds daily summaries; `alerts` applies configurable thresholds with severity levels; `visualizer` makes Matplotlib charts; `report` writes CSV/JSON/TXT; `notifier` sends email via SMTP. Config and secrets come from `.env`. A simulation module generates data in the same JSON shape so the whole system is testable without internet, and unit tests cover alert rules."

## 2. How does the app talk to the weather service?
It sends HTTP GET requests with parameters (city, key, units) to REST endpoints and gets JSON back. I use a timeout and check status codes (401, 404, 429).

## 3. How do you keep the API key safe?
It lives in `.env`, loaded by python-dotenv; `.env` is in `.gitignore`; the repo has `.env.example` only.

## 4. How are alerts generated?
Rule-based comparisons against a `Thresholds` dataclass. Severity is CRITICAL if the value exceeds the limit by 15%. Repeated forecast alerts are merged so the user sees one alert per type.

## 5. Why Pandas?
The forecast is 40 time-stamped rows. Pandas makes grouping by day, min/max/mean and CSV export a few lines.

## 6. What is simulation mode and why did you build it?
It produces fake but realistic data in the real API format, so I can develop, test and demo without a key or internet, and force scenarios (storm, heatwave) to prove every alert works.

## 7. How do you handle errors?
A custom `WeatherAPIError` converts network failures, bad keys, unknown cities, rate limits and bad JSON into clear messages. Parser functions raise `ValueError` for unexpected formats. The email notifier never crashes the app.

## 8. How would you make this production-ready?
Wrap the pipeline in a FastAPI service, store history in PostgreSQL, schedule runs with cron/Celery, add SMS/Telegram, cache API responses, add logging, CI with GitHub Actions and Docker.

## 9. What challenges did you face?
Nested JSON and missing keys, 3-hour data needing daily aggregation, alert spam (solved by merging), unit mismatches (solved with `units=metric`), and keeping secrets out of Git.

## 10. How did you test it?
Unit tests for each alert rule and for the pipeline using simulation scenarios (`python -m unittest discover tests`).

## Bonus: What did you learn?
API integration, JSON parsing, Pandas, rule engines, modular design, secure configuration, Git workflow and documentation.
