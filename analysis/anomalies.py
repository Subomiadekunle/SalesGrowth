# import streamlit as st
# import plotly.express as px
# from sklearn.ensemble import IsolationForest
# import pandas as pd

# def show_anomalies(df):
#     st.header("🚨 Anomaly Detection in Sales Data")

#     df = df.copy()
#     df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
#     df = df.dropna(subset=['Order Date', 'Sales'])

#     # Group by date
#     daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()

#     # Isolation Forest
#     model = IsolationForest(contamination=0.02, random_state=42)
#     model.fit(daily_sales[['Sales']])
#     daily_sales['Anomaly'] = model.predict(daily_sales[['Sales']])

#     # Plot anomalies
#     fig = px.line(daily_sales, x='Order Date', y='Sales', title="📉 Sales with Detected Anomalies")
#     fig.add_scatter(
#         x=daily_sales[daily_sales['Anomaly'] == -1]['Order Date'],
#         y=daily_sales[daily_sales['Anomaly'] == -1]['Sales'],
#         mode='markers',
#         marker=dict(color='red', size=10),
#         name='Anomaly'
#     )

#     st.plotly_chart(fig, use_container_width=True)

#     # Summary
#     num_anomalies = daily_sales['Anomaly'].value_counts().get(-1, 0)
#     st.success(f"✅ Found {num_anomalies} anomalies in your sales data.")
#     if num_anomalies > 0:
#         st.markdown(
#             "**What does an anomaly mean?**\n"
#             "An anomaly is a data point that significantly deviates from typical sales patterns. "
#             "This could indicate an unexpected sales spike (e.g., a promotion or bulk order) or a sudden drop "
#             "(e.g., a stockout, website issue, or external event). These points are worth reviewing to understand the underlying cause."
#         )
#     else:
#         st.markdown("No unusual sales patterns were detected during this period.")

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

    # Label anomalies
    daily_sales['Anomaly Type'] = None
    median_sales = daily_sales['Sales'].median()

    daily_sales.loc[
        (daily_sales['Anomaly'] == -1) & (daily_sales['Sales'] < median_sales),
        'Anomaly Type'
    ] = 'Low Anomaly'

    daily_sales.loc[
        (daily_sales['Anomaly'] == -1) & (daily_sales['Sales'] > median_sales),
        'Anomaly Type'
    ] = 'High Anomaly'

    # Plot
    fig = px.line(daily_sales, x='Order Date', y='Sales', title="📉 Sales with Detected Anomalies")

    # Add low anomalies
    fig.add_scatter(
        x=daily_sales[daily_sales['Anomaly Type'] == 'Low Anomaly']['Order Date'],
        y=daily_sales[daily_sales['Anomaly Type'] == 'Low Anomaly']['Sales'],
        mode='markers',
        marker=dict(color='red', size=10),
        name='Low Anomaly'
    )

    # Add high anomalies
    fig.add_scatter(
        x=daily_sales[daily_sales['Anomaly Type'] == 'High Anomaly']['Order Date'],
        y=daily_sales[daily_sales['Anomaly Type'] == 'High Anomaly']['Sales'],
        mode='markers',
        marker=dict(color='green', size=10),
        name='High Anomaly'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary
    num_anomalies = daily_sales['Anomaly'].value_counts().get(-1, 0)
    st.success(f"✅ Found {num_anomalies} anomalies in your sales data.")

    if num_anomalies > 0:
        st.markdown(
            "**What does an anomaly mean?**\n"
            "- **Low Anomaly** (🔴): Sales on that day were significantly *lower* than usual. This could indicate issues like stockouts, poor traffic, or operational problems.\n"
            "- **High Anomaly** (🟢): Sales were unusually *high*. Possible causes include promotions, bulk purchases, or special events.\n\n"
            "These outliers highlight important business events and deserve deeper investigation."
        )
    else:
        st.markdown("No unusual sales patterns were detected during this period.")
