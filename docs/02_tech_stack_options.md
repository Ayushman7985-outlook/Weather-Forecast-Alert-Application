# 2. Tech Stack Options

| | Option A: Easy | Option B: Intermediate (Recommended) | Option C: Advanced |
|---|---|---|---|
| Tools | Python, requests, json, datetime | + Pandas, Matplotlib, python-dotenv, argparse, smtplib, simulation mode | + FastAPI backend, Streamlit/Next.js frontend, SQLite/PostgreSQL, Celery/cron, Twilio, Docker |
| Difficulty | Beginner | Lower-intermediate | Intermediate to advanced |
| Expected output | Terminal weather + simple alert text | Terminal report, CSV, charts, optional dashboard and email | Web dashboard, REST API, maps, stored history, scheduled push alerts |

## Best choice for students: Option B
It shows API integration, data handling, visualization and automation, which are the exact skills in Python Developer, Data Analyst and Automation job descriptions, without the setup burden of Option C. This repository implements Option B plus an optional Streamlit dashboard. To grow it toward Option C, wrap `src/pipeline.py` in a FastAPI endpoint.
