import streamlit as st
from util.utils import DBTools, Security


def signup_form():
    if "username" not in st.session_state:
        st.session_state["username"] = None

    if "username" in st.session_state:
        if st.session_state.username is not None:
            st.warning("Please logout to create a new account.")
        else:
            create_account_form = st.form("create_new_account")
            create_account_form.subheader("Create New Account")
            new_user = create_account_form.text_input("Username")
            new_password = create_account_form.text_input("Password", type="password")

            if create_account_form.form_submit_button("Signup"):
                
                if not DBTools.view_user(
                    new_user
                ):  # empty result -> username available
                    # create user in userstable
                    DBTools.add_userdata(new_user, Security.make_hashes(new_password))

                    st.success(
                        f"You have successfully created an account with username '{new_user}'."
                    )
                    st.info("Go to Login Menu to login")
                else:
                    st.warning(
                        f"The username '{new_user}' has been taken. Please try again."
                    )
