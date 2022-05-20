"""
This is the main function to navigate between the different pages of the app.
"""
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu
from apps import home, login, signup
from util.utils import DBTools


def main():
    """Manage the navigation menu: Home, Sign in, Create an account"""

    menu = ["Home", "Sign in", "Create an account"]
    # choice = st.sidebar.selectbox("Menu", menu) # simple dropdown menu
    with st.sidebar:
        # fancy option menu
        choice = option_menu(
            menu_title=None,  # required
            options=menu,  # required
            icons=["house", "person-circle", "person-plus-fill"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="vertical",  # horizontal
            styles={
                "container": {"padding": "0!important", "background-color": "#544B35"},
                "icon": {"color": "#DAF2DA", "font-size": "18px"},
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "color": "#DAF2DA",
                    "margin": "0px",
                    "--hover-color": "#716657",
                },
                "nav-link-selected": {"background-color": "#716657"},
            },
        )

    # Setup database tables first if not exist
    DBTools.create_userstable()
    DBTools.create_userscontacts()
    DBTools.create_usersbudgets()
    DBTools.create_usersmeallogs()

    # Choose page
    if choice == "Home":
        home.main()
    elif choice == "Sign in":
        login.sign_in_outcomes()
    elif choice == "Create an account":
        signup.signup_form()
