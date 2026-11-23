# 5. Installation Guide

## Python
Download Python 3.9+ from python.org. On Windows tick **"Add Python to PATH"**. Check with `python --version` (Windows) or `python3 --version` (Mac).

## Virtual environment
**Windows (PowerShell):**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
If activation is blocked: `Set-ExecutionPolicy -Scope Process RemoteSigned`

**Mac / Linux:**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Libraries
`requests, pandas, matplotlib, python-dotenv, streamlit` (all in `requirements.txt`).

## Storing the API key safely
1. Copy `.env.example` to `.env`.
2. Put your key in `.env` only.
3. Code reads it with `os.getenv` (see `src/config.py`).
4. `.gitignore` contains `.env`, so Git never uploads it.
5. Check before every push: `git status` must not list `.env`.
6. If a key leaks, delete it on the OpenWeatherMap dashboard and create a new one.
