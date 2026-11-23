# 8. GitHub Upload Steps

**Repo name:** `Weather-Forecast-Alert-Application`
**Description:** Python weather forecast & alert system with OpenWeatherMap API, simulation mode, Pandas analysis, charts, reports and Streamlit dashboard.
**Topics/tags:** `python` `weather-api` `openweathermap` `alerts` `pandas` `matplotlib` `streamlit` `automation` `api-integration` `data-visualization` `student-project`

## Steps
1. On github.com click **New repository**, use the name above, keep it **Public**. Do not tick "Add README" (we have one).
2. In the project folder:
```bash
git init
git add .
git status            # CONFIRM .env is NOT listed
git commit -m "Initial commit: project structure and README"
git branch -M main
git remote add origin https://github.com/<your-username>/Weather-Forecast-Alert-Application.git
git push -u origin main
```
3. Upload screenshots to `images/`, then:
```bash
git add images outputs reports
git commit -m "docs: add screenshots and sample outputs"
git push
```

## Rules
- Never upload API keys. Commit `.env.example`, never `.env`.
- If you committed a key by mistake: revoke it immediately; deleting the file later is not enough because Git keeps history.

## Commit message style
`feat:` new feature, `fix:` bug fix, `docs:` documentation, `test:` tests, `refactor:` cleanup.
