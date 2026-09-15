from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.text


def test_prediction():
    payload = {
        "Size_sqft": 1500,
        "Bedrooms": 3,
        "Bathrooms": 3,
        "Floors": 2,
        "Property_Type": "Apartment",
        "Price_per_sqft": 8500,
        "Property_Age_years": 5,
        "Distance_to_City_Center_km": 6,
        "Parking_Spaces": 2,
        "Furnished_Status": "Semi-Furnished",
        "Location_Quality": "High"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()

    assert "predicted_price_INR" in result
    assert isinstance(result["predicted_price_INR"], float)
    assert result["predicted_price_INR"] > 0