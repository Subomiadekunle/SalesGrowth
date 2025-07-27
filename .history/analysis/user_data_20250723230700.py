import streamlit as st
import pandas as pd

def get_user_details():
    st.title("🏠 Welcome to SalesGrowth")
    st.markdown("Upload your sales data or try out our app using a sample sales file!")

    # 📥 Sample CSV download + preview
    st.markdown("### 🧪 Sample Sales File")
    with open("sample_sales.csv", "rb") as file:
        st.download_button(
            label="📥 Download Sample Sales File",
            data=file,
            file_name="sample_sales.csv",
            mime="text/csv"
        )

    try:
        df_preview = pd.read_csv("sample_sales.csv")
        st.markdown("🔍 Here's what the sample file looks like:")
        st.dataframe(df_preview.head())
    except Exception as e:
        st.error(f"Couldn't load sample file preview: {e}")

    # Divider
    st.markdown("---")

    # 👤 User Info Collection
    st.markdown("### 👤 Tell us about yourself")

    if "user_name" not in st.session_state:
        user_name = st.text_input("👋 What is your name?")
        if user_name:
            st.session_state.user_name = user_name
            st.success(f"Hi {user_name}, let’s help interpret your sales data!")

    if "user_name" in st.session_state and "data_type" not in st.session_state:
        data_type = st.radio(
            "📂 Is this sales sheet for a company or for personal use?",
            ["Company", "Personal"]
        )
        if data_type:
            st.session_state.data_type = data_type.lower()
            if data_type == "Company":
                company_name = st.text_input("🏢 Which company?")
                if company_name:
                    st.session_state.company_name = company_name
                    st.success(f"Great! Upload the {company_name} sales sheet now.")
            else:
                st.success("Awesome! 🚀 Upload your personal sales sheet now.")

    # Store all info in one dict (optional)
    st.session_state.user_info = {
        "name": st.session_state.get("user_name"),
        "type": st.session_state.get("data_type"),
        "company": st.session_state.get("company_name", None)
    }
