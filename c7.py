import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

emission_factors= {
    "Fossil Fuels": {
        "CNG": 2.21,  # kg CO₂ per Kg
        "Petrol/Gasoline": 2.31,
        "Diesel": 2.68,
        "PNG": 2.30,
        "LPG": 2.98
    },
    "Electricity": {
        "Coal/Thermal": 0.85,  # kg CO₂ per kWh
        "Solar": 0  # No emissions
    },
    "Travel": {
        "Airways": 0.133,  # kg CO₂ per km
        "Roadways": 0.271,
        "Railways": 0.041
    }
}

# Global Warming Potential (GWP) values for fugitive emission
f_e_f = {
    "Domestic Refrigeration": 1430,  # Example: R-134a
    "Commercial Refrigeration": 3922,  # Example: R-404A
    "Industrial Refrigeration": 1774,  # Example: R-410A
    "Residential and Commercial A/C": 2088  # Example: R-407C
}

# Emission factors for different electricity sources (kg CO₂ per kWh)
e_e_f = {
    "Coal/Thermal": 0.92,  # High emissions
    "Solar": 0.05  # Almost negligible emissions
}

# Emission factor for water (kg CO₂e per cubic meter)
w_e_f = 0.344
# Emission factors (kg CO₂e per kg of waste) by waste and treatment type
wa_e_f = {
    "Household Residue": {"Landfills": 1.0, "Combustion": 0.7, "Recycling": 0.2},
    "Food and Drink Waste": {"Landfills": 1.9, "Combustion": 0.8, "Recycling": 0.3},
    "Garden Waste": {"Landfills": 0.6, "Combustion": 0.4, "Recycling": 0.2},
    "Commercial and Industrial Waste": {"Landfills": 2.0, "Combustion": 1.5, "Recycling": 0.6}
}

# Offset factors (approximate, per unit per month)
of_e_f = {
    "tree": 21.77 / 12,              # Monthly offset per tree
    "soil": 0.5,                     # kg CO₂e/m²/month
    "grass": 0.4,                    # kg CO₂e/m²/month
    "water": 0.3                     # kg CO₂e/m²/month
}



# Set Streamlit page config
st.set_page_config(layout="wide", page_title="Carbon Footprint Calculator")

# Initialize session state for slide tracking
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

# Define slides content
slides = [
    {"title": "Fossil Fuels", "content": "", "calculator": True},
    {"title": "Fugitive", "content": "How fugitive impacts the footprint"},
    {"title": "Electricity", "content": "electricity consumption details"},
    {"title": "Water", "content": "Water consumption details."},
    {"title": "Waste", "content": "Waste management insights."},
    {"title": "Travel", "content": "How travel impacts the footprint."},
    {"title": "Offset", "content": "Ways to offset carbon footprint."}
]

# Function to go to the next slide
def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1
# Function to go to the previous slide
def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

# Display current slide
current_slide = slides[st.session_state.slide_index]
st.title(current_slide["title"])
st.write(current_slide["content"])

# If the slide is "Fossil Fuels", show the Carbon Footprint Calculator
if current_slide["title"] == "Fossil Fuels":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility1 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year1 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month1 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader("Fuel Type")
        fuel_type1 = st.selectbox("", ["Choose Fuel Type", "CNG", "Petrol/Gasoline", "Diesel", "PNG", "LPG"])

        st.subheader("Unit")
        unit1 = st.selectbox("", ["Choose Unit", "Kg", "Tonne"])

        st.subheader("Amount Consumed")
        amount_consumed1 = st.number_input("Enter Amount", min_value=1, max_value=10000)

    if fuel_type1 != "Choose Fuel Type":
        factor = emission_factors["Fossil Fuels"][fuel_type1]
        if unit1 == "Tonne":
                amount_consumed1 *= 1000  # Convert to kg

        carbon_footprint = amount_consumed1 * factor

        st.subheader("Estimated Carbon Emission")
        st.write(f"Your estimated CO₂ emission: **{carbon_footprint:.2f} kg CO₂**")

        # Store in session state
        st.session_state["Fossil Fuels Emission"] = carbon_footprint


if current_slide["title"] == "Fugitive":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility2 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year2 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month2 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader("apllication type")
        application_type2 = st.selectbox("", ["Choose application Type", "Domestic Refrigeration", "Commercial Refrigeration", "Industrial Refrigeration", "Residential and Commercial A/C"])

        st.subheader("Units")
        unit2 = st.selectbox("", ["Choose Unit", "Kg", "Tonne"])

        st.subheader("number of units")
        amount_consumed2 = st.number_input("Enter number of units", min_value=1, max_value=10000)

    if application_type2 != "Choose application Type":
        gwp_factor = f_e_f[application_type2]  # Get GWP value
        amount_consumed2 *= 1000  # Convert tonnes to kg

        fugitive_emission = amount_consumed2 * gwp_factor  # Calculate CO₂ equivalent

        st.subheader("Estimated Carbon Emission")
        st.write(f"Your estimated CO₂ equivalent emission: **{fugitive_emission:.2f} kg CO₂**")

        # Store in session state for further calculations
        st.session_state["Fugitive Emission"] = fugitive_emission

if current_slide["title"] == "Electricity":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility3 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year3 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month3 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader("electricity type")
        electricity_type3 = st.selectbox("", ["Choose electricity Type", "Coal/Thermal", "Solar"])

        st.subheader("Electricity Source")
        elec_sou3=st.selectbox("",["Choose Electricity Source", "Purchased", "Self-Produced"])

        st.subheader("Unit")
        unit3 = st.selectbox("", ["Choose Unit", "KWH"])

        st.subheader("Amount Consumed")
        amount_consumed3 = st.number_input("Enter Amount", min_value=1, max_value=10000)

    if electricity_type3 != "Choose electricity Type":
        emission_factor = e_e_f[electricity_type3]  # Get emission factor
        electricity_emission = amount_consumed3 * emission_factor  # Calculate CO₂ equivalent

        st.subheader("Estimated Carbon Emission")
        st.write(f"Your estimated CO₂ equivalent emission: **{electricity_emission:.2f} kg CO₂**")

        # Store in session state for further calculations
        st.session_state["Electricity Emission"] = electricity_emission

if current_slide["title"] == "Water":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility4 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year4 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month4 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader("Water Type")
        fuel_type4 = st.selectbox("", ["Choose Water Type", "Supplied Water", "Treated water"])

        st.subheader("Discharge Site")
        dis_site4= st.text_input("Enter Discharge Site")

        st.subheader("Unit")
        unit4 = st.selectbox("", ["Choose Unit", "Cubic metre", "million litres"])

        st.subheader("Amount")
        amount_consumed4 = st.number_input("Enter Amount", min_value=1, max_value=10000)

    water_emission = 0
    if unit4 == "Cubic metre":
        water_emission = amount_consumed4 * w_e_f
    elif unit4 == "Million litres":
        # 1 million litre = 1000 m³
        water_emission = amount_consumed4 * 1000 * w_e_f

    st.subheader("Estimated Carbon Emission")
    st.write(f"Your estimated CO₂ equivalent emission from water usage is: **{water_emission:.2f} kg CO₂e**")

    st.session_state["Water Emission"] = water_emission

if current_slide["title"] == "Waste":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility5 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year5 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month5 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader("Waste Type")
        waste_type5 = st.selectbox("", ["Choose Waste Type", "Household Residue", "Food and Drink Waste", "Garden Waste", "Commercial and Industrial Waste"])

        st.subheader("Treatment Type")
        treatment_type5 =st.selectbox("", ["Chooose Treatment Type", "Landfills", "Combustion", "Recycling"])

        st.subheader("Unit")
        unit5 = st.selectbox("", ["Choose Unit", "Kg", "Tonne"])

        st.subheader("Amount")
        amount_consumed5 = st.number_input("Enter Amount", min_value=1, max_value=10000)
    emission_factor = wa_e_f.get(waste_type5, {}).get(treatment_type5, 0)
    amount_kg = amount_consumed5 * 1000 if unit5 == "Tonne" else amount_consumed5
    waste_emission = amount_kg * emission_factor

    st.subheader("Estimated Carbon Emission")
    st.write(f"Your estimated CO₂ equivalent emission from waste is: **{waste_emission:.2f} kg CO₂e**")

    st.session_state["Waste Emission"] = waste_emission

if current_slide["title"] == "Travel":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility6 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year6 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month6 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

    with col2:
        st.subheader(" Mode of Transport")
        travel_mode = st.selectbox("", ["Choose Mode of Transport", "Airways", "Roadways", "Railways"])

        st.subheader("Distance Travelled(KM)")
        travel_distance = st.number_input("Enter Approximate Distance", min_value=1, max_value=10000)

    if travel_mode != "Choose Mode of Transport":
        travel_factor = emission_factors["Travel"][travel_mode]
        travel_emission = travel_distance * travel_factor

        st.subheader("Estimated Carbon Emission")
        st.write(f"Your estimated CO₂ emission: **{travel_emission:.2f} kg CO₂**")

        # Store in session state
        st.session_state["Travel Emission"] = travel_emission

if current_slide["title"] == "Offset":
    st.header("Carbon Footprint Calculator")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Facility")
        facility7 = st.selectbox("", ["Choose Facility", "Residential Areas", "Hostels", "Academic Area",
                                    "Health Centre", "Schools", "Visitor's Hostel", "Servants Quarters", "Shops/Bank/PO"])

        st.subheader("Year")
        year7 = st.selectbox("", ["Choose Year", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"])

        st.subheader("Month")
        month7 = st.selectbox("", ["Choose Month", "January", "February", "March", "April", "May", "June",
                                  "July", "August", "September", "October", "November", "December"])

        st.subheader("Area Covered Under Water(m^2)")
        water_consum7 = st.number_input("water covered area Area", min_value=1, max_value=10000)

    with col2:
        st.subheader("Number of Trees in the Facility")
        trees_count7 = st.number_input("trees covered number", min_value=1, max_value=10000)

        st.subheader("Area Covered Under Soil(m^2)")
        soil_area7 = st.number_input("soil covered area Area", min_value=1, max_value=10000)

        st.subheader("Area Covered Under Grass(m^2)")
        grass_area7 = st.number_input("grass covered area Area", min_value=1, max_value=10000)

    tree_offset = trees_count7 * of_e_f["tree"]
    soil_offset = soil_area7 * of_e_f["soil"]
    grass_offset = grass_area7 * of_e_f["grass"]
    water_offset = water_consum7 * of_e_f["water"]

    total_offset = tree_offset + soil_offset + grass_offset + water_offset

    st.subheader("Estimated Offset")
    st.write(f"Your estimated **CO₂ offset** for this month is: **{total_offset:.2f} kg CO₂e**")
    st.session_state["Offset Emission"] = total_offset

# Navigation buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.slide_index > 0:
        st.button("Previous", on_click=prev_slide)
with col2:
    if st.session_state.slide_index < len(slides) - 1:
        st.button("Next", on_click=next_slide)

data = {
    "Factor": ["Fossil Fuels", "Fugitive", "Electricity", "Water", "Waste", "Travel", "Offset"],
    "Emissions (kg CO₂)": ["carbon_footprint", "fugitive_emission", "water_emission", "waste_emission", "travel_emission", "total_offset"]  # Offset is negative
}

# Convert to DataFrame
df = pd.DataFrame(data)

# **Fix: Convert negative values to zero for Pie Chart**
df_pie = df.copy()
df_pie["Emissions (kg CO₂)"] = df_pie["Emissions (kg CO₂)"].apply(lambda x: max(x, 0))

# Create Subplots for Bar Chart and Pie Chart
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Bar Chart
axes[0].bar(df["Factor"], df["Emissions (kg CO₂)"], color=['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'grey'])
axes[0].set_title("Carbon Footprint by Factor")
axes[0].set_ylabel("Emissions (kg CO₂)")
axes[0].set_xticklabels(df["Factor"], rotation=45)

# **Fixed Pie Chart (No Negative Values)**
colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'grey']
axes[1].pie(df_pie["Emissions (kg CO₂)"], labels=df_pie["Factor"], autopct='%1.1f%%', colors=colors, startangle=140)
axes[1].set_title("Carbon Emissions by various factors")

# Display the Graph in Streamlit
df = pd.DataFrame(data)

# ---------- Cleaned Pie Data ----------
df_pie = df.copy()
df_pie["Emissions (kg CO₂)"] = df_pie["Emissions (kg CO₂)"].apply(lambda x: max(x, 0))
df_pie_clean = df_pie.dropna(subset=["Emissions (kg CO₂)"])
df_pie_clean = df_pie_clean[df_pie_clean["Emissions (kg CO₂)"] > 0]
colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'grey']

# ---------- Navigation (Slide Selector) ----------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to:", [
    "📊 Emissions Charts",
    "📋 Emissions Table",
    "  Download Reports"
])

# ---------- Page 1: Charts ----------
if page == "📊 Emissions Charts":
    st.title("📊 Carbon Emissions - Charts")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar Chart
    axes[0].bar(df["Factor"], df["Emissions (kg CO₂)"], color=colors)
    axes[0].set_title("Carbon Footprint by Factor")
    axes[0].set_ylabel("Emissions (kg CO₂)")
    axes[0].set_xticks(range(len(df["Factor"])))
    axes[0].set_xticklabels(df["Factor"], rotation=45)

    # Pie Chart
    axes[1].pie(
        df_pie_clean["Emissions (kg CO₂)"],
        labels=df_pie_clean["Factor"],
        autopct='%1.1f%%',
        colors=colors[:len(df_pie_clean)],
        startangle=140
    )
    axes[1].set_title("Carbon Emissions by Various Factors")
    st.pyplot(fig)

# ---------- Page 2: Table ----------
elif page == "📋 Emissions Table":
    st.title("📋 Emissions Table")

    styled_df = df.style.format({"Emissions (kg CO₂)": "{:,.2f}"}).background_gradient(cmap='Oranges')
    st.dataframe(styled_df, use_container_width=True)

# ---------- Page 3: Downloads ----------
elif page == "  Download Reports":
    st.title("  Download Carbon Emissions Reports")

    # CSV
    csv = df.to_csv(index=False)
    st.download_button("📥 Download Emissions Report (CSV)", csv, "carbon_emissions_report.csv", "text/csv")

    # Chart Image
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].bar(df["Factor"], df["Emissions (kg CO₂)"], color=colors)
    axes[0].set_title("Carbon Footprint by Factor")
    axes[0].set_ylabel("Emissions (kg CO₂)")
    axes[0].set_yscale('log')
    axes[0].set_xticks(range(len(df["Factor"])))
    axes[0].set_xticklabels(df["Factor"], rotation=45)

    axes[1].pie(
        df_pie_clean["Emissions (kg CO₂)"],
        labels=df_pie_clean["Factor"],
        autopct='%1.1f%%',
        colors=colors[:len(df_pie_clean)],
        startangle=140
    )
    axes[1].set_title("Carbon Emissions by Various Factors")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    st.download_button("📸 Download Chart Image (PNG)", buf, "emissions_charts.png", "image/png")


