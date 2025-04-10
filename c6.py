import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Session state setup
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0

slides = ["Fossil Fuels", "Fugitive", "Electricity", "Water", "Waste", "Travel", "Offset", "Graphical Summary"]

def next_slide():
    if st.session_state.slide_index < len(slides) - 1:
        st.session_state.slide_index += 1

def prev_slide():
    if st.session_state.slide_index > 0:
        st.session_state.slide_index -= 1

def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.slide_index = 0

def validate_inputs():
    required_keys = [
        "Fossil Fuels Emission",
        "Fugitive Emission",
        "Electricity Emission",
        "Water Emission",
        "Waste Emission",
        "Travel Emission",
        "Offset Emission"
    ]
    missing = [key for key in required_keys if key not in st.session_state or st.session_state[key] is None]
    return missing

# Slide navigation
current_slide = slides[st.session_state.slide_index]

# UI per slide
st.title("Carbon Footprint Tracker")

if current_slide == "Fossil Fuels":
    st.header("Fossil Fuels")
    st.session_state["Fossil Fuels Emission"] = st.number_input("Enter emission from fossil fuels (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Fugitive":
    st.header("Fugitive Emissions")
    st.session_state["Fugitive Emission"] = st.number_input("Enter fugitive emissions (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Electricity":
    st.header("Electricity Usage")
    st.session_state["Electricity Emission"] = st.number_input("Enter emission from electricity (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Water":
    st.header("Water Usage")
    st.session_state["Water Emission"] = st.number_input("Enter emission from water usage (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Waste":
    st.header("Waste Disposal")
    st.session_state["Waste Emission"] = st.number_input("Enter emission from waste (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Travel":
    st.header("Travel and Transport")
    st.session_state["Travel Emission"] = st.number_input("Enter emission from travel (kg CO₂)", min_value=0.0, format="%.2f")

elif current_slide == "Offset":
    st.header("Offset Emissions")
    st.session_state["Offset Emission"] = st.number_input("Enter offset emission reduction (kg CO₂)", min_value=0.0, format="%.2f")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_slide)
    with col2:
        if st.button("Submit"):
            missing_inputs = validate_inputs()
            if missing_inputs:
                st.error("Please complete the following sections before submitting:")
                for item in missing_inputs:
                    st.markdown(f"- **{item}**")
            else:
                next_slide()

elif current_slide == "Graphical Summary":
    st.header("Graphical Summary of Your Carbon Footprint")

    emissions = {
        "Fossil Fuels": st.session_state.get("Fossil Fuels Emission", 0),
        "Fugitive": st.session_state.get("Fugitive Emission", 0),
        "Electricity": st.session_state.get("Electricity Emission", 0),
        "Water": st.session_state.get("Water Emission", 0),
        "Waste": st.session_state.get("Waste Emission", 0),
        "Travel": st.session_state.get("Travel Emission", 0),
        "Offset": -st.session_state.get("Offset Emission", 0)
    }

    df = pd.DataFrame({
        "Factor": list(emissions.keys()),
        "Emissions (kg CO₂)": list(emissions.values())
    })

    total_emission = df["Emissions (kg CO₂)"].sum()

    st.subheader(f"🌍 Net Carbon Emissions: **{total_emission:.2f} kg CO₂**")

    # Pie chart ignores negative values
    df_pie = df.copy()
    df_pie["Emissions (kg CO₂)"] = df_pie["Emissions (kg CO₂)"].apply(lambda x: max(x, 0))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].bar(df["Factor"], df["Emissions (kg CO₂)"], color='seagreen')
    axes[0].set_title("Bar Chart - Carbon Footprint by Factor")
    axes[0].set_ylabel("Emissions (kg CO₂)")
    axes[0].tick_params(axis='x', rotation=45)

    axes[1].pie(df_pie["Emissions (kg CO₂)"], labels=df_pie["Factor"], autopct='%1.1f%%')
    axes[1].set_title("Pie Chart - Emission Distribution")

    st.pyplot(fig)

    st.markdown("---")
    st.button("Start Over", on_click=reset_app)

# Navigation buttons
if current_slide != "Offset" and current_slide != "Graphical Summary":
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.slide_index > 0:
            st.button("Back", on_click=prev_slide)
    with col2:
        st.button("Next", on_click=next_slide)

