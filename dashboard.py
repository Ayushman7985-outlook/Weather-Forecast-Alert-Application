"""Optional Streamlit dashboard.  Run:  streamlit run dashboard.py"""
import pandas as pd
import streamlit as st

from src import simulation
from src.config import Thresholds
from src.pipeline import run_pipeline
from src.weather_api import WeatherAPIError

st.set_page_config(page_title="Weather Forecast & Alerts", page_icon="🌦️", layout="wide")
st.title("🌦️ Weather Forecast & Alert Application")

with st.sidebar:
    st.header("Settings")
    mode = st.radio("Data source", ["simulation", "api"])
    city = st.text_input("City", "Varanasi")
    scenario = "normal"
    if mode == "simulation":
        scenario = st.selectbox("Scenario", simulation.SCENARIOS)
        st.caption("Known cities: " + ", ".join(simulation.available_cities()))
    st.subheader("Alert thresholds")
    t = Thresholds(
        heat_temp_c=st.slider("Heat (°C)", 25, 50, 38),
        cold_temp_c=st.slider("Cold (°C)", -10, 15, 5),
        humidity_pct=st.slider("Humidity (%)", 50, 100, 85),
        wind_speed_ms=st.slider("Wind (m/s)", 3, 25, 10),
        rain_prob_pct=st.slider("Rain probability (%)", 10, 100, 60),
    )
    go = st.button("Get weather", type="primary")

if go or "result" not in st.session_state:
    try:
        st.session_state["result"] = run_pipeline(city, mode, t, scenario)
    except (WeatherAPIError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

r = st.session_state["result"]
cur, df = r["current"], r["forecast_df"]

st.subheader(f"📍 {cur['city']}, {cur['country']}  ({r['mode']} mode)")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Temperature", f"{cur['temp_c']:.1f} °C", f"feels {cur['feels_like_c']:.1f}")
c2.metric("Humidity", f"{cur['humidity_pct']:.0f} %")
c3.metric("Wind", f"{cur['wind_ms']:.1f} m/s")
c4.metric("Condition", cur["condition"])
c5.metric("Air quality", f"{r['aqi']['label']} ({r['aqi']['aqi']}/5)" if r["aqi"] else "N/A")

st.subheader("🚨 Alerts")
if not r["alerts"]:
    st.success("No alerts. Weather looks safe.")
for a in r["alerts"]:
    text = f"**{a.kind}** ({a.when}): {a.message}"
    {"CRITICAL": st.error, "WARNING": st.warning}.get(a.severity, st.info)(text)

left, right = st.columns(2)
with left:
    st.subheader("Temperature & humidity")
    st.line_chart(df.set_index("datetime")[["temp_c", "humidity_pct"]])
with right:
    st.subheader("Rain probability (%)")
    st.bar_chart(df.set_index("datetime")["rain_prob_pct"])

st.subheader("🗺️ Location")
if cur["lat"] is not None:
    st.map(pd.DataFrame({"lat": [cur["lat"]], "lon": [cur["lon"]]}))

st.subheader("Daily summary")
st.dataframe(r["daily"], use_container_width=True)
st.download_button("Download forecast CSV", df.drop(columns=["date"]).to_csv(index=False),
                   file_name=f"{cur['city']}_forecast.csv")
