import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Streamlit App Config
st.set_page_config(layout="wide", page_title="Carbon Footprint Calculator")

st.title("Carbon Footprint Calculator")

# --- User Inputs ---
st.sidebar.header("Input Data")
st.sidebar.subheader("Fossil Fuels")
fuel_type = st.sidebar.selectbox("Select Fuel Type", ["CNG", "Petrol", "Diesel", "LPG", "PNG"])
fuel_amount = st.sidebar.number_input("Amount Consumed (Kg or L)", min_value=0.0, max_value=10000.0, value=10.0)

st.sidebar.subheader("Fugitive Emissions")
application_type = st.sidebar.selectbox("Application Type", ["Domestic Refrigeration", "Industrial Refrigeration", "AC Units"])
units_leaked = st.sidebar.number_input("Refrigerant Leaked (Kg)", min_value=0.0, max_value=1000.0, value=5.0)

st.sidebar.subheader("Electricity Usage")
electricity_source = st.sidebar.selectbox("Electricity Source", ["Coal", "Solar", "Wind"])
electricity_used = st.sidebar.number_input("Electricity Used (KWH)", min_value=0.0, max_value=100000.0, value=500.0)

st.sidebar.subheader("Water Usage")
water_used = st.sidebar.number_input("Water Consumed (m³)", min_value=0.0, max_value=100000.0, value=100.0)

st.sidebar.subheader("Waste Generation")
waste_type = st.sidebar.selectbox("Waste Type", ["Household", "Industrial", "Food Waste"])
waste_generated = st.sidebar.number_input("Waste Amount (Kg)", min_value=0.0, max_value=10000.0, value=50.0)

st.sidebar.subheader("Travel")
travel_mode = st.sidebar.selectbox("Mode of Transport", ["Car", "Airplane", "Train"])
distance_traveled = st.sidebar.number_input("Distance Traveled (Km)", min_value=0.0, max_value=100000.0, value=100.0)

st.sidebar.subheader("Offset (CO₂ Reduction)")
trees_planted = st.sidebar.number_input("Number of Trees Planted", min_value=0, max_value=10000, value=10)
soil_covered = st.sidebar.number_input("Soil Area Covered (m²)", min_value=0, max_value=100000, value=50)

# --- Emission Factors (Kg CO₂ per unit) ---
emission_factors = {
    "CNG": 2.75, "Petrol": 2.31, "Diesel": 2.68, "LPG": 3.00, "PNG": 2.45,
    "Domestic Refrigeration": 1430, "Industrial Refrigeration": 3922, "AC Units": 2088,
    "Coal": 0.9, "Solar": 0.0, "Wind": 0.0,
    "Household": 1.2, "Industrial": 2.5, "Food Waste": 1.8,
    "Car": 0.2, "Airplane": 0.25, "Train": 0.06
}

# --- Carbon Footprint Calculation ---
emissions = {
    "Fossil Fuels": fuel_amount * emission_factors[fuel_type],
    "Fugitive Emissions": units_leaked * emission_factors[application_type],
    "Electricity": electricity_used * emission_factors[electricity_source],
    "Water": water_used * 0.5,  # Example Factor: 0.5 Kg CO₂ per m³ of water
    "Waste": waste_generated * emission_factors[waste_type],
    "Travel": distance_traveled * emission_factors[travel_mode],
    "Offset": -(trees_planted * 22 + soil_covered * 0.3)  # 1 tree absorbs 22 Kg CO₂ per year
}

# Convert Emissions to DataFrame
df = pd.DataFrame(emissions.items(), columns=["Factor", "Emissions (kg CO₂)"])

# --- Graphical Representation ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar Chart
axes[0].bar(df["Factor"], df["Emissions (kg CO₂)"], color=['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'grey'])
axes[0].set_title("Carbon Footprint by Factor")
axes[0].set_ylabel("Emissions (kg CO₂)")
axes[0].set_xticklabels(df["Factor"], rotation=45)

# **Fix for Pie Chart (No Negative Values)**
df_pie = df.copy()
df_pie["Emissions (kg CO₂)"] = df_pie["Emissions (kg CO₂)"].apply(lambda x: max(x, 0))

# Pie Chart
colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'grey']
axes[1].pie(df_pie["Emissions (kg CO₂)"], labels=df_pie["Factor"], autopct='%1.1f%%', colors=colors, startangle=140)
axes[1].set_title("Percentage Contribution (No Negatives)")

# Display Graphs
st.pyplot(fig)

# Display Data Table
st.subheader("Calculated Carbon Footprint Data")
st.dataframe(df)

# Total Emissions
total_emissions = df["Emissions (kg CO₂)"].sum()
st.subheader(f"🌍 Total Carbon Footprint: {total_emissions:.2f} kg CO₂")


