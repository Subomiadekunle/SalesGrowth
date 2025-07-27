import streamlit as st

def get_user_details():
    st.title("🏠 Welcome to SalesGrowth")
    st.markdown("Upload your sales data or try out our app using a sample sales file!")

    # 📥 Sample CSV download
    with open("sample_sales.csv", "rb") as file:
        btn = st.download_button(
            label="📥 Download Sample Sales File",
            data=file,
            file_name="sample_sales.csv",
            mime="text/csv"
        )
    
    st.markdown("""
    ---
    **👤 Why we ask for user info:**  
    To tailor insights, it helps to know your role. Whether you're in sales, ops, or just testing, this helps frame the data.
    """)
    
    # Add your user form or input logic here if needed

def get_user_details():
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
            if st.session_state.data_type == "company":
                company_name = st.text_input("🏢 Which company?")
                if company_name:
                    st.session_state.company_name = company_name
                    st.success(f"Great! Upload the {company_name} sales sheet now.")
            else:
                st.success(f"Awesome! 🚀 Upload your personal sales sheet now.")
                
