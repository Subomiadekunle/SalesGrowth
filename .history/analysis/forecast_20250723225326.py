# analysis/forecast.py

import streamlit as st
import pandas as pd
import plotly.express as px

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    from sklearn.linear_model import LinearRegression
    import numpy as np

def show_forecast(df):
    st.subheader("📈 30-Day Sales Forecast")

    if 'Order Date' not in df.columns or 'Sales' not in df.columns:
        st.error("Your data must contain 'Order Date' and 'Sales' columns.")
        return

    # Convert 'Order Date' to datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df = df.dropna(subset=['Order Date', 'Sales'])

    # Group by date and sum sales
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('Order Date')

    if PROPHET_AVAILABLE:
        # Rename columns for Prophet
        prophet_df = daily_sales.rename(columns={'Order Date': 'ds', 'Sales': 'y'})

        # Initialize and fit Prophet model
        model = Prophet()
        model.fit(prophet_df)

        # Create future dates
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        # Plot forecast
        fig = px.line(forecast, x='ds', y='yhat', title='Forecasted Sales (Next 30 Days)', markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # Show forecast table
        st.write("📅 Forecast Data (Last 10 Days of Forecast)")
        st.dataframe(forecast[['ds', 'yhat']].tail(10).rename(columns={'ds': 'Date', 'yhat': 'Predicted Sales'}))

    else:
        # Fallback: use Linear Regression
        st.warning("Prophet is not installed. Using Linear Regression as fallback.")

        # Prepare time series for regression
        daily_sales['ds'] = (daily_sales['Order Date'] - daily_sales['Order Date'].min()).dt.days
        X = daily_sales[['ds']]
        y = daily_sales['Sales']
        model = LinearRegression().fit(X, y)

        # Predict next 30 days
        future_days = pd.DataFrame({'ds': range(X['ds'].max() + 1, X['ds'].max() + 31)})
        future_sales = model.predict(future_days)
        future_dates = pd.date_range(start=daily_sales['Order Date'].max() + pd.Timedelta(days=1), periods=30)

        # Display forecast
        forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Sales': future_sales})
        fig = px.line(forecast_df, x='Date', y='Predicted Sales', title='Forecasted Sales (Linear Regression)')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(forecast_df.tail(10))
