import streamlit as st
import pickle
import pandas as pd
import requests
from datetime import date as dt, timedelta

# --- Configuration and Setup ---

# Load the trained model and feature names
try:
    with open("rainfall_prediction_model.pkl", "rb") as file:
        model_data = pickle.load(file)

    model = model_data["model"]
    feature_names = model_data["feature_names"]
except FileNotFoundError:
    st.error("❌ Model file 'rainfall_prediction_model.pkl' not found. Please ensure it is in the same directory.")
    st.stop()
except KeyError:
    st.error("❌ Model file missing 'model' or 'feature_names' key.")
    st.stop()

# Streamlit UI setup
st.set_page_config(page_title="Rainfall Predictor", page_icon="🌧️", layout="centered")
st.title("🌧️ Will It Rain Today?")
st.markdown("Predict whether it will rain using NASA weather data and machine learning.")

# User input
city = st.text_input("🌍 Enter city name", value="Akola")
if not city:
    city = "Akola"

st.markdown("---")

if st.button("Predict"):
    try:
        # Step 1: Get coordinates from Open-Meteo (Geocoding)
        st.subheader("1. Geocoding")
        with st.spinner(f"Finding coordinates for {city}..."):
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
            geo_res = requests.get(geo_url).json()

            if not geo_res.get("results"):
                st.error(f"❌ City '{city}' not found. Please try a different name (e.g., add the country).")
                st.stop()

            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]
            st.success(f"Location found: **Lat {lat:.4f}, Lon {lon:.4f}**")

        # Step 2: Failsafe Weather Data Fetch (T-2, T-3, T-4)
        st.subheader("2. Fetching NASA Data")
        
        input_data = []
        fallback_values = [0.5, 25.0, 3.0, 60.0]  # Precipitation, Temp, Wind, Humidity
        date_found = False
        
        # Loop through dates: T-2, T-3, T-4
        for days_ago in range(2, 5): 
            date = dt.today() - timedelta(days=days_ago)
            date_str = date.strftime("%Y%m%d")
            
            st.caption(f"Attempting to retrieve data for: **{date.strftime('%B %d, %Y')}** (T-{days_ago})")

            # --- FIX 1: Use PRECTOTCORR in the request URL ---
            nasa_url = (
                f"https://power.larc.nasa.gov/api/temporal/daily/point?"
                f"parameters=PRECTOTCORR,T2M,WS2M,RH2M&start={date_str}&end={date_str}"
                f"&latitude={lat}&longitude={lon}&community=AG&format=JSON"
            )

            try:
                # Attempt to get data
                nasa_res = requests.get(nasa_url).json()
                weather = nasa_res.get("properties", {}).get("parameter")

                if weather:
                    # --- FIX 2: Extract PRECTOTCORR from the response ---
                    raw_data = [
                        weather.get("PRECTOTCORR", {}).get(date_str, -999),
                        weather.get("T2M", {}).get(date_str, -999),
                        weather.get("WS2M", {}).get(date_str, -999),
                        weather.get("RH2M", {}).get(date_str, -999),
                    ]
                    
                    # If *all* retrieved values are valid (not -999), use this data and stop
                    if all(val != -999 for val in raw_data):
                        input_data = raw_data
                        st.success(f"✅ Successfully retrieved live weather data from T-{days_ago}.")
                        date_found = True
                        break # Exit the loop, we found good data

            except Exception as e:
                # If the API call itself failed (e.g., connection error), continue to the next day
                pass
        
        # Final Fallback Check
        if not date_found:
            st.warning("⚠️ Could not retrieve live NASA data for the last 3 days. Using fallback values.")
            input_data = fallback_values.copy()
            if 'nasa_res' in locals():
                st.expander("Show Last Raw NASA API Response (for debugging)", expanded=False).json(nasa_res)


        # Step 3: Pad to match expected 7 features
        while len(input_data) < len(feature_names):
            input_data.append(0.0)

        st.markdown("---")

        # Step 4: Visualize weather data
        st.markdown("### 🌤️ Weather Data Used for Prediction")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Precipitation", f"{input_data[0]:.2f} mm")
        col2.metric("Temperature", f"{input_data[1]:.1f} °C")
        col3.metric("Wind Speed", f"{input_data[2]:.1f} m/s")
        col4.metric("Humidity", f"{input_data[3]:.0f} %")
        
        weather_table = pd.DataFrame({
            "Parameter": ["Precipitation (mm)", "Temperature (°C)", "Wind Speed (m/s)", "Humidity (%)"],
            "Value": input_data[:4]
        })
        st.table(weather_table)

        # Step 5: Predict
        input_df = pd.DataFrame([input_data], columns=feature_names)
        st.expander("Show Features Sent to ML Model", expanded=False).dataframe(input_df)

        prediction = model.predict(input_df)

        st.markdown("### 🧠 Prediction Result")
        if prediction[0] == 1:
            st.balloons()
            st.success("🎉 HIGH CHANCE OF RAINFALL! Take an umbrella.")
        else:
            st.info("☀️ NO RAINFALL EXPECTED. Enjoy the dry weather!")

    except Exception as e:
        st.error("⚠️ An unexpected error occurred during the prediction process.")
        st.exception(e)

st.markdown("---")
st.caption("Powered by NASA POWER API and Random Forest ML model. Built with ❤️ using Python + Streamlit.")