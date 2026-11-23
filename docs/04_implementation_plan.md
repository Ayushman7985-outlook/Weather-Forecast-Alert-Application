# 4. Implementation Plan

| Phase | What to do | Why | Expected output | Common beginner mistakes |
|---|---|---|---|---|
| 1 Setup | Install Python 3.9+, VS Code, Git; create venv | Isolated, repeatable environment | `python --version` works | Forgetting to activate the venv |
| 2 Folder creation | Create folders from the structure | Clean, professional repo | Empty skeleton | Everything in one file |
| 3 API key setup | Get OpenWeatherMap key, put in `.env` | Keep secrets out of code | `.env` + `.env.example` | Hardcoding the key; committing `.env`; using a key before it activates (401) |
| 4 Fetching | `requests.get` with `timeout` | Get live JSON | Raw JSON printed | No timeout; no status-code check |
| 5 Parsing | Read nested keys safely | Turn JSON into usable values | dict + DataFrame | `KeyError` on missing fields; Kelvin vs Celsius (use `units=metric`) |
| 6 Forecast analysis | Pandas groupby date | Daily min/max/avg | Daily summary table | Mixing UTC and local time |
| 7 Alert logic | Threshold `if` rules + severity | Core of the app | Alert list | Same alert repeated 20 times; magic numbers (use `Thresholds`) |
| 8 Visualization | Matplotlib line/bar charts | Patterns at a glance | PNG charts | `plt.show()` on a server (use `Agg` + `savefig`) |
| 9 Report generation | Save CSV/JSON/TXT with timestamps | Proof and audit trail | Files in `outputs/`, `reports/` | Overwriting old reports |
| 10 GitHub upload | `git init`, commit, push | Portfolio proof | Public repo | Pushing `.env`; no README |
