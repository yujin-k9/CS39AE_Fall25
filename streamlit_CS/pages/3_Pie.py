import streamlit as st
import pandas as pd
import plotly.express as px

st.title("☕ Drink Sales Distribution")

DATA_PATH = "data/pie_demo.csv"

try:
    df = pd.read_csv(DATA_PATH)
    st.write("### Raw Data")
    st.dataframe(df)

    category_col = st.selectbox("Select category column:", df.columns, index=0)
    value_col = st.selectbox("Select value column:", df.columns, index=1)

    fig = px.pie(df, names=category_col, values=value_col, title="Drink Sales Distribution")
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error(f"File not found: `{DATA_PATH}`")
except Exception as e:
    st.error(f"Error loading data: {e}")

st.caption("Edit `data/pie_demo.csv` to see your drink data update here.")
