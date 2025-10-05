
---

## 🌧️ Rainfall Prediction App

### Predict whether it will rain in a given location using live weather data and a trained machine learning model.

---

### 📌 Features

- 🌍 Location-based prediction using Open-Meteo API  
- 📅 Date input (limited to next 7 days)  
- 🔍 Real-time weather data extraction  
- 🧠 Machine learning model (Random Forest) trained on historical weather data  
- 🖥️ Streamlit-powered web interface  
- ✅ Prediction output: “Rainfall” or “No Rainfall”

---

### 📁 Project Structure

```
rainfall-app/
├── app.py                        # Streamlit app
├── rainfall_prediction_model.pkl # Trained ML model
├── README.md                     # Project documentation
```

---

### 🧠 Model Details

- Trained using RandomForestClassifier  
- Features used:
  - pressure
  - dewpoint
  - humidity
  - cloud
  - sunshine
  - winddirection
  - windspeed  
- Balanced using downsampling  
- Tuned with GridSearchCV  
- Saved using `pickle`

---

### 🚀 Getting Started

#### 1. Clone the repository or download the folder

```bash
git clone https://github.com/yourusername/rainfall-app.git
cd rainfall-app
```

#### 2. Install dependencies

```bash
pip install streamlit pandas scikit-learn requests
```

#### 3. Run the app

```bash
streamlit run app.py
```

---

### 🧪 How to Use

1. Enter a valid city name (e.g., Chhindwara, Mumbai, Delhi)
2. Select a date within the next 7 days
3. Click **Predict**
4. View the result: 🌧️ Rainfall or ☀️ No Rainfall

---

### 🌐 APIs Used

- [Open-Meteo Geocoding API](https://open-meteo.com/)
- [Open-Meteo Forecast API](https://open-meteo.com/)

---

### 📦 Model Training (Optional)

If you want to retrain the model:
- Use the `Rainfall.csv` dataset
- Follow the Jupyter notebook steps:
  - Clean data
  - Handle missing values
  - Balance classes
  - Train and tune Random Forest
  - Save model with `pickle`

---

### 📌 To Improve

- Add SMOTE for better class balancing  
- Use PCA for dimensionality reduction  
- Try other models (Logistic Regression, XGBoost)  
- Deploy online using Streamlit Cloud or Render  
- Add map view or hourly forecast

---

### 📄 License

This project is open-source and free to use for educational and non-commercial purposes.

---
