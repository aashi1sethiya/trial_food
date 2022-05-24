from multiprocessing.sharedctypes import Value
import streamlit as st
from requests.exceptions import HTTPError
import ast
from util.utils import DBTools, Security, read_html, Firebase
import config


def signup_form():

    if "username" not in st.session_state:
        st.session_state["username"] = None

    elif "username" in st.session_state:
        if st.session_state.username is not None:
            st.warning("Please logout to create a new account.")
        else:
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    contents = read_html(f"{config.PATH_TO_HTML}/signup.html")
                    st.markdown(contents, unsafe_allow_html=True)
                with col2:
                    create_account_form = st.form("create_new_account")
                    create_account_form.subheader("Create New Account")
                    new_user = create_account_form.text_input("Username")
                    new_password = create_account_form.text_input(
                        "Password", type="password"
                    )
                    st.warning("Please choose a username and password.")

                    if create_account_form.form_submit_button("Signup"):
                        if len(new_user) == 0 or len(new_password) == 0:
                            st.error("Please enter a valid username and password.")

                        ### Local sqlite3 database auth: userstable ###
                        # elif not DBTools.view_user(
                        #     new_user
                        # ):  # empty result -> username available
                        #     # create user in userstable
                        #     DBTools.add_userdata(new_user, Security.make_hashes(new_password))

                        #     st.success(
                        #         f"You have successfully created an account with username '{new_user}'."
                        #     )
                        #     st.info("Go to Login Menu to login")

                        # else:
                        #     st.error(
                        #         f"The username '{new_user}' has been taken. Please try again."
                        #     )

                        ### Firebase auth ###
                        firebase = Firebase()
                        try:
                            firebase_user = firebase.create_user(new_user, new_password)
                        except HTTPError as e:
                            st.error(ast.literal_eval(e.strerror)["error"]["message"])
                        except ValueError as e:
                            st.error(e)

                        # automatially sign in after sign up
                        st.session_state["firebase_user"] = firebase.signin(
                            new_user, new_password
                        )
                        st.session_state["authentication_status"] = True
                        st.session_state["username"] = new_user
