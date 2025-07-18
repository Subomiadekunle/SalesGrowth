import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest
import pandas as pd

def show_anomalies(df):
    st.header("🚨 Anomaly Detection in Sales Data")

    df = df.copy()
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df = df.dropna(subset=['Order Date', 'Sales'])

    # Group by date
    daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()

    # Isolation Forest
    model = IsolationForest(contamination=0.02, random_state=42)
    model.fit(daily_sales[['Sales']])
    daily_sales['Anomaly'] = model.predict(daily_sales[['Sales']])

    # Plot anomalies
    fig = px.line(daily_sales, x='Order Date', y='Sales', title="📉 Sales with Detected Anomalies")
    fig.add_scatter(
        x=daily_sales[daily_sales['Anomaly'] == -1]['Order Date'],
        y=daily_sales[daily_sales['Anomaly'] == -1]['Sales'],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Anomaly'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary
    num_anomalies = daily_sales['Anomaly'].value_counts().get(-1, 0)
    st.success(f"✅ Found {num_anomalies} anomalies in your sales data.")
