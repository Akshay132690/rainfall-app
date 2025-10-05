

---

## 🌧️ Rainfall Prediction App

### Predict whether it will rain today using NASA weather data and a trained machine learning model.

---

### 🚀 Features

- 🌍 Enter any city name to get weather data
- 📡 Automatically fetches weather from NASA POWER API
- 🧠 Uses a trained Random Forest model to predict rainfall
- 🛡️ Fallback logic ensures prediction even if live data is unavailable
- 📊 Visualizes weather inputs and model features
- 🎉 Friendly UI built with Streamlit

---

### 🧰 Requirements

- Python 3.8+
- `streamlit`
- `pandas`
- `requests`
- `scikit-learn` (for model compatibility)

Install dependencies:

```bash
pip install streamlit pandas requests scikit-learn
```

---

### 📦 Files

- `app.py` → Main Streamlit app
- `rainfall_prediction_model.pkl` → Trained model file (must include `model` and `feature_names` keys)

---

### ▶️ How to Run

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

---

### 🧠 How It Works

1. **Geocoding**: Converts city name to latitude/longitude using Open-Meteo API  
2. **Weather Fetch**: Queries NASA POWER API for recent weather data (T-2 to T-4)  
3. **Fallback**: If no valid data is found, uses default values  
4. **Prediction**: Sends features to a trained Random Forest model  
5. **Visualization**: Displays weather inputs and prediction result

---

### 📌 Notes

- The model must be trained to accept 7 features. If using only 4 weather features, pad with zeros.
- NASA POWER may not return data for the current day—this app checks the last 3 days automatically.
- You can retrain your model using historical NASA data for better accuracy.

---

### ❤️ Credits

Built with [Streamlit](https://streamlit.io/) and powered by [NASA POWER API](https://power.larc.nasa.gov/).  
Developed with love using Python.

---

