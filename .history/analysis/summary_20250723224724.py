# summary.py

import streamlit as st
import pandas as pd

def show_summary(df):
    st.subheader("📄 Sales Summary")

    if df is None or df.empty:
        st.warning("No data available to summarize.")
        return

    try:
        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()
        avg_order_value = df["Sales"].mean()
        top_category = df["Category"].value_counts().idxmax() if "Category" in df.columns else "N/A"
        top_region = df.groupby("Region")["Sales"].sum().idxmax() if "Region" in df.columns else "N/A"
        most_profitable_subcategory = df.groupby("Sub-Category")["Profit"].sum().idxmax() if "Sub-Category" in df.columns else "N/A"
        
        st.markdown(f"""
        <div style="font-size: 18px; line-height: 1.8">
            ✅ **Total Sales**: ${total_sales:,.2f}  
            ✅ **Total Profit**: ${total_profit:,.2f}  
            ✅ **Average Order Value**: ${avg_order_value:,.2f}  
            ✅ **Top Performing Category**: {top_category}  
            ✅ **Top Region by Sales**: {top_region}  
            ✅ **Most Profitable Sub-Category**: {most_profitable_subcategory}  
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred while generating summary: {e}")
