"""Forecast analysis with Pandas: daily summary + simple statistics."""
import pandas as pd


def daily_summary(df):
    """Group the 3-hourly forecast into one row per day."""
    grouped = df.groupby("date")
    summary = pd.DataFrame({
        "min_temp_c": grouped["temp_c"].min().round(1),
        "max_temp_c": grouped["temp_c"].max().round(1),
        "avg_temp_c": grouped["temp_c"].mean().round(1),
        "avg_humidity_pct": grouped["humidity_pct"].mean().round(0),
        "max_wind_ms": grouped["wind_ms"].max().round(1),
        "max_rain_prob_pct": grouped["rain_prob_pct"].max(),
        "total_rain_mm": grouped["rain_mm"].sum().round(1),
        "main_condition": grouped["condition"].agg(lambda s: s.mode().iat[0]),
    })
    return summary.reset_index()


def overall_stats(df):
    """Headline numbers for the whole forecast window."""
    hottest = df.loc[df["temp_c"].idxmax()]
    return {
        "hottest_time": hottest["datetime"].strftime("%a %d %b %H:%M"),
        "hottest_temp_c": float(hottest["temp_c"]),
        "coldest_temp_c": float(df["temp_c"].min()),
        "avg_temp_c": round(float(df["temp_c"].mean()), 1),
        "avg_humidity_pct": round(float(df["humidity_pct"].mean()), 1),
        "total_rain_mm": round(float(df["rain_mm"].sum()), 1),
        "rainy_slots": int((df["rain_prob_pct"] >= 50).sum()),
        "max_wind_ms": float(df["wind_ms"].max()),
    }
