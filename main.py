import os

import joblib
import uvicorn
import xgboost as xgb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Initialize the FastAPI app
app = FastAPI()

# Load the model
MODEL_DIR = os.getenv("MODEL_DIR", "/Users/aswathshakthi/PycharmProjects/MLOps/Predictive_maintenance/models/xgboost.json")
VEC_DIR = os.getenv("VEC_DIR","/Users/aswathshakthi/PycharmProjects/MLOps/Predictive_maintenance/models/scaler.pkl")

loaded_model = xgb.XGBRegressor(random_state=42, n_jobs=-1)
loaded_model.load_model(MODEL_DIR)

scaler = MinMaxScaler()

# Define the input schema
class FeatureInput(BaseModel):
    cycle: float
    LPC_outlet_temperature: float
    HPC_outlet_temperature: float
    LPT_outlet_temperature: float
    HPC_outlet_pressure: float
    Physical_fan_speed: float
    HPC_outlet_Static_pressure: float
    Ratio_of_fuel_flow_to_Ps30: float
    Corrected_fan_speed: float
    Corrected_core_speed: float
    Bypass_Ratio: float
    Bleed_Enthalpy: float
    High_pressure_turbines_Cool_air_flow: float
    Low_pressure_turbines_Cool_air_flow: float


# Define the API endpoint for prediction
@app.post("/predict")
async def predicted_rul(input_data: FeatureInput):
    try:
        # Convert input data to a NumPy array
        input_array = np.array([
            [
                input_data.cycle,
                input_data.LPC_outlet_temperature,
                input_data.HPC_outlet_temperature,
                input_data.LPT_outlet_temperature,
                input_data.HPC_outlet_pressure,
                input_data.Physical_fan_speed,
                input_data.HPC_outlet_Static_pressure,
                input_data.Ratio_of_fuel_flow_to_Ps30,
                input_data.Corrected_fan_speed,
                input_data.Corrected_core_speed,
                input_data.Bypass_Ratio,
                input_data.Bleed_Enthalpy,
                input_data.High_pressure_turbines_Cool_air_flow,
                input_data.Low_pressure_turbines_Cool_air_flow,
            ]
        ])

        # Ensure the array is of type float32
        input_array = input_array.astype(np.float32)
        scaler = joblib.load(VEC_DIR)

        # Fit the scaler on the training data_processing and transform both training and test data_processing
        input_array_norm = scaler.transform(input_array)

        # Predict RUL
        predicted_rul = loaded_model.predict(input_array_norm)

        predicted_rul_cy = np.expm1(predicted_rul[0])
        # Extract and return the prediction
        return {"predicted_rul": float(predicted_rul_cy)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")


# Main entry point to run the application
if __name__ == "__main__":
    # Run FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
