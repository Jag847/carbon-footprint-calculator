import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Set page config
st.set_page_config(layout="wide", page_title="Carbon Footprint Calculator")

# Initialize session state
if 'emission_data' not in st.session_state:
    st.session_state.emission_data = {
        "Fossil Fuels": None,
        "Electricity": None,
        "Travel": None,
        "Water": None,
        "Waste": None,
        "Offset": None
    }
    st.session_state.current_page = "input"
    st.session_state.emission_factors = {
        "Fossil Fuels": {"CNG": 2.21, "Petrol/Gasoline": 2.31, "Diesel": 2.68},
        "Electricity": {"Coal/Thermal": 0.85, "Solar": 0.05},
        "Travel": {"Airways": 0.133, "Roadways": 0.271, "Railways": 0.041}
    }

# Input Page
if st.session_state.current_page == "input":
    st.title("Carbon Footprint Calculator")
    
    # Fossil Fuels Section
    with st.expander("🛢️ Fossil Fuels Consumption"):
        col1, col2 = st.columns(2)
        with col1:
            fuel_type = st.selectbox("Fuel Type", list(st.session_state.emission_factors["Fossil Fuels"].keys()))
            amount = st.number_input("Amount Consumed", min_value=0.0, max_value=10000)
        with col2:
            unit = st.selectbox("Unit", ["kg", "liters", "tonnes"])
            custom_factor = st.number_input("Custom Emission Factor (kg CO₂ per kg)", 
                                         value=st.session_state.emission_factors["Fossil Fuels"][fuel_type],
                                         step=1000)
        
        # Update factor if custom value provided
        st.session_state.emission_factors["Fossil Fuels"][fuel_type] = custom_factor
        
        # Calculate
        if st.button("Calculate Fossil Fuel Emissions"):
            try:
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero")
                
                # Convert to kg
                if unit == "tonnes":
                    amount_kg = amount * 1000
                elif unit == "liters":
                    amount_kg = amount * 0.75  # Approximate conversion
                else:
                    amount_kg = amount
                
                emissions = amount_kg * custom_factor
                st.session_state.emission_data["Fossil Fuels"] = emissions
                st.success(f"Fossil Fuel Emissions: {emissions:.2f} kg CO₂")
            except Exception as e:
                st.error(str(e))

    # Electricity Section
    with st.expander("⚡ Electricity Consumption"):
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox("Energy Source", list(st.session_state.emission_factors["Electricity"].keys()))
            consumption = st.number_input("Electricity Used (kWh)", min_value=0.0, value=0.0, step=0.1)
        with col2:
            custom_factor = st.number_input("Custom Emission Factor (kg CO₂ per kWh)", 
                                         value=st.session_state.emission_factors["Electricity"][source],
                                         step=0.001)
        
        # Update factor
        st.session_state.emission_factors["Electricity"][source] = custom_factor
        
        # Calculate
        if st.button("Calculate Electricity Emissions"):
            try:
                if consumption <= 0:
                    raise ValueError("Consumption must be greater than zero")
                
                emissions = consumption * custom_factor
                st.session_state.emission_data["Electricity"] = emissions
                st.success(f"Electricity Emissions: {emissions:.2f} kg CO₂")
            except Exception as e:
                st.error(str(e))

    # Travel Section
    with st.expander("✈️ Travel Emissions"):
        col1, col2 = st.columns(2)
        with col1:
            mode = st.selectbox("Transport Mode", list(st.session_state.emission_factors["Travel"].keys()))
            distance = st.number_input("Distance Traveled (km)", min_value=0.0, value=0.0, step=0.1)
        with col2:
            custom_factor = st.number_input("Custom Emission Factor (kg CO₂ per km)", 
                                         value=st.session_state.emission_factors["Travel"][mode],
                                         step=0.001)
        
        # Update factor
        st.session_state.emission_factors["Travel"][mode] = custom_factor
        
        # Calculate
        if st.button("Calculate Travel Emissions"):
            try:
                if distance <= 0:
                    raise ValueError("Distance must be greater than zero")
                
                emissions = distance * custom_factor
                st.session_state.emission_data["Travel"] = emissions
                st.success(f"Travel Emissions: {emissions:.2f} kg CO₂")
            except Exception as e:
                st.error(str(e))

    # Submit button to go to results
    if st.button("View Results", type="primary"):
        st.session_state.current_page = "results"
        st.experimental_rerun()

# Results Page
elif st.session_state.current_page == "results":
    st.title("Carbon Footprint Analysis")
    
    # Prepare data
    categories = ["Fossil Fuels", "Electricity", "Travel"]
    emissions = [st.session_state.emission_data.get(cat, 0) for cat in categories]
    
    # Create DataFrame
    df = pd.DataFrame({
        "Category": categories,
        "Emissions (kg CO₂)": emissions
    })
    
    # Filter out zero values for pie chart
    df_pie = df[df["Emissions (kg CO₂)"] > 0].copy()
    
    # Layout for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar Chart
        st.subheader("Emissions by Category")
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        bars = ax1.bar(df["Category"], df["Emissions (kg CO₂)"], 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom')
        
        ax1.set_ylabel("kg CO₂")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
    
    with col2:
        # Pie Chart (only if we have positive values)
        if not df_pie.empty:
            st.subheader("Emissions Distribution")
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            ax2.pie(df_pie["Emissions (kg CO₂)"], labels=df_pie["Category"],
                   autopct='%1.1f%%', startangle=90,
                   colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            st.pyplot(fig2)
        else:
            st.warning("No positive emissions data for pie chart")
    
    # Emissions Table
    st.subheader("Detailed Emissions Data")
    st.dataframe(df.style.format({"Emissions (kg CO₂)": "{:.2f}"}))
    
    # Download Section
    st.subheader("Download Options")
    
    # CSV Download
    csv = df.to_csv(index=False)
    st.download_button(
        "Download Data as CSV",
        csv,
        "carbon_footprint.csv",
        "text/csv"
    )
    
    # Image Download
    if not df_pie.empty:
        buf = io.BytesIO()
        fig2.savefig(buf, format="png")
        buf.seek(0)
        st.download_button(
            "Download Pie Chart as PNG",
            buf,
            "emissions_pie_chart.png",
            "image/png"
        )
    
    # Back button
    if st.button("Back to Calculator"):
        st.session_state.current_page = "input"
        st.experimental_rerun()
