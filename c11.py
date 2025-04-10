import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Carbon Footprint Calculator")

st.markdown("---")
st.header("Fossil Fuels")

fuel_type = st.selectbox("Choose Fuel Type", ["Choose Fuel Type", "Petrol", "Diesel", "LPG", "CNG", "Coal"])
fuel_quantity = st.number_input("Enter quantity", min_value=0.0)

st.subheader("Units")
unit = st.selectbox("", ["Choose Unit", "Litre", "Kg"])

emissions = {}

if fuel_type != "Choose Fuel Type" and unit != "Choose Unit":
    emission_factors = {
        "Petrol": 2.31,
        "Diesel": 2.68,
        "LPG": 1.51,
        "CNG": 2.16,
        "Coal": 2.86,
    }
    emissions["Fossil Fuels"] = fuel_quantity * emission_factors[fuel_type]

st.markdown("---")
st.header("Fugitive Emissions")

fugitive_type = st.selectbox("Choose Type", ["Choose Type", "Refrigerants", "Industrial Gases"])
fugitive_quantity = st.number_input("Enter quantity", min_value=0.0, key="fugitive_qty")

unit2 = st.selectbox("", ["Choose Unit", "Kg", "Tonne"])

if fugitive_type != "Choose Type" and unit2 != "Choose Unit":
    fugitive_factors = {
        "Refrigerants": 1300,
        "Industrial Gases": 9000,
    }
    multiplier = 1 if unit2 == "Kg" else 1000
    emissions["Fugitive"] = fugitive_quantity * multiplier * fugitive_factors[fugitive_type]

st.markdown("---")
st.header("Electricity")

electricity_used = st.number_input("Electricity used (in kWh)", min_value=0.0)
if electricity_used:
    electricity_emission_factor = 0.85
    emissions["Electricity"] = electricity_used * electricity_emission_factor

st.markdown("---")
st.header("Water Consumption")

water_used = st.number_input("Water used (in KL)", min_value=0.0)
if water_used:
    water_emission_factor = 0.344
    emissions["Water"] = water_used * water_emission_factor

st.markdown("---")
st.header("Waste")

waste_type = st.selectbox("Choose Waste Type", ["Choose Waste Type", "Organic", "Plastic", "E-waste"])
waste_quantity = st.number_input("Enter quantity", min_value=0.0, key="waste_qty")

unit3 = st.selectbox("", ["Choose Unit", "Kg", "Tonne"])

if waste_type != "Choose Waste Type" and unit3 != "Choose Unit":
    waste_factors = {
        "Organic": 0.25,
        "Plastic": 6.0,
        "E-waste": 2.5,
    }
    multiplier = 1 if unit3 == "Kg" else 1000
    emissions["Waste"] = waste_quantity * multiplier * waste_factors[waste_type]

st.markdown("---")
st.header("Travel")

travel_mode = st.selectbox("Mode of Travel", ["Choose Mode", "Car", "Bus", "Train", "Flight"])
distance = st.number_input("Distance Travelled (in km)", min_value=0.0)

if travel_mode != "Choose Mode":
    travel_factors = {
        "Car": 0.21,
        "Bus": 0.05,
        "Train": 0.041,
        "Flight": 0.133,
    }
    emissions["Travel"] = distance * travel_factors[travel_mode]

st.markdown("---")
st.header("Carbon Offsets")

offset_quantity = st.number_input("Carbon offset (in Kg CO₂)", min_value=0.0)
if offset_quantity:
    emissions["Offset"] = -offset_quantity

st.markdown("---")
st.header("Summary")

categories = list(emissions.keys())
values = list(emissions.values())

df = pd.DataFrame({"Category": categories, "Emissions (kg CO₂)": values})
st.dataframe(df)

total = df["Emissions (kg CO₂)"].sum()
st.subheader(f"Total Carbon Footprint: {total:.2f} kg CO₂")

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#17becf']

fig, ax = plt.subplots()
df.plot(kind='bar', x='Category', y='Emissions (kg CO₂)', legend=False, ax=ax, color=colors[:len(df)])
plt.ylabel("Emissions (kg CO₂)")
plt.title("Carbon Footprint Summary")
st.pyplot(fig)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Summary CSV", data=csv, file_name="carbon_summary.csv", mime="text/csv")

