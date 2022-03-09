# @Website:  https://ikitcheng.github.io
# @YouTube:  https://youtube.com/c/chinamatt
# @Project:  Food carbon and nutrition Dashboard w/ Streamlit

# TODO:

from ctypes import alignment
import pandas as pd  # pip install pandas openpyxl
import numpy as np  # math operations
import json  # json file
import streamlit as st  # pip install streamlit
from apps import home, login
from streamlit_autorefresh import st_autorefresh

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our Food Impact", 
                   page_icon=":egg:", 
                   layout="wide", 
                   initial_sidebar_state="collapsed", #auto, expanded
                   )


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load homepage
home.navbar()
login.main()