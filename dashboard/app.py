# dashboard/app.py

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# --- CONNECTION ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Edge Observability",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Edge Observability Dashboard")
st.caption("""Live metrics from Raspberry Pi — weather + system health
           The weather data is gathered with Detroit as the location""")

# --- LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM observability ORDER BY timestamp DESC LIMIT 500", conn)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["timestamp"])
    return df

df = load_data()

if df.empty:
    st.warning("No data yet — make sure your Pi is sending data.")
    st.stop()

# --- SPLIT INTO WEATHER AND SYSTEM ---
weather_df = df[df["source"] == "weather"].copy()
system_df = df[df["source"] == "system"].copy()

# --- LATEST SNAPSHOT ---
st.subheader("Latest Readings")
col1, col2, col3, col4, col5 = st.columns(5)

if not weather_df.empty:
    latest_weather = weather_df.iloc[0]
    col1.metric("🌡️ Temp (°C)", f"{latest_weather['temp_c']}°")
    col2.metric("💧 Humidity", f"{latest_weather['humidity_percent']}%")

if not system_df.empty:
    latest_system = system_df.iloc[0]
    col3.metric("🖥️ CPU", f"{latest_system['cpu_percent']}%")
    col4.metric("🧠 Memory", f"{latest_system['memory_percent']}%")
    col5.metric("💾 Disk", f"{latest_system['disk_percent']}%")

# --- CHARTS ---
st.subheader("System Metrics Over Time")

if not system_df.empty:
    st.line_chart(
        system_df.set_index("timestamp")[["cpu_percent", "memory_percent", "disk_percent"]]
    )

st.subheader("Weather Over Time (Detroit)")

if not weather_df.empty:
    st.line_chart(
        weather_df.set_index("timestamp")[["temp_c", "humidity_percent"]]
    )

# --- RAW DATA ---
with st.expander("View raw data"):
    st.dataframe(df)
