import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

st.set_page_config(page_title="Current Weather", layout="wide")
st.title("🌤 Denver Hourly Temperature Trend (Open-Meteo)")

lat, lon = 39.7392, -104.9903
wurl = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={lat}&longitude={lon}"
    f"&hourly=temperature_2m,wind_speed_10m"
    f"&temperature_unit=fahrenheit"
    f"&timezone=America/Denver"
)

def get_recent_weather():
    r = requests.get(wurl, timeout=10)
    r.raise_for_status()
    j = r.json()["hourly"]
    df = pd.DataFrame({
        "time": pd.to_datetime(j["time"]),
        "temperature": j["temperature_2m"],
        "wind": j["wind_speed_10m"]
    })
    df["time"] = df["time"].dt.tz_localize("America/Denver", ambiguous="NaT", nonexistent="shift_forward")
    now_local = pd.Timestamp.now(tz="America/Denver")
    df = df[df["time"] <= now_local].tail(5)
    return df

refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto refresh", value=False)

try:
    df = get_recent_weather()
    st.dataframe(df, use_container_width=True)

    fig = px.line(df, x="time", y="temperature", title="Temperature (°F) Over Time (Recent 5 intervals)", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.caption(f"Last updated at {time.strftime('%H:%M:%S')}")
    st.caption("### Note:")
    st.caption("Open-Meteo provides hourly forecast data only (1-hour intervals).")
    st.caption("However, you can set a custom refresh interval between 10–120 seconds to automatically rerun the app and display the latest available forecast update.")
except requests.RequestException as e:
    st.error(f"Weather API error: {e}")

if auto_refresh:
    time.sleep(refresh_sec)
    st.rerun()
