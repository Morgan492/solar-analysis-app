import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time

st.set_page_config(page_title="Solar & Battery Analysis Tool", layout="wide")
st.title("Solar & Battery Analysis Tool")

# Upload section
st.header("1. Upload Load Data")
uploaded_file = st.file_uploader("Upload your CSV load data (must contain 'datetime' and 'kwh' columns)", type=["csv"])

df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'datetime' in df.columns and 'kwh' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.time
        df['day'] = df['datetime'].dt.strftime('%a')
        st.success("File successfully uploaded and parsed.")
        st.line_chart(df.set_index('datetime')['kwh'])
    else:
        st.error("CSV must contain 'datetime' and 'kwh' columns.")

# DNSP and Tariff selection
st.header("2. Select DNSP and Tariff")
dnsp_options = ["Ausgrid", "Endeavour", "Essential Energy", "Energex"]
dnsp = st.selectbox("Distribution Network Service Provider (DNSP)", dnsp_options)

full_tariffs = {
    "Ausgrid": ["EA025", "EA116", "EA225", "EA256", "EA302", "EA305", "EA310"],
    "Endeavour": ["NS70", "NG90", "NS19"],
    "Essential Energy": ["BLNRSS2", "BLND1AR", "BLNBSS1", "BLND1AB", "BLND4SB", "BLND3AO", "BLND3TO", "BLND4LS"],
    "Energex": ["3600", "3700", "3800", "3900", "6000", "6800", "6900", "7100", "8400", "8500", "8800", "8900"]
}

default_tariff = {
    "Ausgrid": "EA225",
    "Endeavour": "NS70",
    "Essential Energy": "BLNBSS1",
    "Energex": "7100"
}

manual_override = st.checkbox("Manually select tariff code")
if manual_override:
    selected_tariff = st.selectbox("Select Tariff Code", full_tariffs[dnsp])
else:
    selected_tariff = default_tariff[dnsp]
    st.write(f"Auto-selected tariff for {dnsp}: **{selected_tariff}**")

# Tariff structure
st.subheader("Tariff Selection Summary")
st.write(f"**DNSP:** {dnsp}")
st.write(f"**Tariff Code:** {selected_tariff}")
if manual_override:
    st.write("Manual override enabled.")
else:
    st.write("Auto-selected based on DNSP.")

st.info("Detailed rate logic for each tariff will be applied in calculations.")
