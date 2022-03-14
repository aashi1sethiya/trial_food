""" 
This is the Analytics page which shows your carbon footprint over time.

More analytics data will be added in the future.
"""
from ast import parse
from os import environ
import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep
import streamlit as st
from util import plots
from util.utils import DBTools


def calc_CO2_this_month(df_user):
    current_month = datetime.now().month
    current_year = datetime.now().year
    CO2_this_month = df_user.query(
        "Datetime.dt.month == @current_month & Datetime.dt.year == @current_year"
    )["CO2e"].sum()
    return CO2_this_month


def calc_CO2_total(df_user):
    return df_user.CO2e.sum()


def calc_CO2_daily_average(df_user):
    CO2_total = calc_CO2_total(df_user)
    nDays = len(df_user.Datetime.dt.date.unique())
    CO2_daily_average = CO2_total / nDays
    return CO2_daily_average


def calc_nTrees_offset_CO2(df_user):
    """
    Calculate the number of trees needed to offset the user's CO2 emissions.
    Assume 24 kgCO2 / tree / year. Source: https://www.encon.be/en/calculation-co2-offsetting-trees
    """
    CO2_daily_average = calc_CO2_daily_average(df_user)
    nTrees = CO2_daily_average / (24 / 365)
    return nTrees


def environment_analytics(df_user):
    CO2_this_month = calc_CO2_this_month(df_user)
    CO2_total = calc_CO2_total(df_user)
    nTrees = calc_nTrees_offset_CO2(df_user)

    st.subheader("Your Carbon footprint :factory:")
    col1, col2 = st.columns(2)
    with col1:
        col1.metric("This month: ", f"{CO2_this_month:.1f} kgCO2e", "")
    with col2:
        col2.metric(f"Total: ", f"{CO2_total:.1f} kgCO2e", "")

    st.caption(
        f"You need {int(np.ceil(nTrees))} :deciduous_tree: to offset your food carbon emissions!"
    )
    fig_user_CO2e = plots.plot_user_CO2e(df_user)
    st.plotly_chart(fig_user_CO2e, use_container_width=True)


def nutrition_analytics(df_user):
    col1, col2 = st.columns(2)

    # Calories history
    fig_user_calories = plots.plot_user_calories(df_user)
    col1.subheader("Your Calories History (kcal)")
    col1.plotly_chart(fig_user_calories, use_container_width=True)

    # average macro split
    fig_user_macro_split = plots.plot_user_macro_split(df_user)
    col2.subheader("Your Macro Split (average)")
    col2.plotly_chart(fig_user_macro_split, use_container_width=True)


def delete_user_meal_log_form():
    delete_user_meal_log_form = st.form("delete_user_meal_log")
    delete_user_meal_log_form.subheader("Delete Meal Log")
    Datetime = delete_user_meal_log_form.text_input("Datetime", key='Datetime_key')
    Datetime_str = str(pd.to_datetime(Datetime)) # convert to datetime string
    if delete_user_meal_log_form.form_submit_button("Delete"):
        result = DBTools.delete_user_meal_log(st.session_state.username, datetime=Datetime_str)
        with st.spinner(f'Deleting entry {Datetime}...'):
            sleep(0.5)
        del st.session_state.Datetime_key
        st.session_state.Datetime_key = "" # clear input
        st.experimental_rerun()

def main():
    user_meal_log = DBTools.view_usermeallog(st.session_state.username)
    if user_meal_log: # found meal log for user
        df_meal_log = pd.DataFrame(user_meal_log, columns=["Username", "Datetime", "Dishes", "Amount", "CO2e", "Calories", "Carbs", "Protein", "Fat"])
        df_meal_log['Datetime'] = pd.to_datetime(df_meal_log['Datetime'])

        # Environment
        environment_analytics(df_meal_log)

        # Nutrition
        nutrition_analytics(df_meal_log)
        
        # view full meal log
        st.dataframe(df_meal_log)

        # delete a meal log 
        delete_user_meal_log_form()

    else:
        st.error("No meal log available.")