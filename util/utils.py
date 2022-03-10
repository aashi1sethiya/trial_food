"""
Utility functions used by the app. 
"""
import pandas as pd  # pip install pandas openpyxl
import json  # json file
import streamlit as st  # pip install streamlit

# ---- READ JSON data ----
@st.cache
def get_data_from_json(path_to_json):
    data = load_json(path_to_json)
    df = pd.json_normalize(data)
    return df


def load_json(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data
