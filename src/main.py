from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
import pandas as pd
from fastapi.responses import HTMLResponse


app = FastAPI(title="House Price Prediction API")


# Trained ML pipeline load karo
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "house_price_model.pkl"

model = joblib.load(MODEL_PATH)


class HouseData(BaseModel):
    Size_sqft: float
    Bedrooms: int
    Bathrooms: int
    Floors: int
    Property_Type: str
    Price_per_sqft: float
    Property_Age_years: int
    Distance_to_City_Center_km: float
    Parking_Spaces: int
    Furnished_Status: str
    Location_Quality: str


@app.get("/", response_class=HTMLResponse)
def home():
    html_path = Path(__file__).resolve().parent / "templates" / "index.html"

    return html_path.read_text(encoding="utf-8")


@app.post("/predict")
def predict(data: HouseData):

    input_data = pd.DataFrame([{
        "Size_sqft": data.Size_sqft,
        "Bedrooms": data.Bedrooms,
        "Bathrooms": data.Bathrooms,
        "Floors": data.Floors,
        "Property_Type": data.Property_Type,
        "Price_per_sqft": data.Price_per_sqft,
        "Property_Age_years": data.Property_Age_years,
        "Distance_to_City_Center_km": data.Distance_to_City_Center_km,
        "Parking_Spaces": data.Parking_Spaces,
        "Furnished_Status": data.Furnished_Status,
        "Location_Quality": data.Location_Quality
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_price_INR": round(float(prediction), 2)
    }