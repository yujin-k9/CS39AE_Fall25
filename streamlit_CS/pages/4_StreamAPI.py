import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

st.set_page_config(page_title="Live Crypto Prices", layout="wide")
st.title("💰 Live Crypto Prices (CoinGecko)")

COINS = ["bitcoin", "ethereum"]
VS = "usd"
HEADERS = {
    "User-Agent": "msudenver-dataviz-class/1.1",
    "Accept": "application/json",
    "Cache-Control": "no-cache"
}
API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(COINS)}&vs_currencies={VS}"

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

# initialize session history
if "price_history" not in st.session_state:
    st.session_state.price_history = pd.DataFrame(columns=["time", "bitcoin", "ethereum"])

refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)
auto_refresh = st.toggle("Enable auto refresh", value=False)

df, err = fetch_prices(API_URL)

if err or df is None:
    st.error(f"❌ Live API error: {err}")
else:
    # store one row per refresh
    current_time = time.strftime("%H:%M:%S")
    btc_price = df.loc[df["coin"] == "bitcoin", VS].values[0]
    eth_price = df.loc[df["coin"] == "ethereum", VS].values[0]

    new_row = {"time": current_time, "bitcoin": btc_price, "ethereum": eth_price}
    st.session_state.price_history.loc[len(st.session_state.price_history)] = new_row
    st.session_state.price_history = st.session_state.price_history.tail(12)

    st.subheader("Current Price (USD)")
    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="coin", y=VS, title="Current Prices (Bar View)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Last updated at {current_time}")

    st.subheader("Recent Price History (Newest First)")
    hist_df = st.session_state.price_history.iloc[::-1].reset_index(drop=True)
    st.dataframe(hist_df, use_container_width=True)
    st.caption("Note: Shows up to 12 most recent refresh intervals.")

if auto_refresh:
    time.sleep(refresh_sec)
    st.rerun()
