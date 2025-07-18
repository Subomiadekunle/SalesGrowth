import streamlit as st
import plotly.express as px

def show_charts(df):
    st.header("📊 Visual Charts")
    chart_type = st.radio("Select chart type", ["Pie Chart", "Bar Graph", "Line Graph"])

    category_column = st.selectbox("Select category column:", df.columns)
    value_column = st.selectbox("Select value column:", df.columns)

    if category_column and value_column:
        if chart_type == "Pie Chart":
            fig = px.pie(df, values=value_column, names=category_column,
                         title=f"{value_column} by {category_column}")
        elif chart_type == "Bar Graph":
            fig = px.bar(df, x=category_column, y=value_column,
                         title=f"{value_column} by {category_column}")
        else:  # Line Graph
            fig = px.line(df, x=category_column, y=value_column,
                          title=f"{value_column} Over {category_column}")

        st.plotly_chart(fig, use_container_width=True)
