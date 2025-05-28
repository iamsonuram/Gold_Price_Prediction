# Gold Price Predictor

## Project Description
The **Gold Price Predictor** is a Streamlit-based web application designed to predict gold prices in Indian Rupees (INR) per gram for future dates (May 22, 2025, to May 16, 2026). The app leverages a pre-trained Linear Regression model and Prophet-generated forecast data to provide accurate predictions. Users can input the grams of gold and select a date using a calendar or manual entry. The app outputs the predicted price per gram and the total price for the specified grams. Additionally, it displays the real-time price of the Nippon India ETF Gold BeES (GOLDBEES.NS) in the sidebar for market context. A note informs users that predictions typically differ from actual prices by 400 to 600 INR, based on historical performance.

**Note**: The model uses 'High' and 'Low' features, which may cause data leakage as they are proxied by the forecasted 'Close' price. For more accurate predictions, consider retraining the model without these features.

## Features
- **User Input**: Enter grams of gold and select a date (via calendar or manual entry in `YYYY-MM-DD` format).
- **Date Range**: Predictions are valid for dates between May 22, 2025, and May 16, 2026.
- **Real-Time Price**: Displays the current price of Nippon India ETF Gold BeES (GOLDBEES.NS) in the sidebar using the `yfinance` library.
- **Prediction Output**: Shows the predicted price per gram, total price for the entered grams, and a note about the typical prediction error range (400–600 INR).
- **Input Validation**: Ensures grams is a positive number and the date is within the valid range.
- **Warning**: Alerts users about potential data leakage in the model due to 'High' and 'Low' features.

## File Structure
```
gold_price_prediction/
│
├── app.py                    # Streamlit app code
├── gold_price_model.pkl      # Saved Linear Regression model
├── scaler.pkl                # Saved StandardScaler
├── forecast_df.csv           # Saved forecast data from Prophet
├── gold_price_in_inr.csv     # Historical gold price data
├── requirements.txt          # Dependencies for the project
├── README.md                 # This file
```

## Prerequisites
- **Python**: Version 3.8 or higher
- **VS Code**: For editing and running the app
- **Internet Connection**: Required for fetching real-time ETF prices via `yfinance`
- **Required Files**:
  - `gold_price_model.pkl`: Pre-trained Linear Regression model
  - `scaler.pkl`: Pre-trained StandardScaler
  - `forecast_df.csv`: Forecasted data from Prophet
  - `gold_price_in_inr.csv`: Historical gold price data

## Setup Instructions
1. **Clone or Set Up the Project Directory**:
   - Create a directory named `gold_price_prediction`.
   - Place the following files in the directory:
     - `app.py`
     - `gold_price_model.pkl`
     - `scaler.pkl`
     - `forecast_df.csv`
     - `gold_price_in_inr.csv`
     - `requirements.txt`
     - `README.md` (this file)

2. **Install Dependencies**:
   - Open VS Code and navigate to the project directory in the terminal:
     ```bash
     cd path/to/gold_price_prediction
     ```
   - Create and activate a virtual environment (recommended):
     ```bash
     python -m venv venv
     .\venv\Scripts\activate  # On Windows
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Verify Dependencies**:
   - Ensure the following packages are installed (check with `pip list`):
     - `streamlit>=1.35.0`
     - `pandas>=2.0.0`
     - `numpy>=1.25.0`
     - `scikit-learn>=1.3.0`
     - `prophet>=1.1.5`
     - `yfinance>=0.2.40`

## Running the App
1. **Start the Streamlit App**:
   - In the VS Code terminal, with the virtual environment activated, run:
     ```bash
     streamlit run app.py
     ```
   - This will launch the app, typically at `http://localhost:8501`. Open your browser to this URL if it doesn’t open automatically.

2. **Using the App**:
   - **Sidebar**: View the real-time price of Nippon India ETF Gold BeES (GOLDBEES.NS). If the fetch fails (e.g., due to no internet), an error message will appear.
   - **Grams of Gold**: Enter a positive number (e.g., `10` for 10 grams).
   - **Date Selection**: Use the calendar to select a date (restricted to May 22, 2025, to May 16, 2026) or enter a date manually in `YYYY-MM-DD` format (e.g., `2025-05-23`).
   - **Predict Button**: Click to view the predicted price per gram, total price, and a note about the typical error range (400–600 INR).
   - **Output**: Results or error messages (e.g., for invalid inputs) will appear below the button.

## Troubleshooting
- **File Errors**: Ensure all required files (`gold_price_model.pkl`, `scaler.pkl`, `forecast_df.csv`, `gold_price_in_inr.csv`) are in the project directory.
- **Dependency Issues**: Verify all packages are installed correctly (`pip list`). Reinstall dependencies if needed (`pip install -r requirements.txt`).
- **Real-Time Price Issues**: If the ETF price fetch fails, check your internet connection or try again later. The app will display an error message in the sidebar.
- **Port Conflicts**: If `http://localhost:8501` is blocked, Streamlit will suggest an alternative port in the terminal.
- **Market Hours**: Real-time ETF prices are most accurate during Indian market hours (NSE: 9:15 AM to 3:30 PM IST). Outside these hours, the latest closing price is shown.

## Notes
- **Gold ETF**: The app uses Nippon India ETF Gold BeES (GOLDBEES.NS) for real-time prices, as it’s a popular gold ETF in India representing 1 gram of gold per unit. To use a different ETF, modify the ticker in the `fetch_gold_etf_price` function in `app.py`.
- **Prediction Accuracy**: The model’s predictions are based on historical data and Prophet forecasts. The typical error range is 400–600 INR, as observed in historical comparisons (e.g., May 23–28, 2025).
- **Data Leakage**: The model includes 'High' and 'Low' features, which may cause data leakage as they are proxied by the forecasted 'Close' price. Retraining without these features is recommended for improved accuracy.
- **Real-Time Price Limitations**: The `yfinance` library provides near-real-time data but may have delays or fail during non-market hours or due to API limits.

## Future Improvements
- Replace `yfinance` with a more robust API (e.g., Alpha Vantage) for real-time prices.
- Retrain the model without 'High' and 'Low' features to avoid data leakage.
- Add visualizations (e.g., historical vs. predicted price trends).
- Support for multiple gold ETFs or other gold price benchmarks.

## License
This project is for personal use and not distributed under any specific license. Ensure you have the necessary permissions for the dataset and model files.

---

*Last updated: May 28, 2025*