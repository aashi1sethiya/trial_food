import pandas as pd
import streamlit as st
from util.utils import DBTools, Security, read_html, Firebase
import config  # paths to files
import time


def update_profile_form():
    """Update user profile information, including contact info and carbon and nutrition budget."""

    ### Local: Check for exisiting user contact and budget info in local sqlite3 database ###
    # username = st.session_state.username
    # user_contact = DBTools.view_usercontact(username)
    # user_budget = DBTools.view_userbudget(username)
    # if user_contact:
    #     _, name_val, age_val, gender_val, email_val = user_contact[0]
    # else:
    #     name_val, age_val, gender_val, email_val = "", "", "", ""
    # if user_budget:
    #     _, co2_val, calories_val, carbs_val, protein_val, fat_val = user_budget[0]
    # else:
    #     df_rdi = pd.read_csv(config.PATH_TO_NUTRITION_RDI)
    #     livelca_CO2_budget = 2.72  # (kg) based on LiveLCA threshold
    #     co2_val, calories_val, carbs_val, protein_val, fat_val = (
    #         livelca_CO2_budget,
    #         df_rdi["Energ_Kcal"].values[0],
    #         df_rdi["Carbohydrt_(g)"].values[0],
    #         df_rdi["Protein_(g)"].values[0],
    #         df_rdi["Lipid_Tot_(g)"].values[0],
    #     )

    ### Firebase: Check for exisiting user contact and budget info###
    firebase = Firebase()
    doc_dict = firebase.check_user(st.session_state["firebase_user"]["localId"])
    if doc_dict is not None:
        name_val, age_val, gender_val, email_val = (
            doc_dict["name"],
            doc_dict["age"],
            doc_dict["gender"],
            doc_dict["email"],
        )
        co2_val, calories_val, carbs_val, protein_val, fat_val = (
            doc_dict["co2_budget"],
            doc_dict["calories_budget"],
            doc_dict["carbs_budget"],
            doc_dict["protein_budget"],
            doc_dict["fat_budget"],
        )
    else:
        name_val, age_val, gender_val, email_val = "", "", "", st.session_state["username"]
        df_rdi = pd.read_csv(config.PATH_TO_NUTRITION_RDI)
        livelca_CO2_budget = 2.72  # (kg) based on LiveLCA threshold
        co2_val, calories_val, carbs_val, protein_val, fat_val = (
            livelca_CO2_budget,
            df_rdi["Energ_Kcal"].values[0],
            df_rdi["Carbohydrt_(g)"].values[0],
            df_rdi["Protein_(g)"].values[0],
            df_rdi["Lipid_Tot_(g)"].values[0],
        )

    # Form
    col1, col2 = st.columns([3, 2])
    profile_form = col1.form("Update Profile Info")
    profile_form.subheader("Your Profile Details")
    name = profile_form.text_input("Name *", value=name_val)
    age = profile_form.text_input("Age *", value=age_val)
    gender = profile_form.text_input("Gender *", value=gender_val)
    email = profile_form.text_input("Email *", value=email_val)

    profile_form.subheader("Your Daily Carbon and Nutrition Budget")
    co2_budget = profile_form.text_input("Carbon (kgCO2e)", value=co2_val)
    calories_budget = profile_form.text_input("Calories (kcal)", value=calories_val)
    carbs_budget = profile_form.text_input("Carbs (g)", value=carbs_val)
    protein_budget = profile_form.text_input("Protein (g)", value=protein_val)
    fat_budget = profile_form.text_input("Fat (g)", value=fat_val)

    if profile_form.form_submit_button("Update"):

        ### Local sqlite3 database auth: userscontacts ###
        # if not DBTools.view_usercontact(username):  # can't find user in database
        #     DBTools.add_usercontactdata(username, name, age, gender, email)
        # else:
        #     DBTools.update_usercontactdata(username, name, age, gender, email)

        # # User budget
        # if not DBTools.view_userbudget(username):  # can't find user in database
        #     DBTools.add_userbudgetdata(
        #         username,
        #         co2_budget,
        #         calories_budget,
        #         carbs_budget,
        #         protein_budget,
        #         fat_budget,
        #     )
        # else:
        #     DBTools.update_userbudgetdata(
        #         username,
        #         co2_budget,
        #         calories_budget,
        #         carbs_budget,
        #         protein_budget,
        #         fat_budget,
        #     )

        #
        ### Firebase: Creating a new document under the collection 'userstable' ###
        firebase = Firebase()
        firebase_db = firebase.db()
        doc_ref = firebase_db.collection("userstable").document(
            st.session_state["firebase_user"]["localId"]
        )

        try:
            doc_ref.set(
                {
                    "localID": st.session_state["firebase_user"]["localId"],
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "email": st.session_state["username"],
                    "co2_budget": float(co2_budget),
                    "calories_budget": float(calories_budget),
                    "carbs_budget": float(carbs_budget),
                    "protein_budget": float(protein_budget),
                    "fat_budget": float(fat_budget),
                }
            )
            
            st.success(f"Your profile has been updated.")
            time.sleep(1)
            st.experimental_rerun()

        except Exception as e:
            st.error(e)


def main():
    update_profile_form()
    # user = DBTools.view_user(st.session_state.username)
    # user_contact = DBTools.view_usercontact(st.session_state.username)
    # user_budget = DBTools.view_userbudget(st.session_state.username)
    # df_user = pd.DataFrame(user, columns=["Username", "Password"])
    # df_contact = pd.DataFrame(user_contact, columns=["Username", "Name", "Age", "Gender", "Email"])
    # df_budget = pd.DataFrame(user_budget, columns=["Username", "co2_budget", "calories_budget", "carbs_budget", "protein_budget", "fat_budget"])
    # st.dataframe(df_user)
    # st.dataframe(df_contact)
    # st.dataframe(df_budget)
