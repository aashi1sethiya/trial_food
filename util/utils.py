"""
Utility functions used by the app. 
"""
import pandas as pd  # pip install pandas openpyxl
import json  # json file
import streamlit as st  # pip install streamlit
import sqlite3  # Database management
import hashlib  # Security (other libraries include: passlib,hashlib,bcrypt,scrypt)
import config  # paths to files
import pyrebase  # Python wrapper for Firebase
from google.cloud import firestore  # Python wrapper for Firebase
from google.oauth2 import service_account  # Python wrapper for Google auth


class Firebase:
    def __init__(self):
        cred = json.loads(
            st.secrets["appConfigKey"]
        )  # use streamlit secrets to hide sensitive information
        # cred = load_json(config.PATH_TO_FIREBASE_CONFIG+'firebase_app_config.json')
        try:
            firebase = pyrebase.initialize_app(cred)
        except ValueError:
            pass
            # firebase_admin.delete_app(st.session_state['app'])
        self.auth = firebase.auth()

    def create_user(self, email, password):
        # Firebase auth create user
        user = self.auth.create_user_with_email_and_password(
            email=email, password=password
        )
        return user

    def signin(self, email, password):
        # Firebase auth signin user
        user = self.auth.sign_in_with_email_and_password(email, password)
        return user

    def db(self):
        """Connect to firestore database."""
        service_account_dict = json.loads(st.secrets["serviceAccountKey"])
        creds = service_account.Credentials.from_service_account_info(
            service_account_dict
        )
        # db = firestore.Client.from_service_account_json(config.PATH_TO_FIREBASE_CONFIG+'firebase_service_account.json')
        db = firestore.Client(
            credentials=creds, project=config.FIREBASE_APP_NAME
        )  # use streamlit secrets to hide sensitive information
        return db

    def check_user(self, user_localid):
        """Check that the user with `user_localid` exists in firestore db.
        Args:
            user_localid (str): user localId (created by Firebase create_user).
        Returns:
            doc_dict (dict, None): If user exists, get a dict. If not, get None.
        """
        firestore_db = self.db()
        doc_ref = firestore_db.collection("userstable").document(user_localid)
        doc = doc_ref.get()
        doc_dict = doc.to_dict()
        return doc_dict

    def delete_user_meal_log(self, user_localid, datetime):
        """Delete a document in firestore db.
        Ref: https://firebase.google.com/docs/firestore/manage-data/delete-data#python
        Args:
            user_localid (str): user localId (created by Firebase create_user).
            datetime (str): Datetime string in format YYYY-MM-DD HH:MM:SS.

        Returns:
            (tuple): boolean (true if successfully deleted), outcome message. 
        """
        db = self.db()
        try:
            db.collection("usersmeallogs").document(user_localid).collection(
                "meallogs"
            ).document(datetime).delete()
            success = True
            message = f"You deleted entry '{datetime}'. Record updated successfully."
        except:
            success = False
            message = f"User {user_localid}: '{datetime}' entry not found."
        return success, message


# ---- READ JSON data ----
@st.cache(allow_output_mutation=True)
def get_data_from_json(path_to_json):
    data = load_json(path_to_json)
    df = pd.json_normalize(data)
    return df


def load_json(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def read_html(path_to_html):
    f = open(path_to_html, "r")
    contents = f.read()
    f.close()
    return contents


class Security:
    """Hash passwords so passwords are not revealed even if people can see the database."""

    def make_hashes(password):
        """Hash passwords with sha (secure hash algorithm) developed by NSA.

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


class DBTools:
    """Database functions to create, add, login, and view users."""

    # Connect Database
    conn = sqlite3.connect(config.PATH_TO_APP_USER_DATA, check_same_thread=False)
    c = conn.cursor()

    def create_userstable():
        """Table of usernames and passwords."""
        DBTools.c.execute(
            "CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)"
        )

    def create_userscontacts():
        """
        Table of contact info for each user.
        """
        DBTools.c.execute(
            "CREATE TABLE IF NOT EXISTS userscontacts(username TEXT,name TEXT,age INTEGER,gender TEXT,email TEXT)"
        )

    def create_usersbudgets():
        """
        Table of carbon and nutrition budget for each user.
        """
        DBTools.c.execute(
            "CREATE TABLE IF NOT EXISTS usersbudgets(username TEXT,co2 REAL,calories REAL,carbs REAL,protein REAL,fat REAL)"
        )

    def create_usersmeallogs():
        """
        Table of meal logs for each user.
        """
        DBTools.c.execute(
            "CREATE TABLE IF NOT EXISTS usersmeallogs(username TEXT,datetime TEXT,dishtypes TEXT,dishnames TEXT,amount TEXT,co2 REAL,calories REAL,carbs REAL,protein REAL,fat REAL)"
        )

    def add_userdata(username, password):
        DBTools.c.execute(
            "INSERT INTO userstable(username,password) VALUES (?,?)",
            (username, password),
        )
        DBTools.conn.commit()

    def add_usercontactdata(username, name, age, gender, email):
        DBTools.c.execute(
            "INSERT INTO userscontacts(username,name,age,gender,email) VALUES (?,?,?,?,?)",
            (username, name, age, gender, email),
        )
        DBTools.conn.commit()

    def add_userbudgetdata(username, co2, calories, carbs, protein, fat):
        DBTools.c.execute(
            "INSERT INTO usersbudgets(username,co2,calories,carbs,protein,fat) VALUES (?,?,?,?,?,?)",
            (username, co2, calories, carbs, protein, fat),
        )
        DBTools.conn.commit()

    def add_usermealdata(
        username,
        datetime,
        dishtypes,
        dishnames,
        amount,
        co2,
        calories,
        carbs,
        protein,
        fat,
    ):
        DBTools.c.execute(
            "INSERT INTO usersmeallogs(username,datetime,dishtypes,dishnames,amount,co2,calories,carbs,protein,fat) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                username,
                datetime,
                dishtypes,
                dishnames,
                amount,
                co2,
                calories,
                carbs,
                protein,
                fat,
            ),
        )
        DBTools.conn.commit()

    def authenticate_user(username, password):
        """Return the data corresponding to username and password input."""
        DBTools.c.execute(
            "SELECT * FROM userstable WHERE username=? AND password=?",
            (username, password),
        )
        data = DBTools.c.fetchall()
        return data

    def view_user(username):
        DBTools.c.execute("SELECT * FROM userstable WHERE username=?", (username,))
        data = DBTools.c.fetchall()
        return data

    def view_usercontact(username):
        DBTools.c.execute("SELECT * FROM userscontacts WHERE username=?", (username,))
        data = DBTools.c.fetchall()
        return data

    def view_userbudget(username):
        DBTools.c.execute("SELECT * FROM usersbudgets WHERE username=?", (username,))
        data = DBTools.c.fetchall()
        return data

    def view_usermeallog(username):
        DBTools.c.execute("SELECT * FROM usersmeallogs WHERE username=?", (username,))
        data = DBTools.c.fetchall()
        return data

    def view_all_users():
        DBTools.c.execute("SELECT * FROM userstable")
        data = DBTools.c.fetchall()
        return data

    def delete_user(username):
        if DBTools.view_user(username):
            try:
                DBTools.c.execute(
                    "DELETE FROM userstable WHERE username=?", (username,)
                )
                DBTools.c.execute(
                    "DELETE FROM userscontacts WHERE username=?", (username,)
                )
                DBTools.c.execute(
                    "DELETE FROM usersbudgets WHERE username=?", (username,)
                )
                DBTools.c.execute(
                    "DELETE FROM usersmeallogs WHERE username=?", (username,)
                )
                DBTools.conn.commit()
                message = f"You deleted user '{username}'. Record updated successfully."
            except sqlite3.Error as error:
                message = f"Failed to update sqlite table. {error}"
        else:
            message = f"Username '{username}' not found."

        return message

    def delete_user_meal_log(username, datetime):
        if DBTools.view_usermeallog(username):
            try:
                DBTools.c.execute(
                    "DELETE FROM usersmeallogs WHERE (username=? AND datetime=?)",
                    (username, datetime),
                )
                DBTools.conn.commit()
                message = (
                    f"You deleted entry '{datetime}'. Record updated successfully."
                )
            except sqlite3.Error as error:
                message = f"Failed to update sqlite table. {error}"
        else:
            message = f"Username '{username}' not found."

        return message

    def reset_user_password(username):
        if DBTools.view_user(username):
            try:
                default_password = "12345"
                default_password_hash = Security.make_hashes("12345")
                DBTools.c.execute(
                    "UPDATE userstable SET password=? WHERE username=?",
                    (default_password_hash, username),
                )
                DBTools.conn.commit()
                message = f"User '{username}' password has been reset to {default_password}. Record updated successfully."
            except sqlite3.Error as error:
                message = f"Failed to update sqlite table. {error}"
        else:
            message = f"Username '{username}' not found."
        return message

    def update_usercontactdata(username, name, age, gender, email):
        try:
            DBTools.c.execute(
                "UPDATE userscontacts SET name=?,age=?,gender=?,email=? WHERE username=?",
                (name, age, gender, email, username),
            )
            DBTools.conn.commit()
            message = "Update successful."
        except sqlite3.Error as error:
            message = f"Failed to update sqlite table. {error}"

        return message

    def update_userbudgetdata(username, co2, calories, carbs, protein, fat):
        try:
            DBTools.c.execute(
                "UPDATE usersbudgets SET co2=?,calories=?,carbs=?,protein=?,fat=? WHERE username=?",
                (co2, calories, carbs, protein, fat, username),
            )
            DBTools.conn.commit()
            message = "Update successful."

        except sqlite3.Error as error:
            message = f"Failed to update sqlite table. {error}"
            st.write(message)

        return message
