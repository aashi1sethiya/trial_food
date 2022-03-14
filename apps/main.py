"""
This is the main function to navigate between the different pages of the app.
"""
import streamlit as st  # pip install streamlit
from apps import home, login, signup
import config


def main():
    """Manage the navigation menu: Home, Sign in, Create an account"""

    with open(config.PATH_TO_CSS) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    menu = ["Home", "Sign in", "Create an account"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home.main()
    elif choice == "Sign in":
        login.sign_in_outcomes()
    elif choice == "Create an account":
        signup.signup_form()
