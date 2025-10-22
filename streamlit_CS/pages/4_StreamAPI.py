import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

st.set_page_config(page_title="Live API Demo", layout="wide")

st.title("📊 Live Streaming API Demos")
tabs = st.tabs(["💰 CoinGecko Prices", "🌤 Open-Meteo Weather"])


# CoinGecko Demo -------------------------------------------------
with tabs[0]:
    st.subheader("Live Crypto Prices (CoinGecko)")

    COINS = ["bitcoin", "ethereum"]
    VS = "usd"
    HEADERS = {"User-Agent": "msudenver-dataviz-class/1.0", "Accept": "application/json"}
    API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(COINS)}&vs_currencies={VS}"

    SAMPLE_DF = pd.DataFrame([
        {"coin": "bitcoin", VS: 68000},
        {"coin": "ethereum", VS: 3500},
    ])

    @st.cache_data(ttl=300)
    def fetch_prices(url: str):
        try:
            resp = requests.get(url, timeout=10, headers=HEADERS)
            if resp.status_code == 429:
                return None, "429 Too Many Requests"
            resp.raise_for_status()
            data = resp.json()
            df = pd.DataFrame(data).T.reset_index().rename(columns={"index": "coin"})
            return df, None
        except requests.RequestException as e:
            return None, f"Error: {e}"

    refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
    auto_refresh = st.toggle("Enable auto refresh", value=False)

    df, err = fetch_prices(API_URL)
    if err or df is None:
        st.warning(f"⚠️ Using fallback data: {err}")
        df = SAMPLE_DF.copy()

    st.dataframe(df, use_container_width=True)
    fig = px.bar(df, x="coin", y=VS, title=f"Current Price ({VS.upper()})")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Last updated at {time.strftime('%H:%M:%S')}")

    if auto_refresh:
        time.sleep(refresh_sec)
        st.rerun()


# Open-Meteo Weather Demo ----------------------------
with tabs[1]:
    st.subheader("Hourly Weather Forecast (Open-Meteo)")

    lat, lon = 39.7392, -104.9903  # Denver
    wurl = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,wind_speed_10m"
        f"&timezone=America/Denver"
    )

    @st.cache_data(ttl=600)
    def get_weather():
        try:
            r = requests.get(wurl, timeout=10)
            r.raise_for_status()
            j = r.json()["hourly"]
            return pd.DataFrame({
                "time": pd.to_datetime(j["time"]),
                "temperature": j["temperature_2m"],
                "wind": j["wind_speed_10m"]
            }), None
        except requests.RequestException as e:
            return None, f"Error: {e}"

    weather_df, werr = get_weather()
    if werr or weather_df is None:
        st.error(f"Weather API error: {werr}")
    else:
        st.dataframe(weather_df.tail(24), use_container_width=True)
        fig = px.line(
            weather_df,
            x="time",
            y="temperature",
            title="Temperature (°C) Over Time (Hourly)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Last updated at {time.strftime('%H:%M:%S')}")

        refresh_weather = st.toggle("Auto refresh weather", value=False)
        if refresh_weather:
            time.sleep(60)
            st.rerun()
