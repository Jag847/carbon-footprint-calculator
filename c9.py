import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Initialize session state
if 'emission_factors' not in st.session_state:
    st.session_state.emission_factors = {
        "Fossil Fuels": {
            "CNG": 2.21, "Petrol/Gasoline": 2.31, "Diesel": 2.68, "PNG": 2.30, "LPG": 2.98
        },
        "Electricity": {
            "Coal/Thermal": 0.85, "Solar": 0.05, "Wind": 0.02, "Hydro": 0.01
        },
        "Travel": {
            "Airways": 0.133, "Roadways": 0.271, "Railways": 0.041
        }
    }

if 'emissions_data' not in st.session_state:
    st.session_state.emissions_data = {
        "Fossil Fuels": None, "Electricity": None, "Travel": None,
        "Water": None, "Waste": None, "Offset": None
    }

if 'slide_index' not in st.session_state:
    st.session_state.slide_index = 0

# Define slides
slides = [
    {"title": "Emission Factors", "content": "Configure your emission factors"},
    {"title": "Fossil Fuels", "content": "Calculate fossil fuel emissions"},
    {"title": "Electricity", "content": "Calculate electricity emissions"},
    {"title": "Travel", "content": "Calculate travel emissions"},
    {"title": "Water & Waste", "content": "Calculate water and waste emissions"},
    {"title": "Offset", "content": "Calculate carbon offsets"},
    {"title": "Analysis", "content": "View detailed analysis"}
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

# --- Emission Factors Configuration ---
if current_slide["title"] == "Emission Factors":
    st.header("Customize Emission Factors")
    
    with st.expander("🛢️ Fossil Fuels (kg CO₂ per kg)"):
        cols = st.columns(2)
        with cols[0]:
            st.session_state.emission_factors["Fossil Fuels"]["CNG"] = st.number_input(
                "CNG", min_value=0.0, value=st.session_state.emission_factors["Fossil Fuels"]["CNG"], step=0.01)
            st.session_state.emission_factors["Fossil Fuels"]["Diesel"] = st.number_input(
                "Diesel", min_value=0.0, value=st.session_state.emission_factors["Fossil Fuels"]["Diesel"], step=0.01)
        with cols[1]:
            st.session_state.emission_factors["Fossil Fuels"]["Petrol/Gasoline"] = st.number_input(
                "Petrol/Gasoline", min_value=0.0, value=st.session_state.emission_factors["Fossil Fuels"]["Petrol/Gasoline"], step=0.01)
            st.session_state.emission_factors["Fossil Fuels"]["LPG"] = st.number_input(
                "LPG", min_value=0.0, value=st.session_state.emission_factors["Fossil Fuels"]["LPG"], step=0.01)
    
    with st.expander("⚡ Electricity (kg CO₂ per kWh)"):
        st.session_state.emission_factors["Electricity"]["Coal/Thermal"] = st.number_input(
            "Coal/Thermal", min_value=0.0, value=st.session_state.emission_factors["Electricity"]["Coal/Thermal"], step=0.01)
        st.session_state.emission_factors["Electricity"]["Solar"] = st.number_input(
            "Solar", min_value=0.0, value=st.session_state.emission_factors["Electricity"]["Solar"], step=0.01)
    
    with st.expander("🚗 Travel (kg CO₂ per km)"):
        cols = st.columns(3)
        with cols[0]:
            st.session_state.emission_factors["Travel"]["Airways"] = st.number_input(
                "Air Travel", min_value=0.0, value=st.session_state.emission_factors["Travel"]["Airways"], step=0.001)
        with cols[1]:
            st.session_state.emission_factors["Travel"]["Roadways"] = st.number_input(
                "Road Travel", min_value=0.0, value=st.session_state.emission_factors["Travel"]["Roadways"], step=0.001)
        with cols[2]:
            st.session_state.emission_factors["Travel"]["Railways"] = st.number_input(
                "Rail Travel", min_value=0.0, value=st.session_state.emission_factors["Travel"]["Railways"], step=0.001)

# --- Fossil Fuels Calculator ---
elif current_slide["title"] == "Fossil Fuels":
    st.header("Fossil Fuel Consumption")
    
    col1, col2 = st.columns(2)
    with col1:
        fuel_type = st.selectbox("Select fuel type", list(st.session_state.emission_factors["Fossil Fuels"].keys()))
        unit = st.selectbox("Select unit", ["kg", "liters", "tonnes"])
    with col2:
        amount = st.number_input("Amount consumed", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate Emissions"):
        try:
            if amount <= 0:
                raise ValueError("Amount must be greater than zero")
            
            # Convert to kg if needed
            if unit == "tonnes":
                amount_kg = amount * 1000
            elif unit == "liters":
                # Assume approximate density of 0.75 kg/l for fuels
                amount_kg = amount * 0.75
            else:
                amount_kg = amount
            
            factor = st.session_state.emission_factors["Fossil Fuels"][fuel_type]
            emissions = amount_kg * factor
            st.session_state.emissions_data["Fossil Fuels"] = emissions
            
            st.success(f"""
                **Calculation Results:**
                - Fuel Type: {fuel_type}
                - Amount: {amount:.2f} {unit} ({amount_kg:.2f} kg)
                - Emission Factor: {factor:.2f} kg CO₂/kg
                - **Total Emissions: {emissions:.2f} kg CO₂**
            """)
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

# --- Electricity Calculator ---
elif current_slide["title"] == "Electricity":
    st.header("Electricity Consumption")
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("Energy source", list(st.session_state.emission_factors["Electricity"].keys()))
    with col2:
        consumption = st.number_input("Electricity used (kWh)", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate Emissions"):
        try:
            if consumption <= 0:
                raise ValueError("Consumption must be greater than zero")
            
            factor = st.session_state.emission_factors["Electricity"][source]
            emissions = consumption * factor
            st.session_state.emissions_data["Electricity"] = emissions
            
            st.success(f"""
                **Calculation Results:**
                - Energy Source: {source}
                - Consumption: {consumption:.2f} kWh
                - Emission Factor: {factor:.4f} kg CO₂/kWh
                - **Total Emissions: {emissions:.2f} kg CO₂**
            """)
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

# --- Travel Calculator ---
elif current_slide["title"] == "Travel":
    st.header("Travel Emissions")
    
    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox("Transport mode", list(st.session_state.emission_factors["Travel"].keys()))
    with col2:
        distance = st.number_input("Distance traveled (km)", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("Calculate Emissions"):
        try:
            if distance <= 0:
                raise ValueError("Distance must be greater than zero")
            
            factor = st.session_state.emission_factors["Travel"][mode]
            emissions = distance * factor
            st.session_state.emissions_data["Travel"] = emissions
            
            st.success(f"""
                **Calculation Results:**
                - Transport Mode: {mode}
                - Distance: {distance:.2f} km
                - Emission Factor: {factor:.4f} kg CO₂/km
                - **Total Emissions: {emissions:.2f} kg CO₂**
            """)
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

# --- Analysis Page ---
elif current_slide["title"] == "Analysis":
    st.header("Carbon Footprint Analysis")
    
    # Check if we have data
    if all(value is None for value in st.session_state.emissions_data.values()):
        st.warning("⚠️ No data available. Please complete calculations in previous sections.")
        st.stop()
    
    # Prepare data
    analysis_data = {
        "Category": [],
        "Emissions (kg CO₂)": [],
        "Emission Factors": [],
        "Input Values": []
    }
    
    # Collect all available data
    for category, value in st.session_state.emissions_data.items():
        if value is not None:
            analysis_data["Category"].append(category)
            analysis_data["Emissions (kg CO₂)"].append(value)
            
            # Get the appropriate factor based on category
            if category == "Fossil Fuels":
                factor = st.session_state.emission_factors["Fossil Fuels"]["Diesel"]  # Example default
            elif category == "Electricity":
                factor = st.session_state.emission_factors["Electricity"]["Coal/Thermal"]
            elif category == "Travel":
                factor = st.session_state.emission_factors["Travel"]["Roadways"]
            else:
                factor = 0
            
            analysis_data["Emission Factors"].append(factor)
            analysis_data["Input Values"].append(value/factor if factor !=0 else 0)
    
    df = pd.DataFrame(analysis_data)
    
    # Calculate totals
    total_emissions = df["Emissions (kg CO₂)"].sum()
    max_category = df.loc[df["Emissions (kg CO₂)"].idxmax(), "Category"]
    max_emission = df["Emissions (kg CO₂)"].max()
    
    # Display key metrics
    st.subheader("Key Metrics")
    cols = st.columns(3)
    cols[0].metric("Total Emissions", f"{total_emissions:.2f} kg CO₂")
    cols[1].metric("Highest Contributor", max_category, f"{max_emission:.2f} kg CO₂")
    cols[2].metric("Average Emission Factor", f"{df['Emission Factors'].mean():.4f} kg CO₂/unit")
    
    # Visualization section
    st.subheader("Visual Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📊 Emissions Breakdown", "📈 Factor Impact", "📋 Raw Data"])
    
    with tab1:
        # Bar chart of emissions by category
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(df["Category"], df["Emissions (kg CO₂)"], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        ax.set_title("Carbon Emissions by Category")
        ax.set_ylabel("kg CO₂")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Insights
        st.markdown("""
        **Insights:**
        - The longest bar represents your highest emission source
        - Compare relative contributions of different activities
        """)
    
    with tab2:
        # Scatter plot of input values vs emissions
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(df["Input Values"], df["Emissions (kg CO₂)"], 
                           c=df["Emission Factors"], s=100, cmap='viridis')
        
        # Add labels
        for i, txt in enumerate(df["Category"]):
            ax.annotate(txt, (df["Input Values"][i], df["Emissions (kg CO₂)"][i]))
        
        ax.set_title("Input Quantity vs Emissions")
        ax.set_xlabel("Input Quantity (kg, kWh, km)")
        ax.set_ylabel("Emissions (kg CO₂)")
        plt.colorbar(scatter, label='Emission Factor')
        st.pyplot(fig)
        
        # Insights
        st.markdown("""
        **Factor Impact Analysis:**
        - Points higher on the y-axis have greater emissions
        - Points further right represent higher consumption
        - Color intensity shows emission factor magnitude
        """)
    
    with tab3:
        # Show raw data with formatting
        st.dataframe(df.style.format({
            "Emissions (kg CO₂)": "{:.2f}",
            "Emission Factors": "{:.4f}",
            "Input Values": "{:.2f}"
        }))
        
        # Export options
        st.download_button(
            "Download Data as CSV",
            df.to_csv(index=False),
            "carbon_footprint_analysis.csv",
            "text/csv"
        )

# Navigation buttons
st.divider()
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.slide_index > 0:
        st.button("⬅️ Previous", on_click=prev_slide)
with col2:
    if st.session_state.slide_index < len(slides) - 1:
        st.button("Next ➡️", on_click=next_slide)

# Sidebar navigation
st.sidebar.title("Navigation")
for i, slide in enumerate(slides):
    if st.sidebar.button(slide["title"]):
        st.session_state.slide_index = i
