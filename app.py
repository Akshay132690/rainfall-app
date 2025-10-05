import streamlit as st
import pickle
import pandas as pd
import requests

# Load the trained model and feature names
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
feature_names = model_data["feature_names"]

# Streamlit UI setup
st.set_page_config(page_title="Rainfall Predictor", page_icon="🌧️")
st.title("🌦️ Will It Rain On My Parade?")
st.markdown("Enter a city and date to predict rainfall using live weather data.")

# User input
city = st.text_input("🌍 City name", value="Chhindwara")
date = st.date_input("📅 Date")

if st.button("Predict"):
    try:
        # Step 1: Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url).json()

        if not geo_res.get("results"):
            st.error("❌ City not found.")
            st.stop()

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        # Step 2: Get weather forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&daily=pressure_msl,dewpoint_2m_min,relative_humidity_2m_max,cloudcover,shortwave_radiation_sum,"
            f"winddirection_10m_dominant,windspeed_10m_max&timezone=auto"
        )
        weather_res = requests.get(weather_url).json()

        date_str = str(date)
        if "daily" not in weather_res or date_str not in weather_res["daily"]["time"]:
            st.error("❌ No forecast available for that date.")
            st.stop()

        index = weather_res["daily"]["time"].index(date_str)

        # Step 3: Extract features
        input_data = [
            weather_res["daily"]["pressure_msl"][index],
            weather_res["daily"]["dewpoint_2m_min"][index],
            weather_res["daily"]["relative_humidity_2m_max"][index],
            weather_res["daily"]["cloudcover"][index],
            weather_res["daily"]["shortwave_radiation_sum"][index],
            weather_res["daily"]["winddirection_10m_dominant"][index],
            weather_res["daily"]["windspeed_10m_max"][index],
        ]

        input_df = pd.DataFrame([input_data], columns=feature_names)
        prediction = model.predict(input_df)
        result = "🌧️ Rainfall" if prediction[0] == 1 else "☀️ No Rainfall"
        st.success(f"Prediction for {city} on {date_str}: {result}")

    except Exception as e:
        st.error("⚠️ Something went wrong. Please try again.")
        st.exception(e)
