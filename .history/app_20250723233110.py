import io
import streamlit as st
import pandas as pd
from analysis.chart import show_charts
from analysis.anomalies import show_anomalies
from analysis.forecast import show_forecast
from analysis.summary import show_summary
from analysis.user_data import get_user_details

# 💙 Salesforce-Inspired Color Scheme
PRIMARY_COLOR = "#114D91"
SECONDARY_COLOR = "#E5E9F2"
ACCENT_GREEN = "#2ECC71"
ACCENT_RED = "#E74C3C"
TEXT_COLOR = "#000000A1"

# 🎨 Apply custom styles
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {TEXT_COLOR};
        color: {SECONDARY_COLOR};
    }}
    .stSidebar {{
        background-color: {PRIMARY_COLOR};
        color: white;
    }}
    .stButton>button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border-radius: 8px;
        font-weight: 600;
    }}
    .stRadio>div>div>label {{
        color: {PRIMARY_COLOR};
        font-weight: 500;
    }}
    .stDataFrame {{
        background-color: white;
        color: {TEXT_COLOR};
    }}
    .kpi-card {{
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        border: 2px solid {PRIMARY_COLOR};
    }}
    .kpi-title {{
        color: {PRIMARY_COLOR};
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        color: {TEXT_COLOR};
        font-size: 26px;
        font-weight: 700;
    }}
    </style>
""", unsafe_allow_html=True)

# Custom CSS for file uploader
st.markdown("""
    <style>
    .stFileUploader > div {
        background-color: #ffffff;
        border: 2px solid #114D91;
        border-radius: 8px;
        color: #114D91;
        padding: 10px;
    }
    .stFileUploader > div:hover {
        background-color: #e6f0ff;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 SalesGrowth Dashboard")
page = st.sidebar.radio("Go to", ["Home", "Charts", "Anomalies", "Forecast", "Summary"])

# 👤 Show user info form first
if page == "Home":
    get_user_details()

# Check if user has entered info before allowing file upload
if "user_name" in st.session_state and "data_type" in st.session_state:
    uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            import io
            df = pd.read_csv(uploaded_file.read().decode("ISO-8859-1"))
        else:
            df = pd.read_excel(uploaded_file)

        # Show preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head())

        # KPI Cards
        st.subheader("📊 Key Performance Indicators")
        total_sales = df['Sales'].sum()
        total_profit = df['Profit'].sum()
        avg_order_value = df['Sales'].mean()
        top_region = df.groupby('Region')['Sales'].sum().idxmax() if 'Region' in df.columns else "N/A"
        order_count = df.shape[0]

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi4, kpi5, _ = st.columns(3)

        with kpi1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Sales</div><div class="kpi-value">${total_sales:,.2f}</div></div>', unsafe_allow_html=True)
        with kpi2:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Profit</div><div class="kpi-value">${total_profit:,.2f}</div></div>', unsafe_allow_html=True)
        with kpi3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Avg Order Value</div><div class="kpi-value">${avg_order_value:,.2f}</div></div>', unsafe_allow_html=True)
        with kpi4:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Top Region</div><div class="kpi-value">{top_region}</div></div>', unsafe_allow_html=True)
        with kpi5:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">Orders Count</div><div class="kpi-value">{order_count}</div></div>', unsafe_allow_html=True)

        # Route to analysis pages
        if page == "Charts":
            show_charts(df)
        elif page == "Anomalies":
            show_anomalies(df)
        elif page == "Forecast":
            show_forecast(df)
        elif page == "Summary":
            show_summary(df)
    else:
        st.info("📂 Please upload a CSV or Excel file to begin analysis.")
else:
    st.warning("📝 Please provide your name and sales type first (on the Home page).")
