# Tutorial: # guide https://blog.jcharistech.com/2020/05/30/how-to-add-a-login-section-to-streamlit-blog-app/

from configparser import SectionProxy
import logging
from unittest import result
import streamlit as st  # pip install streamlit
from datetime import datetime, timedelta
import jwt
import extra_streamlit_components as stx
from streamlit_lottie import st_lottie  # animations
import sqlite3 # Database management
import hashlib # Security (other libraries include: passlib,hashlib,bcrypt,scrypt)
import pandas as pd
from util import lottie  # utility functions for graphics
from apps import home, analytics

class Security:
    """ Hash passwords so passwords are not revealed even if people can see the database. 
    """
    def make_hashes(password):
        """ Hash passwords with sha (secure hash algorithm) developed by NSA.

        Args:
            password (str): user password.

        Returns:
            (str): hash key corresponding to the user password.
        """
        return hashlib.sha256(str.encode(password)).hexdigest() 

    def check_hashes(password, hashed_text):
        if Security.make_hashes(password) == hashed_text:
            return hashed_text
        return False

# Database management
conn = sqlite3.connect('./data/app_user_data.db', check_same_thread=False)
c = conn.cursor()

class DBTools:
    """Database functions to create, add, login, and view users.
    """

    def create_usertable():
        c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

    def add_userdata(username,password):
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

    def authenticate_user(username,password):
        """Return the data corresponding to username and password input. 
        """
        c.execute('SELECT * FROM userstable WHERE username=? AND password=?',(username,password))
        data = c.fetchall()
        return data

    def view_user(username):
        c.execute('SELECT * FROM userstable WHERE username=?',(username,))
        data = c.fetchall()
        return data

    def view_all_users():
        c.execute('SELECT * FROM userstable')
        data = c.fetchall()
        return data

    def delete_user(username):
        if DBTools.view_user(username):
            try:
                c.execute('DELETE FROM userstable WHERE username=?',(username,))
                conn.commit()
                message = f"You deleted user '{username}'. Record updated successfully."
            except sqlite3.Error as error:
                message = f"Failed to update sqlite table. {error}"
        else:
            message = f"Username '{username}' not found."

        return message

    def reset_user_password(username):
        if DBTools.view_user(username):
            try:
                default_password = '12345'
                default_password_hash = Security.make_hashes('12345')
                c.execute('UPDATE userstable SET password=? WHERE username=?',(default_password_hash,username))
                conn.commit()
                message = f"User '{username}' password has been reset to {default_password}. Record updated successfully."
            except sqlite3.Error as error:
                message = f"Failed to update sqlite table. {error}"
        else:
            message = f"Username '{username}' not found."
        return message


class Authenticate:
    """A secure authentication class to validate user credentials in a Streamlit application.
    Uses cookies. 
    Adapted from: https://github.com/mkhorasani/Streamlit-Authenticator 
    """
    def __init__(self,cookie_name,key,cookie_expiry_days=30):
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
        return jwt.encode({'username':st.session_state['username'],
        'exp_date':self.exp_date},self.key,algorithm='HS256')

    def token_decode(self):
        """
        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        return jwt.decode(self.token,self.key,algorithms=['HS256'])

    def exp_date(self):
        """
        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def login(self,form_name,location='main'):
        """ Login form.
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

        if self.location not in ['main','sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        cookie_manager = stx.CookieManager()

        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'username' not in st.session_state:
            st.session_state['username'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None

        if st.session_state['authentication_status'] != True:
            try:
                self.token = cookie_manager.get(self.cookie_name)
                self.token = self.token_decode()

                if 'logout' not in st.session_state:
                    st.session_state['logout'] = None

                if st.session_state['logout'] != True:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        st.session_state['username'] = self.token['username']
                        st.session_state['authentication_status'] = True
                    else:
                        st.session_state['authentication_status'] = None
            except:
                st.session_state['authentication_status'] = None

            if st.session_state['authentication_status'] != True:
                if self.location == 'main':
                    login_form = st.form('Login')
                elif self.location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(self.form_name)
                self.username = login_form.text_input('Username')
                self.password = login_form.text_input('Password',type='password')

                if login_form.form_submit_button('Login'):
                    result = DBTools.authenticate_user(self.username,Security.check_hashes(self.password, Security.make_hashes(self.password)))
                    if result: # correct username and password
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = self.username
                        self.exp_date = self.exp_date()
                        self.token = self.token_encode()
                        cookie_manager.set(self.cookie_name, self.token,
                        expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                    else:
                        st.session_state['authentication_status'] = False
                        st.session_state['username'] = ''
        
        if st.session_state['authentication_status'] == True:
            # if self.location == 'main':
            #     if st.button('Logout'):
            #         cookie_manager.delete(self.cookie_name)
            #         st.session_state['logout'] = True
            #         st.session_state['username'] = None
            #         st.session_state['authentication_status'] = None
            # elif self.location == 'sidebar':
            st.sidebar.markdown(f"<a style='color:#DAF2DA'> Welcome *{st.session_state['username']}* </a>", unsafe_allow_html=True)
            if st.sidebar.button('Logout'):
                st.session_state['logout'] = True
                cookie_manager.delete(self.cookie_name)
                st.session_state['username'] = None
                st.session_state['authentication_status'] = None
        
        return st.session_state['username'], st.session_state['authentication_status']

def delete_user_form():
    delete_user_form = st.form('delete_user')
    delete_user_form.subheader('Delete User')
    username = delete_user_form.text_input('Username')
    if delete_user_form.form_submit_button('Delete'):
        result = DBTools.delete_user(username)
        st.write(result)

def reset_user_form():
    reset_user_form = st.form('reset_user_password')
    reset_user_form.subheader('Reset User Password')
    username = reset_user_form.text_input('Username')
    if reset_user_form.form_submit_button('Reset password'):
        result = DBTools.reset_user_password(username)
        st.write(result)

def signup_form():
    create_account_form = st.form('create_new_account')
    create_account_form.subheader('Create New Account')
    new_user = create_account_form.text_input("Username")
    new_password = create_account_form.text_input("Password",type='password')

    if create_account_form.form_submit_button("Signup"):
        DBTools.create_usertable()
        result = DBTools.view_user(new_user)
        if not result: # can't find user in database
            DBTools.add_userdata(new_user, Security.make_hashes(new_password))
            st.success(f"You have successfully created an account with username '{new_user}'.")
            st.info("Go to Login Menu to login")
        else: 
            st.warning(f"The username '{new_user}' has been taken. Please try again.")

def logged_in_page(username):
    if username == 'admin':
        delete_user_form()
        reset_user_form()
        user_result = DBTools.view_all_users()
    else:
        home.title()
        task = st.sidebar.selectbox("Please choose an option",["Design Your Meal","Analytics","Profile"])
        if task == "Design Your Meal":
            meal_designer = home.MealDesign(username=username)
            df_selection = meal_designer.select_dishes('Your Meal','sidebar')
            if len(st.session_state['df_selection']) == 0:
                st.warning('Please choose your dishes.')
            else:
                home.meal_analysis(df_selection=st.session_state['df_selection'])
                if st.session_state['save']:
                    home.save_data()
                    st.sidebar.markdown("<a style='color:#DAF2DA'> Results saved. </a>", unsafe_allow_html=True)
                else:
                    st.sidebar.markdown("<a style='color:#DAF2DA'> New changes to save. </a>", unsafe_allow_html=True)
        elif task == "Analytics":
            st.subheader("Your Meal Analytics")
            analytics.main()
            
        elif task == "Profile":
            st.subheader("Your Profile")
            user_result = DBTools.view_user(username)
            df_user = pd.DataFrame(user_result,columns=["Username", 'Password'])
            st.dataframe(df_user)

def main():
    """Simple Login App"""    

    with open('./styles/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    menu = ["Home","Sign in","Create an account"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        home.title()

    elif choice == "Sign in":
        authenticator = Authenticate('some_cookie_name','some_signature_key',cookie_expiry_days=1)
        username, authentication_status = authenticator.login('Login','main')
        if st.session_state['authentication_status']: # use session state variables for multipage app 
            logged_in_page(st.session_state['username'])
        elif st.session_state['authentication_status'] == False:
            st.error('Username/password is incorrect')
        elif st.session_state['authentication_status'] == None:
            st.warning('Please enter your username and password.')
    elif choice == "Create an account":
        signup_form()
    
if __name__ == '__main__':
    main()