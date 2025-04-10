import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# Initialize session state for storing emission factors and calculations
if 'emission_factors' not in st.session_state:
    st.session_state.emission_factors = {
        "Fossil Fuels": {
            "CNG": 2.21,  # Default values that users can modify
            "Petrol/Gasoline": 2.31,
            "Diesel": 2.68,
            "PNG": 2.30,
            "LPG": 2.98
        },
        "Electricity": {
            "Coal/Thermal": 0.85,
            "Solar": 0
        },
        "Travel": {
            "Airways": 0.133,
            "Roadways": 0.271,
            "Railways": 0.041
        }
    }

# Initialize other session state variables
if 'emissions_data' not in st.session_state:
    st.session_state.emissions_data = {
        "Fossil Fuels": None,
        "Fugitive": None,
        "Electricity": None,
        "Water": None,
        "Waste": None,
        "Travel": None,
        "Offset": None
    }

if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

# Define slides
slides = [
    {"title": "Emission Factors", "content": "Set your custom emission factors"},
    {"title": "Fossil Fuels", "content": "Calculate emissions from fossil fuel consumption"},
    {"title": "Fugitive", "content": "Calculate fugitive emissions"},
    {"title": "Electricity", "content": "Calculate electricity emissions"},
    {"title": "Water", "content": "Calculate water-related emissions"},
    {"title": "Waste", "content": "Calculate waste emissions"},
    {"title": "Travel", "content": "Calculate travel emissions"},
    {"title": "Offset", "content": "Calculate carbon offsets"},
    {"title": "Results", "content": "View your carbon footprint results"}
]

# Navigation functions
def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

# Current slide
current_slide = slides[st.session_state.slide_index]
st.title(current_slide["title"])
st.write(current_slide["content"])

# Emission Factors Configuration Slide
if current_slide["title"] == "Emission Factors":
    st.header("Configure Your Emission Factors")
    
    with st.expander("Fossil Fuels Emission Factors (kg CO₂ per kg)"):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.emission_factors["Fossil Fuels"]["CNG"] = st.number_input(
                "CNG", value=st.session_state.emission_factors["Fossil Fuels"]["CNG"], step=0.01)
            st.session_state.emission_factors["Fossil Fuels"]["Petrol/Gasoline"] = st.number_input(
                "Petrol/Gasoline", value=st.session_state.emission_factors["Fossil Fuels"]["Petrol/Gasoline"], step=0.01)
        with col2:
            st.session_state.emission_factors["Fossil Fuels"]["Diesel"] = st.number_input(
                "Diesel", value=st.session_state.emission_factors["Fossil Fuels"]["Diesel"], step=0.01)
            st.session_state.emission_factors["Fossil Fuels"]["LPG"] = st.number_input(
                "LPG", value=st.session_state.emission_factors["Fossil Fuels"]["LPG"], step=0.01)
    
    with st.expander("Electricity Emission Factors (kg CO₂ per kWh)"):
        st.session_state.emission_factors["Electricity"]["Coal/Thermal"] = st.number_input(
            "Coal/Thermal", value=st.session_state.emission_factors["Electricity"]["Coal/Thermal"], step=0.01)
        st.session_state.emission_factors["Electricity"]["Solar"] = st.number_input(
            "Solar", value=st.session_state.emission_factors["Electricity"]["Solar"], step=0.01)
    
    with st.expander("Travel Emission Factors (kg CO₂ per km)"):
        st.session_state.emission_factors["Travel"]["Airways"] = st.number_input(
            "Airways", value=st.session_state.emission_factors["Travel"]["Airways"], step=0.001)
        st.session_state.emission_factors["Travel"]["Roadways"] = st.number_input(
            "Roadways", value=st.session_state.emission_factors["Travel"]["Roadways"], step=0.001)
        st.session_state.emission_factors["Travel"]["Railways"] = st.number_input(
            "Railways", value=st.session_state.emission_factors["Travel"]["Railways"], step=0.001)

# Fossil Fuels Calculator
elif current_slide["title"] == "Fossil Fuels":
    col1, col2 = st.columns(2)
    
    with col1:
        facility = st.selectbox("Facility", ["Residential", "Commercial", "Industrial"])
        fuel_type = st.selectbox("Fuel Type", list(st.session_state.emission_factors["Fossil Fuels"].keys()))
        unit = st.selectbox("Unit", ["kg", "tonnes"])
    
    with col2:
        amount = st.number_input("Amount Consumed", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate"):
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than 0")
            
            factor = st.session_state.emission_factors["Fossil Fuels"][fuel_type]
            amount_kg = amount * 1000 if unit == "tonnes" else amount
            carbon_footprint = amount_kg * factor
            
            st.session_state.emissions_data["Fossil Fuels"] = carbon_footprint
            st.success(f"Estimated CO₂ emission: {carbon_footprint:.2f} kg CO₂")
        except ValueError as e:
            st.error(str(e))

# Electricity Calculator
elif current_slide["title"] == "Electricity":
    col1, col2 = st.columns(2)
    
    with col1:
        facility = st.selectbox("Facility", ["Residential", "Commercial", "Industrial"])
        electricity_type = st.selectbox("Electricity Type", list(st.session_state.emission_factors["Electricity"].keys()))
    
    with col2:
        consumption = st.number_input("Electricity Consumption (kWh)", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate"):
        try:
            if consumption <= 0:
                raise ValueError("Consumption must be greater than 0")
            
            factor = st.session_state.emission_factors["Electricity"][electricity_type]
            electricity_emission = consumption * factor
            
            st.session_state.emissions_data["Electricity"] = electricity_emission
            st.success(f"Estimated CO₂ emission: {electricity_emission:.2f} kg CO₂")
        except ValueError as e:
            st.error(str(e))

# Travel Calculator
elif current_slide["title"] == "Travel":
    col1, col2 = st.columns(2)
    
    with col1:
        travel_mode = st.selectbox("Mode of Transport", list(st.session_state.emission_factors["Travel"].keys()))
    
    with col2:
        distance = st.number_input("Distance Traveled (km)", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate"):
        try:
            if distance <= 0:
                raise ValueError("Distance must be greater than 0")
            
            factor = st.session_state.emission_factors["Travel"][travel_mode]
            travel_emission = distance * factor
            
            st.session_state.emissions_data["Travel"] = travel_emission
            st.success(f"Estimated CO₂ emission: {travel_emission:.2f} kg CO₂")
        except ValueError as e:
            st.error(str(e))

# Results Page
elif current_slide["title"] == "Results":
    st.header("Your Carbon Footprint Results")
    
    # Check if we have any data
    if all(value is None for value in st.session_state.emissions_data.values()):
        st.warning("No data available. Please complete calculations in previous sections.")
    else:
        # Prepare data for visualization
        data = {
            "Category": list(st.session_state.emissions_data.keys()),
            "Emissions (kg CO₂)": list(st.session_state.emissions_data.values())
        }
        df = pd.DataFrame(data)
        
        # Replace None with 0 for calculations
        df.fillna(0, inplace=True)
        
        # Calculate totals
        total_emissions = df[df['Category'] != 'Offset']['Emissions (kg CO₂)'].sum()
        total_offset = abs(df[df['Category'] == 'Offset']['Emissions (kg CO₂)'].values[0])
        net_emissions = total_emissions - total_offset
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Emissions", f"{total_emissions:.2f} kg CO₂")
        col2.metric("Total Offset", f"{total_offset:.2f} kg CO₂")
        col3.metric("Net Emissions", f"{net_emissions:.2f} kg CO₂", 
                   delta_color="inverse" if net_emissions >= 0 else "normal")
        
        # Visualizations
        tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🍕 Pie Chart", "📋 Data Table"])
        
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['red' if x >= 0 else 'green' for x in df["Emissions (kg CO₂)"]]
            ax.bar(df["Category"], df["Emissions (kg CO₂)"], color=colors)
            ax.set_title("Carbon Footprint by Category")
            ax.set_ylabel("kg CO₂")
            ax.axhline(0, color='black', linewidth=0.8)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with tab2:
            df_pie = df[(df["Category"] != "Offset") & (df["Emissions (kg CO₂)"] > 0)]
            if not df_pie.empty:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(df_pie["Emissions (kg CO₂)"], labels=df_pie["Category"], 
                      autopct='%1.1f%%', startangle=90)
                ax.set_title("Emissions Distribution")
                st.pyplot(fig)
            else:
                st.warning("No positive emissions data to display")
        
        with tab3:
            st.dataframe(df.style.format({"Emissions (kg CO₂)": "{:.2f}"}))
            
            # Export data
            csv = df.to_csv(index=False)
            st.download_button(
                "Download Data as CSV",
                csv,
                "carbon_footprint.csv",
                "text/csv",
                key='download-csv'
            )

# Navigation buttons
st.divider()
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.slide_index > 0:
        st.button("Previous", on_click=prev_slide)
with col2:
    if st.session_state.slide_index < len(slides) - 1:
        st.button("Next", on_click=next_slide)

# Sidebar navigation
st.sidebar.title("Navigation")
for i, slide in enumerate(slides):
    if st.sidebar.button(slide["title"]):
        st.session_state.slide_index = i
