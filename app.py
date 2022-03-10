# @Website:  https://ikitcheng.github.io
# @YouTube:  https://youtube.com/c/chinamatt
# @Project:  Food carbon and nutrition Dashboard w/ Streamlit

""" 
This app starts the Food carbon and nutrition Dashboard w/ Streamlit.
"""

import streamlit as st  # pip install streamlit
from apps import home, main

if __name__ == '__main__':
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(
        page_title="Our Food Impact",
        page_icon=":egg:",
        layout="wide",
        initial_sidebar_state="collapsed",  # auto, expanded
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
    home.title()
    main.main()
