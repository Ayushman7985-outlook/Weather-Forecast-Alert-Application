"""Matplotlib charts saved as PNG files (no pop-up window needed)."""
import matplotlib
matplotlib.use("Agg")  # headless backend: works everywhere
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from .config import IMAGE_DIR, Thresholds


def plot_forecast(df, city, t: Thresholds, filename=None):
    """Temperature + humidity line chart and rain-probability bar chart."""
    IMAGE_DIR.mkdir(exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    ax1.plot(df["datetime"], df["temp_c"], color="tab:red", marker="o", ms=3, label="Temperature (°C)")
    ax1.axhline(t.heat_temp_c, color="darkred", ls="--", lw=1, label=f"Heat limit {t.heat_temp_c}°C")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title(f"5-Day Forecast: {city}")
    ax1b = ax1.twinx()
    ax1b.plot(df["datetime"], df["humidity_pct"], color="tab:blue", alpha=0.6, label="Humidity (%)")
    ax1b.set_ylabel("Humidity (%)")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax1b.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    ax1.grid(alpha=0.3)

    colors = ["tab:red" if p >= t.rain_prob_pct else "tab:cyan" for p in df["rain_prob_pct"]]
    ax2.bar(df["datetime"], df["rain_prob_pct"], width=0.1, color=colors)
    ax2.axhline(t.rain_prob_pct, color="navy", ls="--", lw=1, label=f"Rain alert at {t.rain_prob_pct}%")
    ax2.set_ylabel("Rain probability (%)")
    ax2.set_ylim(0, 105)
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%a %d\n%H:%M"))

    fig.tight_layout()
    path = IMAGE_DIR / (filename or f"{city.lower().replace(' ', '_')}_forecast.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_alert_summary(alerts, city, filename=None):
    """Simple bar chart: number of alerts by severity."""
    IMAGE_DIR.mkdir(exist_ok=True)
    levels = ["INFO", "WARNING", "CRITICAL"]
    counts = [sum(1 for a in alerts if a.severity == s) for s in levels]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(levels, counts, color=["tab:blue", "orange", "tab:red"])
    ax.set_title(f"Alerts by severity: {city}")
    ax.set_ylabel("Count")
    ax.set_yticks(range(0, max(counts + [1]) + 1))
    fig.tight_layout()
    path = IMAGE_DIR / (filename or f"{city.lower().replace(' ', '_')}_alerts.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
