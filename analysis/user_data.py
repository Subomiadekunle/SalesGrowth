import streamlit as st

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
                
