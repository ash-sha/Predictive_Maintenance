import pandas as pd
import streamlit as st
import requests
import os

import uuid  # To generate unique IDs

# Load your data
DATA_DIR = os.getenv("DATA_DIR", "df_train_processed.csv")
data = pd.read_csv(DATA_DIR)

# Set up the page layout and logo
st.set_page_config(
    page_title="Predictive Maintenance",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create two columns for side-by-side images
col1, col2 = st.columns([1, 1])

with col1:
    st.image("nasa1.png", width=200)  # Left image (logo)
    st.write("## Predictive Maintenance of NASA TurboJet Engine")

with col2:
    st.image("nasa2.png", width=350)  # Right image (main image)




# Sensor Descriptions and Default Ranges for Relevant Sensors
sensor_descriptions_and_ranges = [
    ("cycle", 0, int(data["cycle"].max() + 1)),
    ("LPC outlet temperature (°R)", 0, int(data["(LPC outlet temperature) (◦R)"].max() + 1)),
    ("HPC outlet temperature (°R)", 0, int(data["(HPC outlet temperature) (◦R)"].max() + 1)),
    ("LPT outlet temperature (°R)", 0, int(data["(LPT outlet temperature) (◦R)"].max() + 1)),
    ("HPC outlet pressure (psia)", 0, int(data["(HPC outlet pressure) (psia)"].max() + 1)),
    ("Physical fan speed (rpm)", 0, int(data["(Physical fan speed) (rpm)"].max() + 1)),
    ("HPC outlet Static pressure (psia)", 0, int(data["(HPC outlet Static pressure) (psia)"].max() + 1)),
    ("Ratio of fuel flow to Ps30 (pps/psia)", 0, int(data["(Ratio of fuel flow to Ps30) (pps/psia)"].max() + 1)),
    ("Corrected fan speed (rpm)", 0, int(data["(Corrected fan speed) (rpm)"].max() + 1)),
    ("Corrected core speed (rpm)", 0, int(data["(Corrected core speed) (rpm)"].max() + 1)),
    ("Bypass Ratio", 0, int(data["(Bypass Ratio)"].max() + 1)),
    ("Bleed Enthalpy (Btu/lbm)", 0, int(data["(Bleed Enthalpy)"].max() + 1)),
    ("High-pressure turbines Cool air flow (lbm/s)", 0, int(data["(High-pressure turbines Cool air flow)"].max() + 1)),
    ("Low-pressure turbines Cool air flow (lbm/s)", 0, int(data["(Low-pressure turbines Cool air flow)"].max() + 1))
]

# Sidebar Inputs
st.sidebar.header("Input Features")

# Sensor inputs with descriptive names and unique ranges
input_features = {}
for idx, (description, min_value, max_value) in enumerate(sensor_descriptions_and_ranges):
    slider_key = f"slider_{idx}_{description}"
    sensor_value = st.sidebar.slider(description, min_value, max_value, (min_value + max_value) // 2, key=slider_key)
    input_features[description] = sensor_value

# Define a function to call the API and get the prediction
def get_prediction(input_data):
    response = requests.post("https://predictive-maintenance-kegp.onrender.com/predict", json=input_data)
    if response.status_code == 200:
        result = response.json()
        return result['predicted_rul']
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Button to trigger the prediction
if st.button("Remaining Useful Life"):
    # Prepare the input data in the format expected by the API
    input_data = {
        "cycle": input_features["cycle"],  # Replace with actual cycle value
        "LPC_outlet_temperature": input_features["LPC outlet temperature (°R)"],
        "HPC_outlet_temperature": input_features["HPC outlet temperature (°R)"],
        "LPT_outlet_temperature": input_features["LPT outlet temperature (°R)"],
        "HPC_outlet_pressure": input_features["HPC outlet pressure (psia)"],
        "Physical_fan_speed": input_features["Physical fan speed (rpm)"],
        "HPC_outlet_Static_pressure": input_features["HPC outlet Static pressure (psia)"],
        "Ratio_of_fuel_flow_to_Ps30": input_features["Ratio of fuel flow to Ps30 (pps/psia)"],
        "Corrected_fan_speed": input_features["Corrected fan speed (rpm)"],
        "Corrected_core_speed": input_features["Corrected core speed (rpm)"],
        "Bypass_Ratio": input_features["Bypass Ratio"],
        "Bleed_Enthalpy": input_features["Bleed Enthalpy (Btu/lbm)"],
        "High_pressure_turbines_Cool_air_flow": input_features["High-pressure turbines Cool air flow (lbm/s)"],
        "Low_pressure_turbines_Cool_air_flow": input_features["Low-pressure turbines Cool air flow (lbm/s)"]
    }

    # Call the API and get the prediction
    predicted_rul = get_prediction(input_data)
    if predicted_rul is not None:
        # st.success(f"{round(predicted_rul,2)}  Cycles")
        st.success(f" Predicted RUL :  {predicted_rul :.2f} Cycles")


