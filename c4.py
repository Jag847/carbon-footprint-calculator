import  streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import seaborn as sns
import plotly.express as px
import matplotlib.ticker as ticker
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
        "Solar": 0.00  # No emissions
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
        "Household Residue": {"Landfills": 1.0, "Combustion": 0.7, "Recycling": 0.2, "Composting": 0.1},
        "Food and Drink Waste": {"Landfills": 1.9, "Combustion": 0.8, "Recycling": 0.3, "Composting": 0.05},                                                  "Garden Waste": {"Landfills": 0.6, "Combustion": 0.4, "Recycling": 0.2, "Composting": 0.03},
    "Commercial and Industrial Waste": {"Landfills": 2.0, "Combustion": 1.5, "Recycling": 0.6, "Composting": 0.2}
}

# Offset factors (approximate, per unit per month)
of_e_f = {
    "tree": 1.75,              # Monthly offset per tree
    "soil": 0.0515,                     # kg CO₂e/m²/month
    "grass": 0.0309,                    # kg CO₂e/m²/month
    "water": 0.0412                     # kg CO₂e/m²/month
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
    {"title": "Offset", "content": "Ways to offset carbon footprint."},
    {"title": "Summary", "content": "Carbon Footprint Summary"}
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
        if unit2 == "Tonne":
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
    elif unit4 == "million litres":
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
        treatment_type5 =st.selectbox("", ["Chooose Treatment Type", "Landfills", "Combustion", "Recycling", "Composting"])

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

    st.session_state["trees_count7"] = trees_count7
    st.session_state["soil_area7"] = soil_area7
    st.session_state["grass_area7"] = grass_area7
    st.session_state["water_consum7"] = water_consum7


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
        st.button("submit", on_click=next_slide)

if current_slide["title"] == "Summary":
    st.header("Carbon Footprint Summary")

    emissions = {
        "Fossil Fuels": float(st.session_state.get("Fossil Fuels Emission", 0.0)),
        "Fugitive": float(st.session_state.get("Fugitive Emission", 0.0)),
        "Electricity": float(st.session_state.get("Electricity Emission", 0.0)),
        "Water": float(st.session_state.get("Water Emission", 0.0)),
        "Waste": float(st.session_state.get("Waste Emission", 0.0)),
        "Travel": float(st.session_state.get("Travel Emission", 0.0)),
    }

    offset = float(st.session_state.get("Offset Emission", 0.0))
    total_emission = sum(emissions.values())
    net_emission = total_emission - offset

    st.subheader("Emissions Breakdown")
    for category, value in emissions.items():
        st.write(f"**{category}:** {value:.2f} kg CO₂e")

    st.subheader("Total Emission (before offset)")
    st.write(f"**{total_emission:.2f} kg CO₂e**")

    st.subheader("Offset")
    st.write(f"**{offset:.2f} kg CO₂e**")

    st.subheader("Net Emission")
    st.success(f"**{net_emission:.2f} kg CO₂e**")

    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)    
    
    df = pd.DataFrame({
        "Category": list(emissions.keys()),
        "Emissions (kg CO₂)": list(emissions.values())
    })
    
# Create visualizations
    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)
# Data
    categories = ["Fossil Fuels", "Fugitive", "Electricity", "Water", "Waste", "Travel"]
    values = df["Emissions (kg CO₂)"]

    categories = list(emissions.keys())
    values = list(emissions.values())

    df = pd.DataFrame({"Category": categories, "Emissions (kg CO₂)": values})
    st.dataframe(df)

    total = df["Emissions (kg CO₂)"].sum()
    st.subheader(f"Total Carbon Footprint: {total:.2f} kg CO₂")

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#17becf']
    
    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)
# Bar Chart
    fig_bar, ax_bar = plt.subplots()
    df.plot(kind='bar', x='Category', y='Emissions (kg CO₂)', legend=False, ax=ax_bar, color=colors[:len(df)])
    ax_bar.set_ylabel("Emissions (kg CO₂)")
    ax_bar.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax_bar.set_title("Carbon Footprint Summary (Bar Chart)")
    st.pyplot(fig_bar)
    
    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)
# Pie Chart (only non-negative values)
    pull_values = [0.1 if val < total_emission * 0.1 else 0 for val in df["Emissions (kg CO₂)"]]

# Plot
    st.subheader("🥧 Emissions Pie Chart (Clear & Distinct)")
    fig = px.pie(
    df,
    values="Emissions (kg CO₂)",
    names="Category",
    title="Emission Contribution by Category",
    color_discrete_sequence=px.colors.qualitative.Set3
)
    fig.update_traces(
    textinfo='percent+label',
    pull=pull_values,
    rotation=90,  # rotate for better label spacing
    textfont_size=14
)
    st.plotly_chart(fig)

    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)

    st.subheader("Download Reports")
    csv = df.to_csv(index=False).encode('utf-8')

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="carbon_footprint.csv",
            mime="text/csv"
    )
    with col2:
          buf = io.BytesIO()
          fig_bar.savefig(buf, format="png", bbox_inches='tight')
          st.download_button(
          label="🖼️ Download Charts",
          data=buf.getvalue(),
          file_name="emission_charts.png",
          mime="image/png"
    )
    
    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)
# Show total emissions
    total = df["Emissions (kg CO₂)"].sum()
    st.markdown(f"## **Total Net Emissions: {total:.2f} kg CO₂**")
    
    st.markdown("<hr style='border-top: 1px dotted #bbb;'>", unsafe_allow_html=True)
# Constants
    TREE_OFFSET_FACTOR = 21            # kg CO₂/year per tree
    LAND_OFFSET_FACTOR = 0.6178         # kg CO₂/year per acre (trees planted)
    GRASS_OFFSET_FACTOR = 0.3707        # kg CO₂/year per acre (approximate)
    WATER_OFFSET_FACTOR = 0.4943      # kg CO₂/year per acre (approximate)
    
    trees_count7 = st.session_state.get("trees_count7", 0)
    soil_area7 = st.session_state.get("soil_area7", 0)
    water_consum7 = st.session_state.get("water_consum7", 0)
    grass_area7 = st.session_state.get("grass_area7", 0)




# Calculations
    tree_offset = trees_count7 * TREE_OFFSET_FACTOR
    land_offset = soil_area7 * LAND_OFFSET_FACTOR
    grass_offset = grass_area7 * GRASS_OFFSET_FACTOR
    water_offset = water_consum7 * WATER_OFFSET_FACTOR
    
    total_offset = tree_offset + land_offset + grass_offset + water_offset

# Display
    st.subheader("Offset Contribution Summary")
    st.markdown(f"""
   🌳 You planted **{trees_count7} trees**, used:
    - **{soil_area7:.2f} m^2** for tree planting
    - **{grass_area7:.2f} m^2** covered in grass
    - **{water_consum7:.2f} m^2** covered in water

    ✅ This helped you reduce approximately:
    - **{tree_offset:.2f} kg CO₂/year** via trees
    - **{land_offset:.2f} kg CO₂/year** from tree-planted land
    - **{grass_offset:.2f} kg CO₂/year** from grassy land
    - **{water_offset:.2f} kg CO₂/year** from water-covered area

    💚 **Total Estimated Offset:** **{total_offset:.2f} kg CO₂/year**
     """)

