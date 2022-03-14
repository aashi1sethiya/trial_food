"""
This is the login page of the app. 
Once successfully logged in, the user can access restricted content.

Reference: 
1) Login app: https://blog.jcharistech.com/2020/05/30/how-to-add-a-login-section-to-streamlit-blog-app/
2) Authenticate class is adapted from: https://github.com/mkhorasani/Streamlit-Authenticator

"""

from datetime import datetime, timedelta
import pandas as pd
import jwt  # for encode and decode
import streamlit as st
import extra_streamlit_components as stx
from apps import design_your_meal, analytics, profile
from util.utils import DBTools, Security


class Authenticate:
    """A secure authentication class to validate user credentials in a Streamlit application.
    Uses cookies.
    Adapted from: https://github.com/mkhorasani/Streamlit-Authenticator
    """

    def __init__(self, cookie_name, key, cookie_expiry_days=30):
        """Create a new instance of "authenticate".
        Parameters
        ----------
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: int
            The number of days before the cookie expires on the client's browser.

        """
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days

    def token_encode(self):
        """
        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode(
            {"username": st.session_state["username"], "exp_date": self.exp_date},
            self.key,
            algorithm="HS256",
        )

    def token_decode(self):
        """
        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        return jwt.decode(self.token, self.key, algorithms=["HS256"])

    def exp_date(self):
        """
        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def login(self, form_name, location="main"):
        """Login form.
        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str, optional
            The location of the login form i.e. main or sidebar. Defaults to main.
        Returns
        -------
        str
            Name of authenticated user.
        boolean
            The status of authentication, None: no credentials entered, False: incorrect credentials, True: correct credentials.
        """
        self.location = location
        self.form_name = form_name

        if self.location not in ["main", "sidebar"]:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        cookie_manager = stx.CookieManager()

        if "authentication_status" not in st.session_state:
            st.session_state["authentication_status"] = None
        if "username" not in st.session_state:
            st.session_state["username"] = None
        if "logout" not in st.session_state:
            st.session_state["logout"] = None

        if st.session_state["authentication_status"] != True:
            try:
                self.token = cookie_manager.get(self.cookie_name)
                self.token = self.token_decode()

                if "logout" not in st.session_state:
                    st.session_state["logout"] = None

                if st.session_state["logout"] != True:
                    if self.token["exp_date"] > datetime.utcnow().timestamp():
                        st.session_state["username"] = self.token["username"]
                        st.session_state["authentication_status"] = True
                    else:
                        st.session_state["authentication_status"] = None
            except:
                st.session_state["authentication_status"] = None

            if st.session_state["authentication_status"] != True:
                if self.location == "main":
                    login_form = st.form("Login")
                elif self.location == "sidebar":
                    login_form = st.sidebar.form("Login")

                login_form.subheader(self.form_name)
                self.username = login_form.text_input("Username")
                self.password = login_form.text_input("Password", type="password")

                if login_form.form_submit_button("Login"):
                    result = DBTools.authenticate_user(
                        self.username,
                        Security.check_hashes(
                            self.password, Security.make_hashes(self.password)
                        ),
                    )
                    if result:  # correct username and password
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = self.username
                        self.exp_date = self.exp_date()
                        self.token = self.token_encode()
                        cookie_manager.set(
                            self.cookie_name,
                            self.token,
                            expires_at=datetime.now()
                            + timedelta(days=self.cookie_expiry_days),
                        )
                    else:
                        st.session_state["authentication_status"] = False
                        st.session_state["username"] = ""

        if st.session_state["authentication_status"] == True:
            # if self.location == 'main':
            #     if st.button('Logout'):
            #         cookie_manager.delete(self.cookie_name)
            #         st.session_state['logout'] = True
            #         st.session_state['username'] = None
            #         st.session_state['authentication_status'] = None
            # elif self.location == 'sidebar':
            st.sidebar.markdown(
                f"<a style='color:#DAF2DA'> Welcome *{st.session_state['username']}* </a>",
                unsafe_allow_html=True,
            )
            if st.sidebar.button("Logout"):
                st.session_state["logout"] = True
                cookie_manager.delete(self.cookie_name)
                st.session_state["username"] = None
                st.session_state["authentication_status"] = None

        return st.session_state["username"], st.session_state["authentication_status"]


def delete_user_form():
    delete_user_form = st.form("delete_user")
    delete_user_form.subheader("Delete User")
    username = delete_user_form.text_input("Username")
    if delete_user_form.form_submit_button("Delete"):
        result = DBTools.delete_user(username)
        st.write(result)


def reset_user_form():
    reset_user_form = st.form("reset_user_password")
    reset_user_form.subheader("Reset User Password")
    username = reset_user_form.text_input("Username")
    if reset_user_form.form_submit_button("Reset password"):
        result = DBTools.reset_user_password(username)
        st.write(result)


def sign_in_outcomes():
    authenticator = Authenticate(
        "some_cookie_name", "some_signature_key", cookie_expiry_days=1
    )
    username, authentication_status = authenticator.login("Login", "main")
    if st.session_state[
        "authentication_status"
    ]:  # use session state variables for multipage app
        logged_in_page(st.session_state["username"])
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
        st.session_state["username"] = None
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password.")


def logged_in_page(username):
    """Restricted access page for successfully logged in users only.

    Args:
        username (str): username of user.
    """
    if username == "admin":
        delete_user_form()
        reset_user_form()
        user_result = DBTools.view_all_users()
        st.dataframe(user_result)
    else:
        if not DBTools.view_usercontact(username) and not DBTools.view_userbudget(
            username
        ):
            task = st.sidebar.selectbox("Please choose an option", ["Profile"])
            st.warning("Please update your profile.")
        else:
            task = st.sidebar.selectbox(
                "Please choose an option", ["Design Your Meal", "Analytics", "Profile"]
            )

        if task == "Design Your Meal":
            meal_designer = design_your_meal.MealDesign(username=username)
            df_selection = meal_designer.select_dishes("Your Meal", "sidebar")
            if len(st.session_state["df_selection"]) == 0:
                st.warning("Please choose your dishes.")
            else:
                design_your_meal.meal_analysis(
                    df_selection=st.session_state["df_selection"]
                )
                if st.session_state["save"]:
                    design_your_meal.save_data()
                    st.sidebar.markdown(
                        "<a style='color:#DAF2DA'> Results saved. </a>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.sidebar.markdown(
                        "<a style='color:#DAF2DA'> New changes to save. </a>",
                        unsafe_allow_html=True,
                    )
        elif task == "Analytics":
            analytics.main()

        elif task == "Profile":
            profile.main()
