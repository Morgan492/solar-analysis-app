
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Solar & Battery Analysis Tool", layout="wide")

st.title("Solar & Battery Analysis Tool")

st.markdown("Upload your load data and configure your system settings below to estimate solar and battery performance.")

uploaded_file = st.file_uploader("Upload your CSV load data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'])
        st.success("File successfully uploaded and parsed.")
        st.line_chart(df.set_index('datetime')['kwh'])

solar_size = st.number_input("Solar System Size (kW)", value=100.0)
battery_size = st.number_input("Battery Capacity (kWh)", value=50.0)
grid_tariff = st.number_input("Grid Tariff ($/kWh)", value=0.22)
export_tariff = st.number_input("Export Tariff ($/kWh)", value=0.10)
self_consumption = st.slider("Estimated Self-Consumption (%)", 0, 100, 85)

if st.button("Run Analysis"):
    solar_yield = 1330
    gen = solar_size * solar_yield
    self_cons = gen * (self_consumption / 100)
    export = gen - self_cons
    battery_saving = battery_size * 365 * 0.9 * grid_tariff
    savings = self_cons * grid_tariff
    export_income = export * export_tariff
    total = savings + export_income + battery_saving

    st.metric("Annual Generation (kWh)", f"{gen:,.0f}")
    st.metric("Savings from Self-Consumption ($)", f"{savings:,.0f}")
    st.metric("Export Income ($)", f"{export_income:,.0f}")
    st.metric("Battery Savings ($)", f"{battery_saving:,.0f}")
    st.metric("Total Annual Benefit ($)", f"{total:,.0f}")
