# @Website:  https://ikitcheng.github.io
# @YouTube:  https://youtube.com/c/chinamatt
# @Project:  Food carbon and nutrition Dashboard w/ Streamlit

""" 
This app starts the Food carbon and nutrition Dashboard w/ Streamlit.
"""

import streamlit as st  # pip install streamlit
from apps import home, main
from util import bg_image
import config

if __name__ == "__main__":
    # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    st.set_page_config(
        page_title="Our Food Impact",
        page_icon=f"{config.PATH_TO_IMAGES}page_icon.png",
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

    # Apply css style
    with open(config.PATH_TO_CSS) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load background image
    bg_image.set_png_as_page_bg(
        f"{config.PATH_TO_IMAGES}bg/background_opacity_100_new_bgcolor_shift.png"
    )

    # Load homepage
    # home.navbar()
    home.title()
    main.main()
