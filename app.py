import streamlit as st
import pandas as pd
import pickle
from datetime import datetime, timedelta
import warnings
import numpy as np
from sklearn.preprocessing import StandardScaler
import yfinance as yf

# Set page configuration
st.set_page_config(page_title="Gold Price Predictor", page_icon="🪙", layout="centered")

# Load the saved model, scaler, and forecast data
with open('gold_price_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

forecast_df = pd.read_csv('forecast_df.csv')
forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
data = pd.read_csv('gold_price_in_inr.csv')
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

# Function to fetch real-time gold ETF price
def fetch_gold_etf_price():
    try:
        gold_etf = yf.Ticker("IVZINGOLD.BO")
        price_data = gold_etf.history(period="1d")
        if not price_data.empty:
            latest_price = price_data['Close'].iloc[-1]
            return f"Current Gold ETF Price (IVZINGOLD.BO): Rs.{latest_price:.2f}"
        else:
            return "Unable to fetch real-time price: No data available."
    except Exception as e:
        return f"Unable to fetch real-time price: {str(e)}"

# Function to prepare features for a given date
def prepare_features(date_str, forecast_df, historical_df):
    try:
        # Parse input date
        input_date = pd.to_datetime(date_str, format='%Y-%m-%d')

        # Check if the date is within the forecast period
        max_historical_date = historical_df['Date'].max()
        max_forecast_date = max_historical_date + timedelta(days=365)
        if input_date < max_historical_date or input_date > max_forecast_date:
            raise ValueError(f"Date must be between {max_historical_date.strftime('%Y-%m-%d')} and {max_forecast_date.strftime('%Y-%m-%d')}.")

        # Get the closest forecasted date
        forecast_row = forecast_df.iloc[(forecast_df['ds'] - input_date).abs().idxmin()]

        # Extract features
        features = {
            'Open': forecast_row['Open'],
            'High': forecast_row['Close'],  # Using Close as proxy
            'Low': forecast_row['Close'],   # Using Close as proxy
            'Volume': forecast_row['Volume'],
            'Year': input_date.year,
            'Month': input_date.month,
            'Day': input_date.day,
            'DayOfWeek': input_date.dayofweek,
            'Close_Lag1': forecast_row['Close_Lag1'],
            'MA7': forecast_row['MA7']
        }

        # Convert to DataFrame
        feature_df = pd.DataFrame([features])

        # Scale features
        feature_scaled = scaler.transform(feature_df)

        return feature_scaled
    except Exception as e:
        raise ValueError(f"Error preparing features: {str(e)}")

# Function to predict gold price
def predict_gold_price(date_str, model, forecast_df, historical_df):
    try:
        # Prepare features
        features_scaled = prepare_features(date_str, forecast_df, historical_df)

        # Make prediction
        prediction = model.predict(features_scaled)[0]

        return prediction
    except Exception as e:
        return f"Prediction failed: {str(e)}"

# Sidebar for real-time gold ETF price
st.sidebar.title("Real-Time Gold ETF Price")
st.sidebar.markdown(fetch_gold_etf_price())

# Main app
st.title("🪙 Gold Price Predictor")
st.markdown("Enter the grams of gold and select a date (between 2025-05-22 and 2026-05-16) to predict the gold price.")

# Input section
st.subheader("Input Details")
col1, col2 = st.columns(2)

with col1:
    grams = st.text_input("Grams of Gold", placeholder="e.g., 10")

with col2:
    date_input = st.date_input(
        "Select Date",
        min_value=datetime(2025, 5, 22),
        max_value=datetime(2026, 5, 16),
        value=datetime(2025, 5, 23)
    )

manual_date = st.text_input("Or Enter Date Manually (YYYY-MM-DD)", placeholder="e.g., 2025-05-23")

# Predict button
if st.button("Predict"):
    try:
        # Use manual_date if provided, else use date_input from calendar
        date_str = manual_date if manual_date else date_input.strftime('%Y-%m-%d')
        if not date_str:
            st.error("Please provide a date either via calendar or manual entry.")
            st.stop()

        # Validate date range
        input_date = pd.to_datetime(date_str, format='%Y-%m-%d')
        min_date = pd.to_datetime('2025-05-22')
        max_date = pd.to_datetime('2026-05-16')
        if input_date < min_date or input_date > max_date:
            st.error("Date must be between 2025-05-22 and 2026-05-16.")
            st.stop()

        # Validate grams
        grams = float(grams)
        if grams <= 0:
            st.error("Grams must be a positive number.")
            st.stop()

        # Get prediction
        predicted_price = predict_gold_price(date_str, model, forecast_df, data)
        if isinstance(predicted_price, str):
            st.error(predicted_price)  # Error message
            st.stop()

        # Calculate price per gram and total price
        price_per_gram = predicted_price
        total_price = predicted_price * grams

        # Display results
        st.success(
            f"**Predicted Price per Gram for {date_str}:** Rs.{price_per_gram:.2f}\n\n"
            f"**Total Price for {grams} grams:** Rs.{total_price:.2f}\n\n"
            f"**Note:** The difference between predicted price and actual price is usually between 600 to 800 INR."
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")
